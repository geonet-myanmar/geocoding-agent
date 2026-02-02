# GeoAI Agent - Quick Start Guide

## 5-Minute Setup

### 1. Install Prerequisites

```bash
# Install GitHub Copilot CLI
npm install -g @github/copilot-cli

# Authenticate
copilot auth login
```

### 2. Set Up Python Environment

```bash
# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Agent

```bash
python geocoding_agent.py
```

### 5. Try It Out

```
GeoNet Myanmar: Where is Bangkok?
GeoNet Myanmar: What are the coordinates of the Eiffel Tower?
GeoNet Myanmar: exit
```

## That's It!

For detailed documentation, see [GEOCODING_AGENT_DOCUMENTATION.md](GEOCODING_AGENT_DOCUMENTATION.md)

## Common Issues

**"copilot command not found"**
→ Install with: `npm install -g @github/copilot-cli`

**"Module not found: copilot"**
→ Install with: `pip install github-copilot-sdk`

**"Not authenticated"**
→ Run: `copilot auth login`
