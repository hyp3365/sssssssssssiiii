#!/usr/bin/env python3
"""Apply the bandwidth-limiter outbound (ported from shtorm-7/sing-box-extended)
to an official SagerNet/sing-box source tree.

Usage (run inside the sing-box source root):
    python3 <this-dir>/apply.py
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "source"
ROOT = Path.cwd()


def die(msg):
    raise SystemExit(f"ERROR: {msg}")


# 1. copy source files
for f in sorted(SRC.rglob("*.go")):
    rel = f.relative_to(SRC)
    dst = ROOT / rel
    if dst.exists():
        die(f"{rel} already exists in sing-box tree")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, dst)
    print(f"CREATED: {rel}")

# 2. constant/proxy.go
p = ROOT / "constant/proxy.go"
s = p.read_text()
if "TypeBandwidthLimiter" in s:
    die("constant TypeBandwidthLimiter already defined")
s, n = re.subn(r'(\n\tTypeSelector\s*=\s*"selector"\n)',
               r'\1\tTypeBandwidthLimiter = "bandwidth-limiter"\n', s, count=1)
if n != 1:
    die("constant/proxy.go: TypeSelector not found")
s, n = re.subn(r'(\n\tcase TypeSelector:\n)',
               '\n\tcase TypeBandwidthLimiter:\n\t\treturn "Bandwidth Limiter"\\1', s, count=1)
if n != 1:
    die("constant/proxy.go: case TypeSelector not found")
p.write_text(s)
print("PATCHED: constant/proxy.go")

# 3. include/registry.go
p = ROOT / "include/registry.go"
s = p.read_text()
s, n = re.subn(r'(\n\tgroup\.RegisterSelector\(registry\)\n)',
               r'\1\tbandwidth.RegisterOutbound(registry)\n', s, count=1)
if n != 1:
    die("include/registry.go: group.RegisterSelector(registry) not found")
s, n = re.subn(r'import \(\n',
               'import (\n\t"github.com/sagernet/sing-box/protocol/limiter/bandwidth"\n', s, count=1)
if n != 1:
    die("include/registry.go: import block not found")
p.write_text(s)
print("PATCHED: include/registry.go")

print("bandwidth-limiter applied.")
