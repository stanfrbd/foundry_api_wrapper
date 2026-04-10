# foundry-api-wrapper

Very small Python CLI wrapper around Azure Foundry chat completions.

## Install (editable)

```bash
pip install -e .
```

After install, the command is available from your PATH:

```bash
foundry-api -p "What is the capital of France?"
```

## Environment variables

You can export these variables or define them in a local `.env` file:

```bash
export FOUNDRY_BASE_URL=https://YOUR-RESOURCE-NAME.openai.azure.com/openai/deployments/
export FOUNDRY_API_KEY=YOUR-AZURE-API-KEY
export FOUNDRY_MODEL=YOUR-DEPLOYMENT-NAME
```

Notes:
- The wrapper accepts `FOUNDRY_BASE_URL` in either style:
  - `https://<resource>.openai.azure.com/openai/v1/`
  - `https://<resource>.openai.azure.com/openai/deployments/`
- If the `deployments/` style is provided, it is normalized automatically to `.../openai/v1/` for the OpenAI client.

## Usage

Prompt:

```bash
foundry-api -p "Explain zero trust in one sentence"
```

JSON output only:

```bash
foundry-api -p "Return a JSON object with keys city and country" --json
```

In `--json` mode, the wrapper asks the model to return valid JSON only and prints the raw JSON response directly, without any extra wrapper object.

Override the deployment for one call:

```bash
foundry-api -p "Hello" --model my-other-deployment
```

Print the full API response:

```bash
foundry-api -p "Hello" --raw
```

You can also execute the script file directly:

```bash
python foundry-api.py -p "Hello"
```
