#!/usr/bin/env bash
# deploy.sh — deploy a single HTML file to Fluid Docs
# Dependencies: curl, python3 (standard on macOS/Linux)
# Usage:
#   bash deploy.sh                            # list HTML files and pick one
#   bash deploy.sh --host http://localhost:8080  # use a local server
#   bash deploy.sh --logout                   # clear cached credentials
#   bash deploy.sh --help
#
# Environment variables:
#   FLUIDDOCS_URL   Server base URL (overridden by --host flag)

set -euo pipefail

BASE_URL="${FLUIDDOCS_URL:-https://fluiddocs.ai}"
AUTH_FILE="${HOME}/.config/fluiddocs/auth.json"
_GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
STATE_FILE="${_GIT_ROOT}/.fluid-docs.json"

POLL_INTERVAL=2
POLL_MAX=300   # 5 minutes (browser auth window)

# ── Helpers ───────────────────────────────────────────────────────────────────

json_get() {
  # json_get KEY < file  or  KEY <<< "$string"
  local key="$1"
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('${key}',''))"
}

json_get_nested() {
  # json_get_nested FILE KEY1 KEY2
  local file="$1" k1="$2" k2="$3"
  python3 -c "
import json, sys
with open('${file}') as f:
    d = json.load(f)
print(d.get('${k1}', {}).get('${k2}', ''))
"
}

json_set_auth() {
  local token="$1" expires="$2"
  mkdir -p "$(dirname "$AUTH_FILE")"
  python3 -c "
import json
with open('${AUTH_FILE}', 'w') as f:
    json.dump({'token': '${token}', 'expiresAt': '${expires}'}, f)
"
}

json_upsert_state() {
  local filename="$1" project_id="$2" url="$3"
  local now
  now=$(python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())")
  python3 -c "
import json, os
path = '${STATE_FILE}'
d = {}
if os.path.exists(path):
    with open(path) as f:
        d = json.load(f)
d['${filename}'] = {'projectId': '${project_id}', 'url': '${url}', 'lastDeployed': '${now}'}
with open(path, 'w') as f:
    json.dump(d, f, indent=2)
print('${url}')
"
}

is_token_valid() {
  # Returns 0 (true) if token file exists and expires more than 5 min from now
  if [ ! -f "$AUTH_FILE" ]; then return 1; fi
  local expires
  expires=$(json_get "expiresAt" < "$AUTH_FILE")
  if [ -z "$expires" ]; then return 1; fi
  local ok
  ok=$(python3 -c "
from datetime import datetime, timezone, timedelta
import sys
try:
    exp = datetime.fromisoformat('${expires}'.replace('Z', '+00:00'))
    margin = datetime.now(timezone.utc) + timedelta(minutes=5)
    print('ok' if exp > margin else '')
except Exception:
    print('')
")
  [ "$ok" = "ok" ]
}

open_browser() {
  local url="$1"
  case "$(uname -s)" in
    Darwin)  open "$url" ;;
    Linux)
      if command -v xdg-open &>/dev/null; then
        xdg-open "$url"
      else
        echo "  Could not auto-open browser. Visit the URL above manually."
      fi
      ;;
    MINGW*|CYGWIN*|MSYS*)  explorer.exe "$url" ;;
    *)  echo "  Could not auto-open browser. Visit the URL above manually." ;;
  esac
}

spin_chars=('\' '|' '/' '-')
spin_idx=0
spinner() {
  printf "\r  %s Waiting for browser authorization…" "${spin_chars[$spin_idx]}"
  spin_idx=$(( (spin_idx + 1) % 4 ))
}

# ── Auth flow ─────────────────────────────────────────────────────────────────

do_auth() {
  echo ""
  echo "Authenticating with Fluid Docs…"

  local start_resp
  start_resp=$(curl -s -X POST "${BASE_URL}/api/v1/auth/cli-start")

  local request_id login_url
  request_id=$(echo "$start_resp" | json_get "requestId")
  login_url=$(echo "$start_resp" | json_get "loginUrl")

  if [ -z "$request_id" ]; then
    echo "Error: Could not start auth session. Is the server reachable at ${BASE_URL}?" >&2
    exit 1
  fi

  echo ""
  echo "  Open this URL to sign in:"
  echo "  ${login_url}"
  echo ""

  open_browser "$login_url"

  local elapsed=0
  while [ $elapsed -lt $POLL_MAX ]; do
    spinner
    sleep $POLL_INTERVAL
    elapsed=$((elapsed + POLL_INTERVAL))

    local poll_resp status
    poll_resp=$(curl -s "${BASE_URL}/api/v1/auth/cli-poll?requestId=${request_id}")
    status=$(echo "$poll_resp" | json_get "status")

    if [ "$status" = "authorized" ]; then
      local token expires
      token=$(echo "$poll_resp" | json_get "token")
      expires=$(echo "$poll_resp" | json_get "expiresAt")
      printf "\r  ✓ Authorized!                                  \n"
      json_set_auth "$token" "$expires"
      return 0
    elif [ "$status" = "expired" ]; then
      printf "\r  ✗ Auth request expired. Please try again.\n" >&2
      exit 1
    fi
  done

  printf "\r  ✗ Timed out waiting for browser authorization.\n" >&2
  exit 1
}

# ── Arg parsing ───────────────────────────────────────────────────────────────

DO_LOGOUT=false
FRIENDLY_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      echo "Usage: bash deploy.sh [OPTIONS]"
      echo ""
      echo "  Deploy an HTML file from the current directory to Fluid Docs."
      echo "  Auth token is cached in ~/.config/fluiddocs/auth.json."
      echo "  Project mapping is stored in ./.fluid-docs.json."
      echo ""
      echo "  Options:"
      echo "    --host URL   Server base URL (default: https://fluiddocs.ai)"
      echo "                 Can also be set via FLUIDDOCS_URL env var."
      echo "    --name NAME  Friendly project name (default: filename without extension)"
      echo "    --logout     Clear cached credentials"
      echo "    --help       Show this message"
      echo ""
      echo "  Examples:"
      echo "    bash deploy.sh --host http://localhost:8080"
      echo "    bash deploy.sh --name \"My Project\""
      exit 0
      ;;
    --logout)
      DO_LOGOUT=true
      shift
      ;;
    --host)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --host requires a URL argument" >&2
        exit 1
      fi
      BASE_URL="${2%/}"   # strip trailing slash
      shift 2
      ;;
    --host=*)
      BASE_URL="${1#--host=}"
      BASE_URL="${BASE_URL%/}"
      shift
      ;;
    --name)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --name requires a value" >&2
        exit 1
      fi
      FRIENDLY_NAME="$2"
      shift 2
      ;;
    --name=*)
      FRIENDLY_NAME="${1#--name=}"
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run 'bash deploy.sh --help' for usage." >&2
      exit 1
      ;;
  esac
done

# ── Main ─────────────────────────────────────────────────────────────────────

if $DO_LOGOUT; then
  rm -f "$AUTH_FILE"
  echo "Logged out. Run the script again to re-authenticate."
  exit 0
fi

# Ensure token is valid
if ! is_token_valid; then
  do_auth
fi

TOKEN=$(json_get "token" < "$AUTH_FILE")

# Collect top-level HTML files (mapfile requires bash 4+; use while-read for macOS compat)
HTML_FILES=()
while IFS= read -r f; do
  HTML_FILES+=("$f")
done < <(find . -maxdepth 1 \( -name "*.html" -o -name "*.htm" \) | sort | sed 's|^\./||')

if [ ${#HTML_FILES[@]} -eq 0 ]; then
  echo "No HTML files found in the current directory." >&2
  exit 1
fi

# Pick a file
if [ ${#HTML_FILES[@]} -eq 1 ]; then
  SELECTED_FILE="${HTML_FILES[0]}"
  echo "Found: ${SELECTED_FILE}"
else
  echo ""
  echo "Select a file to deploy:"
  for i in "${!HTML_FILES[@]}"; do
    echo "  $((i + 1))) ${HTML_FILES[$i]}"
  done
  echo ""
  printf "Enter number [1]: "
  read -r choice
  choice="${choice:-1}"
  if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt ${#HTML_FILES[@]} ]; then
    echo "Invalid choice." >&2
    exit 1
  fi
  SELECTED_FILE="${HTML_FILES[$((choice - 1))]}"
fi

# Derive name from filename, or use friendly name if provided
NAME="${FRIENDLY_NAME:-${SELECTED_FILE%.*}}"

# Check for existing projectId
EXISTING_PROJECT_ID=""
if [ -f "$STATE_FILE" ]; then
  EXISTING_PROJECT_ID=$(python3 -c "
import json, os
with open('${STATE_FILE}') as f:
    d = json.load(f)
print(d.get('${SELECTED_FILE}', {}).get('projectId', ''))
" 2>/dev/null || true)
fi

echo ""
echo "Deploying ${SELECTED_FILE}…"

# Build curl args
CURL_ARGS=(
  -s
  -X POST
  "${BASE_URL}/api/v1/deploy/upload"
  -H "Authorization: Bearer ${TOKEN}"
  -F "file=@${SELECTED_FILE}"
  -F "name=${NAME}"
)
if [ -n "$EXISTING_PROJECT_ID" ]; then
  CURL_ARGS+=(-F "existingProjectId=${EXISTING_PROJECT_ID}")
fi

DEPLOY_RESP=$(curl "${CURL_ARGS[@]}")

PROJECT_ID=$(echo "$DEPLOY_RESP" | json_get "projectId")
DEPLOY_URL=$(echo "$DEPLOY_RESP" | json_get "url")
DEPLOY_ERROR=$(echo "$DEPLOY_RESP" | json_get "error")

if [ -n "$DEPLOY_ERROR" ] || [ -z "$PROJECT_ID" ]; then
  echo ""
  echo "Deploy failed: ${DEPLOY_ERROR:-unexpected response}" >&2
  exit 1
fi

# Save state
json_upsert_state "$SELECTED_FILE" "$PROJECT_ID" "$DEPLOY_URL" > /dev/null

echo ""
echo "  ✓ Deployed → ${DEPLOY_URL}"
echo ""

# Open the live page in the browser
open_browser "$DEPLOY_URL"
