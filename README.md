# 🏢 AI Company Researcher  

🚀 **AI Company Researcher** is an **Apify Actor** that **automates company research** using **Tavily Search API** and **AI-powered insights**.  

It gathers **company details, financials, products, leadership insights, and recent developments**, then compiles a **structured Markdown report** with **inline citations**.  

---

## 🏆 **Features**  
✔ **Automated Company Research** using Tavily search  
✔ **AI-Generated Research Questions** for deep insights  
✔ **Financial & Product Analysis** from reliable sources  
✔ **Leadership & Market Position Insights**  
✔ **Markdown Reports with Citations** stored in Apify  

---

## 🚀 **How It Works**  
1️⃣ **Extracts Company Website** – Uses Tavily to find the **official URL**.  
2️⃣ **Fetches Initial Info** – Scrapes basic company details.  
3️⃣ **Generates Research Questions** – AI creates **focused queries**.  
4️⃣ **Performs Tavily Search** – Finds **relevant articles** & sources.  
5️⃣ **Compiles AI-Powered Report** – LLM formats research into **structured Markdown**.  
6️⃣ **Stores Report in Apify** – Report is saved to **Apify Key-Value Store**.  

---

## 📦 **Installation & Setup**  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/bala-ceg/ai-companyresearcher.git
cd ai-companyresearcher
```

### 2️⃣ Create a Virtual Environment (Optional)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Keys
Create a `.env` file and add your API keys:
```ini
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
```

---

## 🎯 **How to Run Locally**
```bash
apify run --input-file=input.json
```
📜 **Example `input.json`**
```json
{
    "company_name": "OpenAI"
}
```

---
```
ai-companyresearcher/
│── src/
│   ├── main.py        # Apify Actor entry point
│   ├── tools.py       # Tavily search & research logic
│   ├── models.py      # Pydantic models for structured data
│   ├── report.md      # AI-generated company research report
│── .venv/             # Virtual environment (optional)
│── requirements.txt   # Python dependencies
│── README.md          # Project documentation
│── input.json         # Example input format
│── .env               # API keys (gitignore this file)

```
---

## 📝 AI-Generated Report
### Executive Summary

OpenAI, an American artificial intelligence (AI) research organization, consists of two entities: OpenAI Inc., a nonprofit research segment, and OpenAI Global LLC, a for-profit subsidiary focused on commercializing AI technologies ([Britannica Money](https://www.britannica.com/money/OpenAI)). Established in December 2015, OpenAI's primary goal is to advance artificial general intelligence (AGI) to enable machines to learn, understand, and apply intelligence across various domains akin to human capabilities. Noteworthy achievements include developing ChatGPT, one of the most advanced AI models for processing language and generating human-like text.

### Leadership and Vision

The CEO of OpenAI is Sam Altman, a well-known figure in the tech industry ([Britannica Money](https://www.britannica.com/money/OpenAI)). Altman, along with the key team members, brings a wealth of experience in AI research and strategic leadership. Recent developments include the addition of new members to the Board of Directors, such as Dr. Sue Desmond-Hellmann, Nicole Seligman, and Fidji Simo, as part of the company's expansion plans ([OpenAI](https://openai.com/index/openai-announces-new-members-to-board-of-directors)).

### Product and Service Overview

OpenAI's flagship platform, ChatGPT, powered by advanced AI models, offers state-of-the-art solutions for language processing and text generation ([Britannica Money](https://www.britannica.com/money/OpenAI)). Targeting a wide range of customers, OpenAI aims to address complex business challenges with innovative AI-driven analytics and natural language processing tools. Despite facing competition from companies like Cohere and Baidu AI ([Business Model Analyst](https://businessmodelanalyst.com/openai-competitors/)), OpenAI remains a leader in AI research and development.

### Financial Performance

In terms of financial performance, OpenAI has seen substantial growth, with estimated annual revenue surpassing $5 billion ([Tanay Jaipuria](https://www.tanayj.com/p/openai-and-anthropic-revenue-breakdown)). ChatGPT alone is projected to contribute approximately $2.7 billion to OpenAI's revenue by the end of the year, highlighting the company's strong market position and revenue streams. The company's API revenue plays a significant role in its overall financial success.

### Recent Developments

Recent developments at OpenAI include strategic partnerships, product updates, and market strategies to further enhance its AI offerings. The company's focus on innovation and technological advancements continues to drive its success in the competitive AI landscape. Notable collaborations and initiatives demonstrate OpenAI's commitment to staying at the forefront of AI research and development.

### Citations

- [OpenAI | ChatGPT, Sam Altman, Microsoft, & History | Britannica Money](https://www.britannica.com/money/OpenAI)
- [OpenAI announces new members to board of directors](https://openai.com/index/openai-announces-new-members-to-board-of-directors/)
- [Top 10 OpenAI Competitors and Alternatives (2025)](https://businessmodelanalyst.com/openai-competitors/)
- [OpenAI and Anthropic Revenue Breakdown - by Tanay Jaipuria](https://www.tanayj.com/p/openai-and-anthropic-revenue-breakdown)

---


## 🚀 **Contributing**
We welcome contributions! Feel free to:
- **Open Issues** for bug reports or feature requests.
- **Submit Pull Requests** to improve the code.

---