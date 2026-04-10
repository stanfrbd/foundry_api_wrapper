import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


def _normalize_base_url(raw_url: str) -> str:
    url = raw_url.strip()
    if not url.endswith("/"):
        url = f"{url}/"

    if "/openai/deployments/" in url:
        prefix = url.split("/openai/deployments/", 1)[0]
        return f"{prefix}/openai/v1/"

    return url


def _get_config() -> tuple[str, str, str]:
    load_dotenv()

    base_url = os.getenv("FOUNDRY_BASE_URL")
    api_key = os.getenv("FOUNDRY_API_KEY")
    model = os.getenv("FOUNDRY_MODEL")

    missing = [
        name
        for name, value in (
            ("FOUNDRY_BASE_URL", base_url),
            ("FOUNDRY_API_KEY", api_key),
            ("FOUNDRY_MODEL", model),
        )
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing required configuration: " + ", ".join(missing)
        )

    return _normalize_base_url(base_url), api_key, model


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="foundry-api",
        description="Minimal CLI wrapper for Azure Foundry chat completions.",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        required=True,
        help="Prompt to send to the model.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Ask the model to return valid JSON and print it as-is.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print the full API response as JSON.",
    )
    parser.add_argument(
        "--model",
        help="Override FOUNDRY_MODEL for this invocation.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        base_url, api_key, model = _get_config()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.model:
        model = args.model

    client = OpenAI(base_url=base_url, api_key=api_key)

    if args.raw:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": args.prompt}],
        )
        print(completion.model_dump_json(indent=2))
        return 0

    messages = [{"role": "user", "content": args.prompt}]
    completion_kwargs = {}

    if args.json:
        messages = [
            {
                "role": "system",
                "content": (
                    "Return only valid JSON. "
                    "Do not add markdown fences, explanations, or extra text."
                ),
            },
            {"role": "user", "content": args.prompt},
        ]
        completion_kwargs["response_format"] = {"type": "json_object"}

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        **completion_kwargs,
    )

    message = completion.choices[0].message
    content = message.content if message and message.content is not None else ""

    print(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
