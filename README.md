# MCP Date Server Demo

This project demonstrates a complete MCP (Model Context Protocol) implementation with:
1. An MCP Server that exposes a date tool
2. An MCP Client that connects to the server
3. Integration with OpenAI to use the tool via function calling
4. A Gradio UI to compare responses with and without tool access

## Project Structure

```
simple_mcp_server/
├── date_server.py      # MCP Server with get_current_date tool
├── date.py             # Date utility function
├── mcp_client.py       # MCP Client that connects to server and integrates with OpenAI
├── app.py              # Gradio UI application
└── requirements.txt    # Python dependencies
```

## How It Works

### 1. MCP Server (`date_server.py`)
- Uses FastMCP to create an MCP server
- Exposes a `get_current_date` tool that returns the current date
- Accepts a format parameter for date formatting (strftime format)

### 2. Date Utility (`date.py`)
- Contains the actual date logic using Python's datetime
- Returns formatted current date

### 3. MCP Client (`mcp_client.py`)
- Connects to the MCP server via stdio
- Retrieves available tools from the server
- Converts MCP tools to OpenAI function format
- Enables OpenAI to call MCP tools through function calling
- Handles the agentic loop: question → tool call → result → final answer

### 4. Gradio App (`app.py`)
- Side-by-side comparison of:
  - **With MCP Tools**: Agent can access the real date via the tool
  - **Without MCP Tools**: Agent responds without tool access (may hallucinate)
- Demonstrates the value of MCP for providing agents with real-time data

## Setup

1. Create a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

### Option 1: Full Gradio UI (Recommended)
```bash
uv run app.py
```
Then open http://localhost:7860 in your browser.

### Option 2: Test MCP Client Directly
```bash
uv run mcp_client.py
```
This runs a standalone test of the MCP client without the UI.

### Option 3: Test MCP Server Only
```bash
uv run date_server.py
```
This starts just the MCP server (it will wait for connections).

## Key Features

- **Tool Exposure**: The MCP server exposes a `get_current_date` tool
- **Native OpenAI Integration**: Uses OpenAI's function calling without Agents SDK
- **Real-time Data**: Agent gets accurate current date through the tool
- **Comparison**: See the difference between agent with/without tool access

## Requirements Met

✅ **Basic**: MCP Server with date function exposed as a tool
✅ **Advanced**: MCP Client using native OpenAI calls (no Agents SDK)

## Example Usage

When you ask "What is today's date?":

**With MCP Tools**:
1. OpenAI receives the question
2. OpenAI decides to call the `get_current_date` tool
3. MCP Client calls the tool through the MCP Server
4. Tool returns actual current date: "2026-01-10"
5. OpenAI formats final answer with accurate date

**Without MCP Tools**:
- OpenAI responds based on training data
- May provide wrong date or hedge with "I don't have access to current date"

## Technical Notes

- Uses `stdio` transport for MCP server/client communication
- Server runs as subprocess spawned by the client
- OpenAI function calling bridges the gap between OpenAI and MCP
- Asynchronous implementation using asyncio
