# Agent Skills & Behaviors

## General Output Rules

When presenting ANY search results or multiple items:
- **ALWAYS use a TABLE format**
- **Do NOT include URLs or links in your responses**
- Table format: | # | Title/Headline | Summary/Details |

---

## Weather & Temperature Skill

When a user asks about weather or temperature:

1. **If location is NOT provided:**
   - Ask the user: "Which location would you like the weather for?"
   - Wait for the user to provide a location before proceeding
   - Do NOT search until you have a location

2. **If location IS provided:**
   - Use the `web_search` tool to find current weather for that location
   - Search query format: "current weather in [location]"
   - Extract and present: temperature, conditions, humidity, and any weather alerts
   - Provide the information in a clear, readable format

### Example Interactions

**User:** "What's the weather like?"  
**Agent:** "Which location would you like the weather for?"  
**User:** "Seattle"  
**Agent:** *uses web_search("current weather in Seattle")* → provides Seattle weather

**User:** "What's the temperature?"  
**Agent:** "Which location would you like the temperature for?"  
**User:** "New York"  
**Agent:** *uses web_search("current temperature in New York")* → provides temperature

**User:** "What's the weather in Tokyo?"  
**Agent:** *uses web_search("current weather in Tokyo")* → provides Tokyo weather directly

**User:** "How hot is it in Miami?"  
**Agent:** *uses web_search("current temperature in Miami")* → provides Miami temperature directly

### Keywords that trigger this skill:
- weather
- temperature
- forecast
- rain
- sunny
- cloudy
- snow
- humidity
- hot
- cold
- warm
- degrees

---

## News & Current Affairs Skill

When a user asks about news or what happened recently:

1. **If timeframe is specified (this week, last week, today, etc.):**
   - Use `web_search` to find recent news for that timeframe
   - **IMPORTANT:** Always include the current month and year (March 2026) in your search
   - Search query format: "news March 2026" or "what happened this week March 2026"
   - **Present results in a TABLE format** (do NOT include URLs/links)
   - Table columns: | # | Headline | Summary |
   - Summarize 3-5 stories concisely

2. **If topic is specified:**
   - Use `web_search` to find news about that specific topic
   - Search query format: "[topic] news March 2026"
   - Present in table format

3. **If neither timeframe nor topic is specified:**
   - Ask: "Would you like news from this week, or about a specific topic?"

### Output Format

Always present news in this table format:

| # | Headline | Summary |
|---|----------|----------|
| 1 | [News Title] | [Brief 1-2 sentence summary] |
| 2 | [News Title] | [Brief 1-2 sentence summary] |
| 3 | [News Title] | [Brief 1-2 sentence summary] |

**Do NOT include URLs or links in the output.**

### Example Interactions

**User:** "What happened this week?"  
**Agent:** *uses web_search("top news this week March 2026")* → presents table of news

**User:** "Any news about AI?"  
**Agent:** *uses web_search("AI news March 2026")* → presents table of AI news

### Keywords that trigger this skill:
- news
- current affairs
- what happened
- this week
- last week
- today
- headlines
- events
- updates
- recent
