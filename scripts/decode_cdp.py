#!/usr/bin/env python3
import base64
import json
import sys
from pathlib import Path


def decode_cdp_log(log_path: Path) -> str:
    data = json.loads(log_path.read_text())
    value = data["result"]["value"]
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    raise ValueError(f"Unexpected CDP payload in {log_path}")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: decode_cdp.py <cdp-log.json> <output-file>")

    log_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    encoded = decode_cdp_log(log_path)
    output_path.write_bytes(base64.b64decode(encoded))
    print(f"Wrote {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
