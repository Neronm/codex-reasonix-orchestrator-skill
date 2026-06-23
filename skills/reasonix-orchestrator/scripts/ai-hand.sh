#!/usr/bin/env bash
set -euo pipefail

task_slug="${1-}"

echo "Codex Desktop Orchestrator mode: invoking Reasonix Hand only."
echo "Expected caller: Codex Desktop after user confirmation."

get_project_root() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  cd "${script_dir}/../.." && pwd
}

assert_safe_task_slug() {
  local slug="$1"

  if [[ ! "$slug" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$ ]]; then
    echo "Invalid task slug. Use 1-80 chars: letters, numbers, dot, underscore, hyphen." >&2
    exit 1
  fi
}

test_command_available() {
  local name="$1"
  command -v "$name" >/dev/null 2>&1
}

capture_command_output() {
  local output
  set +e
  output="$("$@" 2>&1)"
  local status=$?
  set -e
  printf '%s' "$output"
  return "$status"
}

resolve_reasonix_command() {
  if ! test_command_available "reasonix"; then
    echo "reasonix CLI not found in PATH. Install Reasonix CLI and make sure \`reasonix\` is available before running ./scripts/ai-hand.sh." >&2
    exit 1
  fi

  local version help
  version="$(capture_command_output reasonix --version || true)"
  if [[ -z "${version//[[:space:]]/}" ]]; then
    version="$(capture_command_output reasonix --help || true)"
  fi

  help="$(capture_command_output reasonix --help || true)"

  if grep -Eq '^[[:space:]]*reasonix[[:space:]]+run[[:space:]]+' <<<"$help"; then
    printf 'run'
    return 0
  fi
  if grep -Eq '^[[:space:]]*reasonix[[:space:]]+code[[:space:]]+' <<<"$help"; then
    printf 'code'
    return 0
  fi
  if grep -Eq '^[[:space:]]*reasonix[[:space:]]+exec[[:space:]]+' <<<"$help"; then
    printf 'exec'
    return 0
  fi

  echo "reasonix CLI found, but no supported execution command detected. Expected run, code, or exec." >&2
  echo "$version" >/dev/null
  exit 1
}

invoke_reasonix_task() {
  local prompt="$1"
  local project_root="$2"
  local reasonix_command
  reasonix_command="$(resolve_reasonix_command)"

  local -a args
  args=("$reasonix_command" "--dir" "$project_root" "$prompt")

  reasonix "${args[@]}"
}

if [[ -z "$task_slug" ]]; then
  echo "Usage: ./scripts/ai-hand.sh \"<task-slug>\"" >&2
  exit 1
fi

project_root="$(get_project_root)"
assert_safe_task_slug "$task_slug"

task_dir="${project_root}/.ai/tasks/${task_slug}"
if [[ ! -d "$task_dir" ]]; then
  echo "Task directory not found: ${task_dir}" >&2
  exit 1
fi

spec_path="${task_dir}/SPEC.md"
acceptance_path="${task_dir}/ACCEPTANCE.md"
handoff_path="${task_dir}/REASONIX_HANDOFF.md"
report_path="${task_dir}/EXECUTION_REPORT.md"
prompt_path="${project_root}/.ai/prompts/reasonix-hand.md"
system_path="${project_root}/.reasonix/system-hand.md"

required_paths=(
  "$spec_path"
  "$acceptance_path"
  "$handoff_path"
  "$prompt_path"
  "$system_path"
)

for path in "${required_paths[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "Required file missing: ${path}" >&2
    exit 1
  fi
done

prompt_template="$(cat "$prompt_path")"
system_hand="$(cat "$system_path")"
spec="$(cat "$spec_path")"
acceptance="$(cat "$acceptance_path")"
handoff="$(cat "$handoff_path")"

prompt=$(
  cat <<EOF
${system_hand}

${prompt_template}

Project root:
${project_root}

Task directory:
${task_dir}

Required execution report path:
${report_path}

SPEC.md:
${spec}

ACCEPTANCE.md:
${acceptance}

REASONIX_HANDOFF.md:
${handoff}

Execute now. Act only as Reasonix Hand. Do not redesign requirements. Do not ask the user for more confirmation. Write EXECUTION_REPORT.md when finished.
EOF
)

invoke_reasonix_task "$prompt" "$project_root"

if [[ ! -f "$report_path" ]]; then
  echo "Reasonix Hand did not create required file: ${report_path}" >&2
  exit 1
fi

echo "Reasonix Hand report written to ${report_path}"
