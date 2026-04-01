# Workshop: Give Your Coding Agent a Perpetual Sandbox for Isolated Execution

## Prerequisites

- Blaxel account
  - [Sign up free](https://app.blaxel.ai?utm_source=osd_amd_04_2026&utm_medium=conference&utm_campaign=q2_2026_events)
- Blaxel CLI
  - [Install the CLI](https://docs.blaxel.ai/cli-reference/introduction?utm_source=osd_amd_04_2026&utm_medium=conference&utm_campaign=q2_2026_events)
- Blaxel API key
  - [Generate an API key](https://docs.blaxel.ai/Security/Access-tokens#manage-api-keys?utm_source=osd_amd_04_2026&utm_medium=conference&utm_campaign=q2_2026_events)
- LLM provider API key
  - [Generate OpenAI API key](https://platform.openai.com/account/api-keys)
  - [Generate Anthropic API key](https://platform.claude.com/settings/keys)
  - [Generate Google Gemini API key](https://aistudio.google.com/app/apikey)

## Setup and usage

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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
