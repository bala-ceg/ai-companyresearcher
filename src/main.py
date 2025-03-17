import asyncio
import json
import logging
from apify import Actor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.tools import research_company
from src.models import CompanyResearchState
import os
# Configure Logging
Actor.log.setLevel(logging.INFO)

# OpenAI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)

async def save_report(state):
    """Save the research report in markdown format & store in Apify KV Store."""
    
    report_content = state["research_report"]

    # Store report in Apify Key-Value Store
    store = await Actor.open_key_value_store()
    await store.set_value("company_research_report.md", report_content)
    Actor.log.info('Saved the "company_research_report.md" file into the key-value store!')

async def main():
    """Runs the AI Company Research workflow."""
    async with Actor:
        actor_input = await Actor.get_input() or {}
        Actor.log.info(f"Received input: {actor_input}")

        # Extract company name from input
        company_name = actor_input.get("company_name")
        if not company_name:
            Actor.log.error("Company name is required in input.")
            return

        # Run research
        research_data = research_company(company_name)

        # Prepare research findings for report generation
        research_findings = json.dumps(research_data["research_findings"], indent=2)
        company_url = research_data["company_url"]

        # LLM Prompt for Report Generation
        report_prompt = ChatPromptTemplate.from_template("""
        You are an expert researcher tasked with writing a fact-based report on recent developments for the company **{company_name}**.
        Write the report in Markdown format, but **do not include a title**. Each section must be written in well-structured paragraphs, not lists or bullet points.

        Ensure the report includes:
        - **Inline citations** as Markdown hyperlinks directly in the main sections (e.g., Company X is an innovative leader in AI ([LinkedIn](https://linkedin.com))).
        - A **Citations Section** at the end that lists all URLs used.

        ### Report Structure:
        1. **Executive Summary**:
            - Overview of the company, its services, location, employee count, and achievements.

        2. **Leadership and Vision**:
            - CEO and key team members, their experience, and strategic impact.

        3. **Product and Service Overview**:
            - Summary of main offerings, unique features, and target customers.

        4. **Financial Performance**:
            - Revenue, funding rounds, investors, and growth metrics.

        5. **Recent Developments**:
            - Product updates, partnerships, and market strategies.

        6. **Citations**:
            - Inline citations within the text.
            - Full list of referenced URLs.

        ---
        **Company Website:** {company_url}  
        **Research Findings:** {research_findings}
        """)

        # Generate report
        Actor.log.info(f"Generating research report for {company_name}")
        response = report_prompt | llm
        research_report = response.invoke({
            "company_name": company_name,
            "company_url": company_url,
            "research_findings": research_findings
        }).content  # Ensure correct input keys

        # Store report in state
        final_state = {
            "company_name": company_name,
            "company_url": company_url,
            "research_report": research_report
        }

        # Save final report
        await save_report(final_state)

        # Push final state to Apify dataset
        await Actor.push_data(final_state)

if __name__ == "__main__":
    asyncio.run(main())
