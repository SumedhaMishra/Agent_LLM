# Agent Skills & Behaviors

## Weather Skill

When a user asks about the weather:

1. **If location is NOT provided:**
   - Ask the user: "Which location would you like the weather for?"
   - Wait for the user to provide a location before proceeding

2. **If location IS provided:**
   - Use `web_search` to find current weather for that location
   - Search query format: "current weather in [location]"
   - Provide temperature, conditions, and any relevant weather alerts

### Example Interactions

**User:** "What's the weather like?"  
**Agent:** "Which location would you like the weather for?"  
**User:** "Seattle"  
**Agent:** *searches and provides Seattle weather*

**User:** "What's the weather in Tokyo?"  
**Agent:** *searches and provides Tokyo weather directly*

### Keywords that trigger this skill:
- weather
- temperature
- forecast
- rain
- sunny
- cloudy
- snow
- humidity
