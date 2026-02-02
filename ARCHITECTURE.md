# GeoAI Agent Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                │
│                  (Command Line Interface)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Natural Language Query
                        │ "Where is Bangkok?"
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Python Application                       │
│                  (geocoding_agent.py)                       │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │            Main Event Loop                        │    │
│  │  - Receives user input                            │    │
│  │  - Sends to AI session                            │    │
│  │  - Displays responses                             │    │
│  └───────────────────┬───────────────────────────────┘    │
│                      │                                      │
└──────────────────────┼──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Copilot SDK (Python)                    │
│                                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │          CopilotClient                           │     │
│  │  - Manages CLI process lifecycle                 │     │
│  │  - Handles JSON-RPC communication                │     │
│  └──────────────────┬───────────────────────────────┘     │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────┐     │
│  │          Session Manager                         │     │
│  │  - Maintains conversation context                │     │
│  │  - Routes messages to AI model                   │     │
│  │  - Manages tool calls                            │     │
│  └──────────────────┬───────────────────────────────┘     │
│                     │                                       │
└─────────────────────┼───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────────┐      ┌───────────────────┐
│   AI Model        │      │  Custom Tools     │
│   (GPT/Claude)    │      │                   │
│                   │      │  ┌─────────────┐  │
│ - Understands     │◄─────┤  │get_coords   │  │
│   natural language│      │  │             │  │
│ - Decides when to │      │  │handler:     │  │
│   use tools       │──────┤  │async func   │  │
│ - Formats         │      │  └──────┬──────┘  │
│   responses       │      │         │         │
└───────────────────┘      └─────────┼─────────┘
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │   GeoPy Library     │
                           │                     │
                           │  ┌──────────────┐   │
                           │  │  Nominatim   │   │
                           │  │  Geocoder    │   │
                           │  └──────┬───────┘   │
                           │         │           │
                           └─────────┼───────────┘
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │  OpenStreetMap API  │
                           │  (Nominatim)        │
                           │                     │
                           │  Returns:           │
                           │  - Latitude         │
                           │  - Longitude        │
                           │  - Address          │
                           └─────────────────────┘
```

## Data Flow

### Request Flow (User → AI → Tool → Response)

```
1. User Input
   │
   │ "Where is Bangkok?"
   │
   ▼
2. Python Event Loop
   │
   │ input() → user_input
   │
   ▼
3. Session Send
   │
   │ session.send_and_wait({"prompt": user_input})
   │
   ▼
4. Copilot SDK
   │
   │ JSON-RPC to Copilot CLI
   │
   ▼
5. AI Model Processing
   │
   ├─► Analyzes: "User wants location coordinates"
   ├─► Checks available tools
   └─► Decides: "Use get_coordinates tool"
   │
   ▼
6. Tool Call Request
   │
   │ {
   │   "tool": "get_coordinates",
   │   "args": {"place_name": "Bangkok"}
   │ }
   │
   ▼
7. Python Handler Execution
   │
   │ get_coordinates_impl(args)
   │
   ▼
8. GeoPy Geocoding
   │
   │ geolocator.geocode("Bangkok")
   │
   ▼
9. OpenStreetMap API
   │
   │ HTTP Request to Nominatim
   │
   ▼
10. API Response
   │
   │ {
   │   "lat": 13.7563,
   │   "lon": 100.5018,
   │   "display_name": "Bangkok, Thailand"
   │ }
   │
   ▼
11. Tool Return Value
   │
   │ "Bangkok is located at Lat: 13.7563, Lon: 100.5018"
   │
   ▼
12. AI Model Formatting
   │
   │ Receives tool result
   │ Formats final response
   │
   ▼
13. Response to User
   │
   │ "Bangkok is located at Lat: 13.7563, Lon: 100.5018"
   │
   ▼
14. Display to User

    Agent: Bangkok is located at Lat: 13.7563, Lon: 100.5018
```

## Component Details

### 1. User Interface Layer

**File**: `geocoding_agent.py` (lines 57-79)

**Responsibilities**:
- Capture user input via CLI
- Display AI responses
- Handle exit commands
- Manage keyboard interrupts

**Key Code**:
```python
user_input = input("\nGeoNet Myanmar: ")
response = await session.send_and_wait({"prompt": user_input})
print(f"Agent: {response.data.content}")
```

### 2. Application Layer

**File**: `geocoding_agent.py` (lines 38-83)

**Responsibilities**:
- Initialize Copilot client
- Create and configure AI session
- Manage application lifecycle
- Error handling and cleanup

**Key Code**:
```python
client = CopilotClient()
await client.start()

session = await client.create_session({
    "model": "gpt-5-mini",
    "tools": [get_coords_tool],
    "system_message": "..."
})
```

### 3. SDK Layer (GitHub Copilot SDK)

**Package**: `github-copilot-sdk`

**Components**:
- **CopilotClient**: Manages CLI process
- **Session**: Handles conversation context
- **JSON-RPC Bridge**: Communicates with CLI

**Communication Protocol**:
```json
// Request
{
  "method": "session.send",
  "params": {
    "prompt": "Where is Bangkok?",
    "session_id": "abc123"
  }
}

// Response
{
  "type": "assistant.message",
  "data": {
    "content": "Bangkok is located at..."
  }
}
```

### 4. AI Model Layer

**Models Supported**:
- GPT-5-mini (fast, cost-effective)
- GPT-5 (most capable)
- Claude Sonnet 4.5 (balanced)
- Claude Opus 4.5 (most capable)

**Responsibilities**:
- Natural language understanding
- Tool selection and calling
- Response generation
- Context management

**Decision Process**:
```
1. Parse user intent
   "Where is Bangkok?" → Need location coordinates

2. Check available tools
   - get_coordinates: "Get lat/lon of a place" ✓ MATCH

3. Extract parameters
   place_name = "Bangkok"

4. Call tool
   get_coordinates({"place_name": "Bangkok"})

5. Receive result
   "Bangkok is located at Lat: 13.7563, Lon: 100.5018"

6. Format response
   Return to user with context
```

### 5. Tool Layer

**File**: `geocoding_agent.py` (lines 11-34)

**Components**:
1. **Input Schema** (Pydantic Model)
2. **Handler Function** (Async implementation)
3. **Tool Definition** (SDK registration)

**Structure**:
```python
# 1. Schema
class GetCoordinatesInput(BaseModel):
    place_name: str = Field(...)

# 2. Handler
async def get_coordinates_impl(args: GetCoordinatesInput) -> str:
    return geocoding_result

# 3. Definition
tool = define_tool(
    name="get_coordinates",
    description="...",
    handler=get_coordinates_impl
)
```

### 6. Geocoding Layer (GeoPy)

**Package**: `geopy`

**Components**:
- **Nominatim**: OpenStreetMap geocoder
- **Location Objects**: Results with lat/lon
- **Distance Calculator**: For extended version

**Capabilities**:
```python
# Forward geocoding
location = geolocator.geocode("Bangkok")
# → Location(latitude=13.7563, longitude=100.5018, ...)

# Reverse geocoding
location = geolocator.reverse("13.7563, 100.5018")
# → Location(address="Bangkok, Thailand", ...)

# Distance calculation
distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
```

### 7. External API Layer

**Service**: OpenStreetMap Nominatim

**Endpoint**: `https://nominatim.openstreetmap.org/search`

**Rate Limits**:
- 1 request per second
- Requires User-Agent header

**Response Format**:
```json
{
  "lat": "13.7563",
  "lon": "100.5018",
  "display_name": "Bangkok, Thailand",
  "type": "city",
  "importance": 0.9
}
```

## Conversation State Management

### Session Context

The SDK maintains conversation history:

```
Turn 1:
  User: "Where is Bangkok?"
  AI: "Bangkok is at Lat: 13.7563, Lon: 100.5018"
  ↓
  [Stored in session]

Turn 2:
  User: "How far is that from Paris?"
  AI: [Has context: "that" = Bangkok]
      [Calls: get_coordinates("Paris")]
      [Calculates distance using previous Bangkok coords]
  ↓
  Response: "Paris is 9,442 km from Bangkok"
```

### Context Window

- Model-dependent (typically 128k tokens for GPT-5)
- Includes: User messages, AI responses, tool calls, tool results
- Automatically managed by SDK

## Error Handling Architecture

```
Error Source          Handler Location       Strategy
─────────────────────────────────────────────────────────
User Input (empty)    → Event Loop          → Skip, continue
User Input (exit)     → Event Loop          → Break loop
Keyboard Interrupt    → Event Loop          → Graceful exit

Network Error         → Tool Handler        → Return error string
Location Not Found    → Tool Handler        → Return "not found" string
API Timeout           → Tool Handler        → Return timeout message

Session Timeout       → Session Layer       → Raise TimeoutError
Model Error           → SDK Layer           → Propagate exception

Unhandled Exception   → Finally Block       → Cleanup client
```

## Performance Characteristics

### Latency Breakdown

```
Component                    Typical Time
─────────────────────────────────────────
User input                   0ms (blocking)
JSON-RPC overhead            10-50ms
AI model inference           500-2000ms
Tool execution               200-1000ms
  ├─ Geocoding API call      150-800ms
  └─ Python processing       50-200ms
Response formatting          100-300ms
─────────────────────────────────────────
Total (simple query)         1-4 seconds
```

### Resource Usage

```
Component                Memory        CPU
──────────────────────────────────────────
Python process           ~50MB         Low
Copilot CLI process      ~100MB        Low
AI model (remote)        N/A           N/A
──────────────────────────────────────────
Total                    ~150MB        Low
```

## Security Architecture

### Authentication Flow

```
1. User runs: copilot auth login
   ↓
2. Browser opens → GitHub OAuth
   ↓
3. Token stored in ~/.copilot/config
   ↓
4. SDK reads token automatically
   ↓
5. CLI authenticates API requests
```

### Data Privacy

- **Local Processing**: Tool execution happens locally
- **Remote Processing**: AI inference happens on GitHub servers
- **No Storage**: Conversations not stored by default
- **API Calls**: Geocoding calls to OpenStreetMap (public service)

## Extensibility Points

### 1. Add New Tools

```python
new_tool = define_tool(
    name="tool_name",
    description="...",
    handler=async_function
)

session = await client.create_session({
    "tools": [get_coords_tool, new_tool]  # Add here
})
```

### 2. Change AI Model

```python
session = await client.create_session({
    "model": "claude-sonnet-4.5"  # Change here
})
```

### 3. Add Middleware

```python
def on_tool_call(event):
    print(f"Tool called: {event.tool_name}")

def on_tool_result(event):
    print(f"Tool result: {event.result}")

session.on("tool.call", on_tool_call)
session.on("tool.result", on_tool_result)
```

### 4. Custom Geocoding Service

```python
from geopy.geocoders import GoogleV3

geolocator = GoogleV3(api_key="YOUR_KEY")
# Same interface, different backend
```

## Deployment Options

### 1. CLI Application (Current)
- Direct user interaction
- Best for: Personal use, testing

### 2. Web Service
- FastAPI/Flask wrapper
- Best for: API endpoints, web apps

### 3. Chatbot Integration
- Slack/Discord/Teams
- Best for: Team collaboration

### 4. Desktop GUI
- Tkinter/PyQt wrapper
- Best for: Non-technical users

### 5. Mobile Backend
- REST API server
- Best for: Mobile app backend

## Testing Strategy

### Unit Tests
```python
# Test tool handler
async def test_get_coordinates():
    args = GetCoordinatesInput(place_name="Bangkok")
    result = await get_coordinates_impl(args)
    assert "13.7563" in result
```

### Integration Tests
```python
# Test full flow
async def test_full_session():
    client = CopilotClient()
    await client.start()
    session = await client.create_session({...})
    response = await session.send_and_wait({
        "prompt": "Where is Bangkok?"
    })
    assert "coordinates" in response.data.content.lower()
```

### Mocking External Services
```python
from unittest.mock import patch

@patch('geopy.geocoders.Nominatim.geocode')
async def test_with_mock(mock_geocode):
    mock_geocode.return_value = MockLocation(13.7563, 100.5018)
    # Test without real API calls
```

## Monitoring and Logging

### Recommended Logging Points

```python
import logging

logger = logging.getLogger(__name__)

# 1. Application lifecycle
logger.info("Client started")
logger.info("Session created")

# 2. User interactions
logger.info(f"User query: {user_input}")

# 3. Tool calls
logger.info(f"Tool called: {tool_name}({args})")

# 4. External API calls
logger.info(f"Geocoding: {place_name}")

# 5. Errors
logger.error(f"Error: {exception}")
```

### Metrics to Track

- Queries per session
- Tool call success rate
- Average response time
- Error frequency
- Most queried locations

## Conclusion

This architecture demonstrates a clean separation of concerns:

1. **UI Layer**: Simple input/output
2. **Application Layer**: Lifecycle management
3. **SDK Layer**: AI orchestration
4. **Tool Layer**: Custom functionality
5. **Service Layer**: External APIs

The design is modular, testable, and easy to extend for new use cases.
