#!/usr/bin/env python3
import base64
import sys
from pathlib import Path

target = Path(sys.argv[1])
target.parent.mkdir(parents=True, exist_ok=True)
data = sys.stdin.read().strip()
target.write_bytes(base64.b64decode(data))
