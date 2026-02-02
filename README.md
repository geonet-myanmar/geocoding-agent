# GeoAI Agent

An interactive AI-powered geocoding assistant built with the GitHub Copilot SDK and GeoPy. Ask natural language questions about locations and get precise geographic coordinates.

## Quick Demo

```
GeoNet Myanmar: Where is Bangkok?
   [Tool] Fetching coordinates for: Bangkok...
Agent: Bangkok is located at Lat: 13.7563, Lon: 100.5018

GeoNet Myanmar: What about the Eiffel Tower?
   [Tool] Fetching coordinates for: Eiffel Tower...
Agent: Eiffel Tower is located at Lat: 48.8584, Lon: 2.2945
```

## Features

- **Natural Language Queries**: Ask about locations in plain English
- **Real-time Geocoding**: Powered by OpenStreetMap's Nominatim service
- **Persistent Context**: Maintains conversation history across queries
- **Custom AI Tools**: Demonstrates tool integration with language models
- **Extensible Architecture**: Easy to add new capabilities

## Quick Start

1. **Install GitHub Copilot CLI**
   ```bash
   npm install -g @github/copilot-cli
   copilot auth login
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Agent**
   ```bash
   python geocoding_agent.py
   ```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## Documentation

- **[Complete Documentation](GEOCODING_AGENT_DOCUMENTATION.md)** - Comprehensive guide covering:
  - Architecture and code walkthrough
  - Installation and setup
  - Usage examples
  - Extension tutorials
  - Troubleshooting
  - API reference

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes

## Project Files

```
demo/
├── geocoding_agent.py              # Basic geocoding agent
├── geocoding_agent_extended.py     # Extended version with multiple tools
├── requirements.txt                 # Python dependencies
├── config_example.yaml             # Configuration template
├── README.md                       # This file
├── QUICKSTART.md                   # Quick start guide
└── GEOCODING_AGENT_DOCUMENTATION.md # Complete documentation
```

## Examples

### Basic Version (geocoding_agent.py)
Single tool for geocoding locations:
- Get coordinates for cities, landmarks, and places
- Simple interactive interface

### Extended Version (geocoding_agent_extended.py)
Three tools for advanced features:
- **Geocoding**: Find coordinates for any location
- **Distance Calculation**: Measure distances between two places
- **Reverse Geocoding**: Get location names from coordinates

Run the extended version:
```bash
python geocoding_agent_extended.py
```

Try these queries:
```
GeoNet Pro: How far is Paris from London?
GeoNet Pro: What location is at coordinates 40.7128, -74.0060?
GeoNet Pro: Find the coordinates of Mount Everest
```

## Technology Stack

- **[GitHub Copilot SDK](https://github.com/github/copilot-sdk)** - AI agent framework
- **[GeoPy](https://geopy.readthedocs.io/)** - Geocoding library
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation
- **[OpenStreetMap Nominatim](https://nominatim.org/)** - Geocoding service

## Requirements

- Python 3.8+
- GitHub Copilot subscription
- Node.js (for Copilot CLI)
- Internet connection

## Configuration

Create a `config.yaml` file based on `config_example.yaml`:

```yaml
model: "gpt-5-mini"
system_message: "You are a GeoAI Assistant..."
geocoder:
  user_agent: "your_app_name"
  timeout: 10
```

## Extending the Agent

The agent architecture makes it easy to add new capabilities. See the documentation for tutorials on:

- Adding new geocoding tools (distance, reverse geocoding, etc.)
- Switching AI models (GPT-5, Claude Sonnet, etc.)
- Integrating with web frameworks (FastAPI, Flask)
- Adding logging and analytics
- Building a GUI interface

Example: Add a weather tool in just a few lines:

```python
class WeatherInput(BaseModel):
    place_name: str = Field(description="Location for weather lookup")

async def get_weather_impl(args: WeatherInput) -> str:
    location = geolocator.geocode(args.place_name)
    # Fetch weather using coordinates...
    return f"Weather in {args.place_name}: ..."

weather_tool = define_tool(
    name="get_weather",
    description="Get current weather for a location",
    handler=get_weather_impl
)
```

## Use Cases

This architecture can be adapted for many different applications:

- **Customer Support**: Database lookup tools
- **DevOps**: Docker/Kubernetes management tools
- **Data Science**: Pandas/NumPy analysis tools
- **Code Analysis**: GitHub API integration tools
- **Travel Planning**: Weather, timezone, currency tools

## Troubleshooting

**Agent not using the tool?**
- Make tool descriptions more specific
- Update the system message to emphasize tool usage

**Geocoding errors?**
- Check internet connection
- Verify OpenStreetMap is not blocked
- Add rate limiting (1 request per second)

**Timeout errors?**
- Increase timeout: `session.send_and_wait({...}, timeout=300)`

See [GEOCODING_AGENT_DOCUMENTATION.md](GEOCODING_AGENT_DOCUMENTATION.md#troubleshooting) for complete troubleshooting guide.

## License

This project uses open-source libraries:
- GitHub Copilot SDK (MIT License)
- GeoPy (MIT License)
- Pydantic (MIT License)

OpenStreetMap data is licensed under ODbL. When using Nominatim, include attribution:
```
© OpenStreetMap contributors
```

## Learn More

- [GitHub Copilot SDK Documentation](https://github.com/github/copilot-sdk)
- [GeoPy Documentation](https://geopy.readthedocs.io/)
- [Pydantic Tutorial](https://docs.pydantic.dev/latest/concepts/models/)
- [OpenStreetMap Nominatim](https://nominatim.org/)

## Contributing

Feel free to:
- Add new tools and features
- Improve error handling
- Optimize performance
- Share your extensions

## Support

- Check [GEOCODING_AGENT_DOCUMENTATION.md](GEOCODING_AGENT_DOCUMENTATION.md) for detailed help
- Review [GitHub Copilot SDK Discussions](https://github.com/github/copilot-sdk/discussions)
- File issues at [Copilot SDK Issues](https://github.com/github/copilot-sdk/issues)

---

Built with ❤️ using GitHub Copilot SDK | Geography data by OpenStreetMap
