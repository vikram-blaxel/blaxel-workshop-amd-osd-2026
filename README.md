# Workshop: Give Your Coding Agent a Perpetual Sandbox for Isolated Execution

## Prerequisites

- Python 3.12+ development environment
- LLM provider API key (Gemini, Anthropic or OpenAI)

## Setup and usage

```
python3 -m venv .venv
source .venv/bin/activate
pip install blaxel fastapi strands-agents[all] strands-agents-tools
export BL_WORKSPACE=...
export BL_API_KEY=...
export ANTHROPIC_API_KEY=...  # or OPENAI_API_KEY or GOOGLE_API_KEY, then uncomment the matching model in the script
python 01-sbx-basics/sandbox.py  # replace with the example you want to run
```

## Examples

- [01-sbx-basics](01-sbx-basics/sandbox.py) - Create a sandbox
- [02-connect-agt-sbx](02-connect-agt-sbx/agent.py) - Connect a Strands agent to a sandbox via the MCP server
- [03-analyze-data](03-analyze-data/agent.py) - Read a CSV file and have the agent generate a chart from the data using the sandbox for compute
- [04-preview-sbx](04-preview-sbx/sandbox.py) - Expose a sandbox server as a public preview URL
- [05-develop-webapp](05-develop-webapp/agent.py) - Create a Strands agent that accepts a task and uses the agent to develop a Next.js app in a sandbox

## Help

Need help? [Join the Discord](https://discord.gg/enAfyZFWHW)!
