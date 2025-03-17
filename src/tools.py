import json
from apify import Actor
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(TAVILY_API_KEY)
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)

# Step 1: Extract the company's website from Tavily
def fetch_company_url(company_name: str) -> str:
    """Fetches the company's official website using Tavily."""
    
    query = f"Official website of {company_name}"
    Actor.log.info(f"Searching for company website: {query}")

    search_response = tavily_client.search(query=query, search_depth="basic", max_results=1)
    results = search_response.get("results", [])

    if results:
        website_url = results[0].get("url", "N/A")
        Actor.log.info(f"Found company website: {website_url}")
        return website_url

    Actor.log.warning(f"No official website found for {company_name}")
    return "N/A"

# Step 2: Extract initial company information
def fetch_initial_company_info(company_name: str, company_url: str) -> str:
    """Uses Tavily to fetch basic company information."""
    
    query = f"Basic company information for {company_name} from {company_url}"
    Actor.log.info(f"Fetching initial company details: {query}")

    search_response = tavily_client.search(query=query, search_depth="basic", max_results=3)
    documents = [result.get("content", "") for result in search_response.get("results", [])]

    if documents:
        initial_info = "\n\n".join(documents[:2])  # Take top 2 results
        Actor.log.info(f"Extracted initial company info: {initial_info[:200]}...")  # Log first 200 chars
        return initial_info

    Actor.log.warning(f"No initial company info found for {company_name}")
    return "N/A"

# Step 3: Generate research questions
question_generation_prompt = ChatPromptTemplate.from_template("""
    You are an expert researcher focusing on company analysis.
    Generate exactly 4 research questions about **{company}** to extract relevant insights.

    ### Key Areas:
    - **Background:** Founding year, mission, headquarters, CEO, employees.
    - **Products & Services:** Main offerings, features, customer segments.
    - **Market Position:** Competitors, market share, industry trends.
    - **Financials:** Revenue, funding, investors, growth trends.

    Company URL: {company_url}  
    Initial Information:  
    {initial_documents}
    
    Provide the response in a **valid JSON array format**.
""")

def generate_research_questions(company_name: str, company_url: str, initial_documents: str) -> list:
    """Generate research questions dynamically."""
    
    Actor.log.info(f"Generating research questions for {company_name}")

    response = question_generation_prompt | llm
    generated_response = response.invoke({
        "company": company_name,
        "company_url": company_url,
        "initial_documents": initial_documents
    }).content

    # Convert response to a JSON list of questions
    try:
        questions = json.loads(generated_response)
        if not isinstance(questions, list):
            raise ValueError("Expected a list of questions but got another format.")
    except json.JSONDecodeError:
        Actor.log.error("Failed to parse generated questions. Using fallback.")
        questions = generated_response.strip().split("\n")  # Split by lines as fallback

    questions = [q.strip() for q in questions if q.strip()]  # Ensure clean questions
    Actor.log.info(f"Generated research questions: {questions}")
    return questions

# Step 4: Perform research using generated questions
def research_company(company_name: str) -> dict:
    """Generates research questions and performs Tavily searches."""
    
    # Get company website
    company_url = fetch_company_url(company_name)
    
    # Get initial company information
    initial_documents = fetch_initial_company_info(company_name, company_url)
    
    # Generate research questions
    questions = generate_research_questions(company_name, company_url, initial_documents)

    search_results = []

    for question in questions:
        Actor.log.info(f"Searching Tavily for: {question}")  # Log each individual query
        try:
            response = tavily_client.search(
                query=question,  # Sending each question separately
                search_depth="basic",
                max_results=3
            )
            search_results.extend(response.get("results", []))  # Append results individually
        except Exception as e:
            Actor.log.error(f"Tavily API Error for query '{question}': {str(e)}")  # Log API errors

    return {
        "company_name": company_name,
        "company_url": company_url,
        "initial_documents": initial_documents,
        "research_findings": search_results
    }
