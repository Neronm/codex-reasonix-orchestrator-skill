#!/usr/bin/env bash
set -euo pipefail

repo_root="${1:-.}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
validator="${script_dir}/validate_skill.py"

if command -v python3 >/dev/null 2>&1; then
  python3_bin="python3"
elif command -v python >/dev/null 2>&1; then
  python3_bin="python"
else
  echo "python3 or python is required in PATH." >&2
  exit 1
fi

"${python3_bin}" "${validator}" --repo-root "${repo_root}" --require-bash
