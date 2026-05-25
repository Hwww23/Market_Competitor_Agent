import requests
import json
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime

# Competitor Intelligence Agent
# Takes a company name, searches the web for real data,
# and returns a structured JSON analysis using a local LLM.
load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

url = "http://localhost:11434/api/chat"

company = input("Enter competitor name: ")

results = tavily.search(f"{company} pricing features competitors 2026")

search_context = "\n\n".join(
    f"""
    Title: {r['title']}
    URL: {r['url']}
    Content: {r['content']}
    """
        for r in results['results']
    )

prompt = f"""
Based on the following real web data about {company}:

{search_context}

Return ONLY a JSON object with these fields:
company_name, core_product, pricing_model, perceived_strength, perceived_weakness.
If unsure, use 'Unknown'. No text outside the JSON.
"""

payload = {
    "model": "gemma4:e4b",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "stream": False
}

response = requests.post(url, json=payload)
content = response.json()['message']['content']
content = content.replace("```json", "").replace("```", "").strip()
data = json.loads(content)
print(content)

today = datetime.now().strftime("%Y-%m-%d_%H-%M")

os.makedirs("reports", exist_ok=True)
with open(f"reports/{company}_{today}.json", "w") as f:
    json.dump(data, f, indent=2)