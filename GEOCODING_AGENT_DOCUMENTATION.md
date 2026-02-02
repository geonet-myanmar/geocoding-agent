# GeoAI Agent - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [What This Agent Does](#what-this-agent-does)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Understanding the Code](#understanding-the-code)
7. [Running the Agent](#running-the-agent)
8. [Usage Examples](#usage-examples)
9. [How to Extend](#how-to-extend)
10. [Troubleshooting](#troubleshooting)
11. [API Reference](#api-reference)
12. [Additional Resources](#additional-resources)

---

## Overview

The GeoAI Agent is an interactive conversational AI that can look up geographic coordinates for any location in the world. Built using the GitHub Copilot SDK and GeoPy library, it demonstrates how to create custom AI agents with specialized tools.

**Key Features:**
- Natural language geocoding queries
- Real-time coordinate lookups using OpenStreetMap data
- Persistent conversation context
- Custom tool integration with AI models
- Interactive command-line interface

---

## What This Agent Does

The GeoAI Agent combines the power of large language models with geographic information systems. It can:

1. **Understand natural queries** like "Where is Bangkok?" or "What are the coordinates of the Eiffel Tower?"
2. **Call geocoding tools** automatically when it needs location data
3. **Maintain conversation context** across multiple queries
4. **Provide formatted responses** with latitude and longitude information

### Example Interaction:
```
GeoNet Myanmar: Where is Yangon?
   [Tool] Fetching coordinates for: Yangon...
Agent: Yangon is located at Lat: 16.8661, Lon: 96.1951

GeoNet Myanmar: How far is that from Bangkok?
   [Tool] Fetching coordinates for: Bangkok...
Agent: Bangkok is located at Lat: 13.7563, Lon: 100.5018
The distance between Yangon and Bangkok is approximately 385 kilometers.
```

---

## Prerequisites

### Required Software
- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **GitHub Copilot CLI**: The underlying engine for the SDK
- **GitHub Account**: With active Copilot subscription

### Required Knowledge
- Basic Python programming
- Understanding of async/await patterns
- Familiarity with command-line interfaces
- Basic geography concepts

---

## Installation

### Step 1: Install GitHub Copilot CLI

First, install the GitHub Copilot CLI, which powers the SDK:

```bash
# Using npm (recommended)
npm install -g @github/copilot-cli

# Or using Homebrew (macOS/Linux)
brew install github-copilot-cli
```

Verify installation:
```bash
copilot --version
```

### Step 2: Authenticate with GitHub

```bash
copilot auth login
```

Follow the prompts to authenticate with your GitHub account.

### Step 3: Install Python Dependencies

Create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Install required packages:

```bash
pip install github-copilot-sdk geopy pydantic
```

### Step 4: Download the Agent Code

Save the `geocoding_agent.py` file to your project directory.

### Step 5: Verify Installation

Run a quick test:

```bash
python geocoding_agent.py
```

If everything is set up correctly, you should see:
```
Starting Copilot Client...
🌍 GeoAI Agent initialized (Model: GPT-5 mini).
   Type 'exit' or 'quit' to stop.
--------------------------------------------------
```

---

## Project Structure

```
demo/
├── geocoding_agent.py        # Main agent implementation
├── requirements.txt          # Python dependencies (optional)
└── README.md                 # This documentation
```

### Minimal requirements.txt

```txt
github-copilot-sdk>=0.1.0
geopy>=2.4.0
pydantic>=2.0.0
```

---

## Understanding the Code

### Architecture Overview

The agent is built with three main components:

```
┌─────────────────────────────────────────┐
│         User Input (CLI)                │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      CopilotClient (SDK)                │
│  - Manages AI model communication       │
│  - Routes tool calls                    │
│  - Maintains session context            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    get_coordinates Tool                 │
│  - Geocodes location names              │
│  - Returns lat/lon data                 │
│  - Uses Nominatim/OpenStreetMap         │
└─────────────────────────────────────────┘
```

### Code Walkthrough

#### Part 1: Import Dependencies (Lines 1-4)

```python
import asyncio
from copilot import CopilotClient, define_tool
from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field
```

- **asyncio**: Python's async/await framework for concurrent operations
- **CopilotClient**: Main SDK class for managing AI agent
- **define_tool**: Decorator to create custom tools for the AI
- **Nominatim**: Geocoding service from GeoPy using OpenStreetMap data
- **Pydantic**: Data validation library for defining tool input schemas

#### Part 2: Initialize Geocoder (Line 8)

```python
geolocator = Nominatim(user_agent="geoai_agent_interactive")
```

Creates a Nominatim geocoder instance. The `user_agent` parameter is required by OpenStreetMap's usage policy to identify your application.

#### Part 3: Define Tool Input Schema (Lines 11-15)

```python
class GetCoordinatesInput(BaseModel):
    place_name: str = Field(
        ...,
        description="The name of the city or place to locate (e.g., 'Bangkok', 'Eiffel Tower')."
    )
```

**Why Pydantic?**
- Automatic JSON schema generation
- Type validation at runtime
- Clear documentation for the AI model
- The AI uses the `description` field to understand when and how to use this parameter

**The `...` (Ellipsis)**: In Pydantic, this means the field is required.

#### Part 4: Implement Tool Handler (Lines 18-27)

```python
async def get_coordinates_impl(args: GetCoordinatesInput) -> str:
    print(f"\n   [Tool] Fetching coordinates for: {args.place_name}...")
    try:
        location = geolocator.geocode(args.place_name)
        if location:
            return f"{args.place_name} is located at Lat: {location.latitude}, Lon: {location.longitude}"
        else:
            return f"Could not find coordinates for {args.place_name}."
    except Exception as e:
        return f"Error finding location: {str(e)}"
```

**Key Points:**
- **async function**: Required by the SDK for non-blocking execution
- **args: GetCoordinatesInput**: Type-safe input validated by Pydantic
- **Returns string**: The AI model receives this as the tool result
- **Error handling**: Always return a string, even on errors

#### Part 5: Register the Tool (Lines 30-34)

```python
get_coords_tool = define_tool(
    name="get_coordinates",
    description="Get the latitude and longitude of a specific city or place name.",
    handler=get_coordinates_impl
)
```

**define_tool parameters:**
- **name**: Unique identifier for the tool (used internally)
- **description**: Tells the AI when to use this tool
- **handler**: The async function to execute

The AI model reads the `description` to decide when to call this tool.

#### Part 6: Main Agent Loop (Lines 38-83)

##### Initialize Client (Lines 39-43)

```python
async def main():
    client = CopilotClient()

    try:
        print("Starting Copilot Client...")
        await client.start()
```

Creates and starts the Copilot client, which launches the CLI process.

##### Create Session (Lines 46-50)

```python
session = await client.create_session({
    "model": "gpt-5-mini",
    "tools": [get_coords_tool],
    "system_message": "You are a GeoAI Assistant. Always use coordinates when discussing locations."
})
```

**Session Configuration:**
- **model**: The AI model to use (gpt-5-mini, claude-sonnet-4.5, etc.)
- **tools**: List of custom tools available to the AI
- **system_message**: Instructions that guide the AI's behavior

**Note**: The session maintains conversation context across multiple turns.

##### Interactive Loop (Lines 57-79)

```python
while True:
    try:
        user_input = input("\nGeoNet Myanmar: ")

        if user_input.strip().lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        if not user_input.strip():
            continue

        response = await session.send_and_wait({
            "prompt": user_input
        }, timeout=120)

        print(f"Agent: {response.data.content}")
```

**Flow:**
1. Get user input
2. Check for exit commands
3. Send to AI model via session
4. Wait for response (with 2-minute timeout)
5. Display AI's response

**session.send_and_wait()**: Convenience method that:
- Sends the prompt to the AI
- Waits for the AI to finish processing
- Returns the complete response

##### Cleanup (Lines 81-83)

```python
finally:
    print("Stopping client...")
    await client.stop()
```

Ensures the Copilot CLI process is properly terminated, even if errors occur.

---

## Running the Agent

### Basic Usage

```bash
python geocoding_agent.py
```

### Expected Output on Start

```
Starting Copilot Client...

🌍 GeoAI Agent initialized (Model: GPT-5 mini).
   Type 'exit' or 'quit' to stop.
--------------------------------------------------

GeoNet Myanmar:
```

### Exiting the Agent

Type either:
- `exit`
- `quit`
- Press `Ctrl+C` (keyboard interrupt)

---

## Usage Examples

### Example 1: Simple Location Query

```
GeoNet Myanmar: Where is Tokyo?

   [Tool] Fetching coordinates for: Tokyo...
Agent: Tokyo is located at Lat: 35.6762, Lon: 139.6503
```

### Example 2: Multiple Locations

```
GeoNet Myanmar: Tell me the coordinates of Paris and London

   [Tool] Fetching coordinates for: Paris...
   [Tool] Fetching coordinates for: London...
Agent: Paris is located at Lat: 48.8566, Lon: 2.3522
London is located at Lat: 51.5074, Lon: -0.1278
```

### Example 3: Contextual Follow-up

```
GeoNet Myanmar: Where is New York City?

   [Tool] Fetching coordinates for: New York City...
Agent: New York City is located at Lat: 40.7128, Lon: -74.0060

GeoNet Myanmar: What about Los Angeles?

   [Tool] Fetching coordinates for: Los Angeles...
Agent: Los Angeles is located at Lat: 34.0522, Lon: -118.2437
```

### Example 4: Landmarks and POIs

```
GeoNet Myanmar: Find the Statue of Liberty

   [Tool] Fetching coordinates for: Statue of Liberty...
Agent: Statue of Liberty is located at Lat: 40.6892, Lon: -74.0445
```

### Example 5: Location Not Found

```
GeoNet Myanmar: Where is Atlantis?

   [Tool] Fetching coordinates for: Atlantis...
Agent: I couldn't find coordinates for Atlantis as it's a mythical location.
```

---

## How to Extend

### 1. Add More Geocoding Tools

#### Distance Calculator Tool

```python
from geopy.distance import geodesic

class DistanceInput(BaseModel):
    location1: str = Field(description="First location name")
    location2: str = Field(description="Second location name")

async def calculate_distance_impl(args: DistanceInput) -> str:
    try:
        loc1 = geolocator.geocode(args.location1)
        loc2 = geolocator.geocode(args.location2)

        if not loc1 or not loc2:
            return "Could not find one or both locations."

        coords1 = (loc1.latitude, loc1.longitude)
        coords2 = (loc2.latitude, loc2.longitude)

        distance = geodesic(coords1, coords2).kilometers
        return f"Distance: {distance:.2f} km"
    except Exception as e:
        return f"Error: {str(e)}"

distance_tool = define_tool(
    name="calculate_distance",
    description="Calculate distance between two locations in kilometers.",
    handler=calculate_distance_impl
)

# Add to session tools
session = await client.create_session({
    "model": "gpt-5-mini",
    "tools": [get_coords_tool, distance_tool],
    "system_message": "You are a GeoAI Assistant..."
})
```

#### Reverse Geocoding Tool

```python
class ReverseGeocodeInput(BaseModel):
    latitude: float = Field(description="Latitude coordinate")
    longitude: float = Field(description="Longitude coordinate")

async def reverse_geocode_impl(args: ReverseGeocodeInput) -> str:
    try:
        location = geolocator.reverse(f"{args.latitude}, {args.longitude}")
        if location:
            return f"Location: {location.address}"
        else:
            return "No location found for these coordinates."
    except Exception as e:
        return f"Error: {str(e)}"

reverse_tool = define_tool(
    name="reverse_geocode",
    description="Get location name from latitude and longitude coordinates.",
    handler=reverse_geocode_impl
)
```

### 2. Switch AI Models

The code uses `gpt-5-mini`. You can change to other models:

```python
# Use Claude Sonnet
session = await client.create_session({
    "model": "claude-sonnet-4.5",
    "tools": [get_coords_tool],
    "system_message": "..."
})

# Use GPT-5
session = await client.create_session({
    "model": "gpt-5",
    "tools": [get_coords_tool],
    "system_message": "..."
})
```

**Available Models:**
- `gpt-5-mini` - Fast and cost-effective
- `gpt-5` - Most capable GPT model
- `claude-sonnet-4.5` - Balanced performance
- `claude-opus-4.5` - Most capable Claude model

Check available models at runtime:

```python
models = await client.get_models()
for model in models:
    print(f"- {model.name}")
```

### 3. Add Streaming Responses

For real-time token-by-token responses:

```python
session = await client.create_session({
    "model": "gpt-5-mini",
    "tools": [get_coords_tool],
    "system_message": "...",
    "streaming": True
})

# Handle streaming events
def on_event(event):
    if event.type.value == "assistant.message_delta":
        print(event.data.delta_content, end="", flush=True)
    elif event.type.value == "session.idle":
        print()  # New line after complete response

session.on(on_event)
await session.send({"prompt": user_input})
```

### 4. Add Web Search Capability

```python
from copilot import enable_web_search

session = await client.create_session({
    "model": "gpt-5-mini",
    "tools": [get_coords_tool],
    "system_message": "...",
    "web_search": True  # Enable web search
})
```

### 5. Integrate with Web Frameworks

#### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
client = None

@app.on_event("startup")
async def startup():
    global client
    client = CopilotClient()
    await client.start()

@app.on_event("shutdown")
async def shutdown():
    await client.stop()

class Query(BaseModel):
    message: str

@app.post("/geocode")
async def geocode(query: Query):
    session = await client.create_session({
        "model": "gpt-5-mini",
        "tools": [get_coords_tool]
    })

    response = await session.send_and_wait({
        "prompt": query.message
    })

    return {"response": response.data.content}
```

#### Flask Example

```python
from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)
client = None

@app.route('/geocode', methods=['POST'])
def geocode():
    data = request.json
    message = data.get('message')

    # Run async code in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def process():
        session = await client.create_session({
            "model": "gpt-5-mini",
            "tools": [get_coords_tool]
        })
        return await session.send_and_wait({"prompt": message})

    response = loop.run_until_complete(process())
    return jsonify({"response": response.data.content})
```

### 6. Add Logging and Analytics

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log tool calls
async def get_coordinates_impl(args: GetCoordinatesInput) -> str:
    logger.info(f"Tool called: get_coordinates({args.place_name})")
    start_time = datetime.now()

    try:
        location = geolocator.geocode(args.place_name)
        duration = (datetime.now() - start_time).total_seconds()

        if location:
            logger.info(f"Success: {args.place_name} -> {location.latitude}, {location.longitude} ({duration:.2f}s)")
            return f"{args.place_name} is located at Lat: {location.latitude}, Lon: {location.longitude}"
        else:
            logger.warning(f"Not found: {args.place_name} ({duration:.2f}s)")
            return f"Could not find coordinates for {args.place_name}."
    except Exception as e:
        logger.error(f"Error: {args.place_name} - {str(e)}")
        return f"Error finding location: {str(e)}"
```

### 7. Add Configuration File

Create `config.yaml`:

```yaml
model: "gpt-5-mini"
system_message: "You are a GeoAI Assistant."
geocoder:
  user_agent: "geoai_agent_interactive"
  timeout: 10
session:
  timeout: 120
  streaming: false
```

Load in code:

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

geolocator = Nominatim(
    user_agent=config['geocoder']['user_agent'],
    timeout=config['geocoder']['timeout']
)

session = await client.create_session({
    "model": config['model'],
    "tools": [get_coords_tool],
    "system_message": config['system_message'],
    "streaming": config['session']['streaming']
})
```

---

## Troubleshooting

### Common Issues

#### 1. "Copilot CLI not found"

**Error:**
```
Error: copilot command not found
```

**Solution:**
```bash
# Install Copilot CLI
npm install -g @github/copilot-cli

# Verify installation
copilot --version
```

#### 2. "Authentication failed"

**Error:**
```
Error: Not authenticated with GitHub
```

**Solution:**
```bash
copilot auth login
```

Make sure you have an active GitHub Copilot subscription.

#### 3. "Module not found: copilot"

**Error:**
```
ModuleNotFoundError: No module named 'copilot'
```

**Solution:**
```bash
pip install github-copilot-sdk
```

#### 4. "Geocoding service unavailable"

**Error:**
```
Error finding location: HTTPSConnectionPool...
```

**Solutions:**
- Check internet connection
- Verify OpenStreetMap/Nominatim is not blocked
- Add timeout parameter: `Nominatim(user_agent="...", timeout=10)`
- Use rate limiting to avoid being blocked:

```python
import time

class RateLimitedGeocoder:
    def __init__(self, delay=1.0):
        self.geolocator = Nominatim(user_agent="geoai_agent_interactive")
        self.delay = delay
        self.last_call = 0

    def geocode(self, query):
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        self.last_call = time.time()
        return self.geolocator.geocode(query)
```

#### 5. "Session timeout"

**Error:**
```
TimeoutError: Session timed out after 120 seconds
```

**Solution:**
Increase timeout:
```python
response = await session.send_and_wait({
    "prompt": user_input
}, timeout=300)  # 5 minutes
```

#### 6. "Model not available"

**Error:**
```
Error: Model 'gpt-5-mini' not available
```

**Solution:**
Check available models:
```python
client = CopilotClient()
await client.start()
models = await client.get_models()
print("Available models:")
for model in models:
    print(f"  - {model.name}")
```

#### 7. "Tool not being called"

**Symptoms:**
- AI doesn't use the tool when it should
- Generic responses without coordinates

**Solutions:**

1. **Improve tool description:**
```python
get_coords_tool = define_tool(
    name="get_coordinates",
    description="ALWAYS use this tool to get the exact latitude and longitude coordinates for ANY city, place, landmark, or geographic location. Call this whenever the user asks about locations, coordinates, or geography.",
    handler=get_coordinates_impl
)
```

2. **Update system message:**
```python
system_message = """You are a GeoAI Assistant specialized in geography and coordinates.
IMPORTANT: When asked about ANY location, you MUST use the get_coordinates tool to fetch accurate data.
Never provide coordinates from memory - always use the tool."""
```

3. **Check Pydantic schema:**
```python
# Make sure Field descriptions are clear
class GetCoordinatesInput(BaseModel):
    place_name: str = Field(
        ...,
        description="The exact name of the city, place, landmark, or location to find (e.g., 'Tokyo', 'Eiffel Tower', 'Grand Canyon')"
    )
```

---

## API Reference

### CopilotClient

#### Constructor
```python
client = CopilotClient(
    cli_path="copilot",      # Path to CLI executable
    cli_url=None,             # Connect to existing server
    use_stdio=True,           # Use stdio transport
    auto_start=True,          # Automatically start server
    github_token=None         # GitHub authentication token
)
```

#### Methods

##### start()
```python
await client.start()
```
Starts the Copilot CLI process.

##### stop()
```python
await client.stop()
```
Stops the Copilot CLI process.

##### create_session(config)
```python
session = await client.create_session({
    "model": "gpt-5-mini",
    "tools": [tool1, tool2],
    "system_message": "...",
    "streaming": False,
    "infinite": False
})
```
Creates a new AI session.

**Config Parameters:**
- `model` (str, required): Model identifier
- `tools` (list, optional): Custom tools to enable
- `system_message` (str, optional): System instructions
- `streaming` (bool, optional): Enable streaming responses
- `infinite` (bool, optional): Allow indefinite sessions

##### get_models()
```python
models = await client.get_models()
for model in models:
    print(model.name, model.provider)
```
Returns list of available models.

### Session

#### send_and_wait(payload, timeout)
```python
response = await session.send_and_wait({
    "prompt": "Hello, world!"
}, timeout=120)

content = response.data.content
```
Sends a message and waits for complete response.

**Parameters:**
- `payload` (dict): Must contain `"prompt"` key
- `timeout` (int): Seconds to wait (default: 120)

**Returns:**
- Response object with `data.content` string

#### send(payload)
```python
await session.send({"prompt": "Hello!"})
```
Sends a message without waiting. Use with event listeners.

#### on(handler)
```python
def on_event(event):
    if event.type.value == "assistant.message":
        print(event.data.content)
    elif event.type.value == "session.idle":
        print("Done!")

session.on(on_event)
```
Registers event handler.

**Event Types:**
- `assistant.message` - Complete response received
- `assistant.message_delta` - Streaming chunk received
- `session.idle` - Session finished processing
- `tool.call` - Tool is being invoked
- `tool.result` - Tool execution completed

### define_tool

```python
tool = define_tool(
    name="tool_name",
    description="What this tool does",
    handler=async_function
)
```

**Parameters:**
- `name` (str): Unique identifier
- `description` (str): When to use this tool (shown to AI)
- `handler` (async function): Implementation

**Handler Signature:**
```python
async def handler(args: PydanticModel) -> str:
    # Your implementation
    return "result string"
```

### Geocoding with GeoPy

#### Nominatim Geocoder

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(
    user_agent="my_app_name",
    timeout=10
)

# Forward geocoding
location = geolocator.geocode("New York City")
print(location.latitude, location.longitude)
print(location.address)

# Reverse geocoding
location = geolocator.reverse("40.7128, -74.0060")
print(location.address)
```

#### Distance Calculation

```python
from geopy.distance import geodesic

coords1 = (40.7128, -74.0060)  # New York
coords2 = (34.0522, -118.2437)  # Los Angeles

distance = geodesic(coords1, coords2).kilometers
print(f"Distance: {distance:.2f} km")
```

---

## Additional Resources

### Official Documentation

- **GitHub Copilot SDK**: https://github.com/github/copilot-sdk
- **Python SDK**: https://github.com/github/copilot-sdk/tree/main/python
- **GeoPy Documentation**: https://geopy.readthedocs.io/
- **Pydantic Documentation**: https://docs.pydantic.dev/

### Learning Resources

- **Async Python Tutorial**: https://realpython.com/async-io-python/
- **Pydantic Tutorial**: https://docs.pydantic.dev/latest/concepts/models/
- **OpenStreetMap Nominatim**: https://nominatim.org/
- **GitHub Copilot**: https://github.com/features/copilot

### Example Projects

Explore more Copilot SDK examples:
```bash
git clone https://github.com/github/copilot-sdk.git
cd copilot-sdk/python/examples
```

### Community

- **GitHub Discussions**: https://github.com/github/copilot-sdk/discussions
- **Issue Tracker**: https://github.com/github/copilot-sdk/issues

### Alternative Geocoding Services

If Nominatim doesn't meet your needs, GeoPy supports other services:

```python
# Google Maps (requires API key)
from geopy.geocoders import GoogleV3
geolocator = GoogleV3(api_key="YOUR_API_KEY")

# Bing Maps (requires API key)
from geopy.geocoders import Bing
geolocator = Bing(api_key="YOUR_API_KEY")

# MapBox (requires API key)
from geopy.geocoders import MapBox
geolocator = MapBox(api_key="YOUR_API_KEY")
```

### Performance Tips

1. **Cache geocoding results:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def geocode_cached(place_name):
    return geolocator.geocode(place_name)
```

2. **Use async geocoding with multiple queries:**
```python
import aiohttp
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter

async with Nominatim(
    user_agent="my_app",
    adapter_factory=AioHTTPAdapter,
) as geolocator:
    location = await geolocator.geocode("New York City")
```

3. **Batch processing:**
```python
locations = ["Paris", "London", "Tokyo", "Sydney"]
results = []

for loc in locations:
    time.sleep(1)  # Respect rate limits
    result = geolocator.geocode(loc)
    results.append((loc, result))
```

---

## Next Steps

Now that you understand how the GeoAI Agent works, try:

1. **Experiment with different models** to see performance differences
2. **Add new tools** like weather lookups or timezone conversions
3. **Integrate with a web app** using FastAPI or Flask
4. **Build a GUI** using Tkinter, PyQt, or web technologies
5. **Deploy as a service** using Docker and cloud platforms

### Example Enhancement: Weather Integration

Combine geocoding with weather data:

```python
import aiohttp

class WeatherInput(BaseModel):
    place_name: str = Field(description="Location for weather lookup")

async def get_weather_impl(args: WeatherInput) -> str:
    # First geocode the location
    location = geolocator.geocode(args.place_name)
    if not location:
        return f"Could not find {args.place_name}"

    # Then get weather (example with Open-Meteo API)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current_weather=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            weather = data['current_weather']
            return f"Weather in {args.place_name}: {weather['temperature']}°C, Wind: {weather['windspeed']} km/h"

weather_tool = define_tool(
    name="get_weather",
    description="Get current weather for a location",
    handler=get_weather_impl
)
```

---

## License and Attribution

This project uses:
- **GitHub Copilot SDK**: MIT License
- **GeoPy**: MIT License
- **Pydantic**: MIT License
- **OpenStreetMap Data**: ODbL License

When using OpenStreetMap/Nominatim data, please include attribution:
```
© OpenStreetMap contributors
```

---

## Conclusion

You now have a complete understanding of how to build, run, and extend the GeoAI Agent. This architecture can be adapted for many different use cases:

- Customer service bots with database tools
- Code analysis agents with GitHub API tools
- Data science assistants with pandas/numpy tools
- DevOps agents with Docker/Kubernetes tools

The key is defining clear, focused tools with good descriptions and letting the AI model orchestrate them intelligently.

Happy building!
