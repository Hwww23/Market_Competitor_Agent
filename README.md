# Competitor Intelligence Agent

When researching the market, you want to know what the market has yet to offer. 
This agent takes a list of companies, researches them and their competitors using 
real-time web data, and produces structured intelligence reports automatically.

## Architecture
```
User Input → Tavily (web search) → Ollama (LLM reasoning) → JSON Reports + Markdown
```

## Setup

### Local
```powershell
pip install -r requirements.txt
cp .env.example .env  # add your TAVILY_API_KEY
python agent.py
```

### Docker
```powershell
docker run -it `
  -e TAVILY_API_KEY=your_key `
  -e OLLAMA_URL=http://host.docker.internal:11434/api/chat `
  -v "${PWD}/reports:/app/reports" `
  competitor-agent
```

## Example Output
```json
{
  "company_name": "Spotify",
  "core_product": "Music streaming platform",
  "pricing_model": "Freemium",
  "perceived_strength": "Market leader with 751M users",
  "perceived_weakness": "Frequent price increases"
}
```

## Known Limitations
- Similarly named companies (e.g. "Firefox" vs "Mozilla Firefox") may 
  appear as duplicates. Future fix: fuzzy string matching + LLM verification.
- LLM output is non-deterministic — results may vary between runs.
- Requires Ollama running locally for LLM inference.