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

url = os.getenv("OLLAMA_URL")

companies = [company.strip() for company in input("Enter competitors (comma separated): ").split(",")]

os.makedirs("reports", exist_ok=True)

seen = set()
all_results = [] 

for company in companies:
    print(f"\nAnalysing {company}...")
    try:
        results = tavily.search(f"{company} top competitors alternative products comparison 2026")
    except Exception as e:
        print(f"Error during search: {e}")
        exit(1)

    search_context = "\n\n".join(
        f"""
        Title: {r['title']}
        URL: {r['url']}
        Content: {r['content']}
        """
            for r in results['results']
        )

    prompt = f"""
    Based on the following real web data about {company} and its competitors:

    {search_context}

    Identify {company} and its top 3 competitors from the data.
    Return ONLY a JSON array like this:
    [
        {{
            "company_name": "string",
            "core_product": "string", 
            "pricing_model": "string",
            "perceived_strength": "string",
            "perceived_weakness": "string"
        }}
    ]
    The first entry should be {company} itself, followed by its competitors.
    Always use the official product name, not the parent company name.
    Use 'Mozilla Firefox' not 'Firefox' or 'Mozilla'.
    Use 'Google Chrome' not 'Chrome' or 'Google'.
    Use 'Microsoft Edge' not 'Edge' or 'Microsoft'.
    No text outside the JSON array.
    """

    payload = {
        "model": "gemma4:e4b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        content = response.json()['message']['content']
    except Exception as e:
        print(f"Error during LLM processing: {e}")
        exit(1)

    try:
        content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        print(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        exit(1)

    today = datetime.now().strftime("%Y-%m-%d_%H-%M")
    with open(f"reports/{company}_{today}.json", "w") as f:
        json.dump(data, f, indent=2)

    all_results.extend(data)
    print(f"✓ {company} done")

report = f"# Competitor Analysis Report\n"
report += f"Generated: {today}\n\n"

for company_data in all_results:
    name = company_data['company_name']
    if name not in seen:
        seen.add(name)
        report += f"## {company_data['company_name']}\n"
        report += f"**Product:** {company_data['core_product']}\n\n"
        report += f"**Pricing:** {company_data['pricing_model']}\n\n"
        report += f"**Strength:** {company_data['perceived_strength']}\n\n"
        report += f"**Weakness:** {company_data['perceived_weakness']}\n\n"
        report += "---\n\n"

with open(f"reports/combined_report_{today}.md", "w") as f:
    f.write(report)

print(f"\n✓ Combined report saved to reports/combined_report_{today}.md")