#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CATALOG="$REPO_ROOT/corpus/tier2/CANDIDATE_REPOS.tsv"
PDF_LINKS="$REPO_ROOT/corpus/tier2/PDF_LINKS.txt"
OUT_DIR="$REPO_ROOT/corpus/research/availability"
OUT_JSON="$OUT_DIR/availability.json"
OUT_MD="$OUT_DIR/AVAILABILITY_REPORT.md"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"
CURL_TIMEOUT_SEC="${AVAILABILITY_TIMEOUT_SEC:-10}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/availability-scan.XXXXXX")"

trash_path() {
  local path="$1"
  [ -e "$path" ] || return 0
  command -v trash >/dev/null 2>&1 || return 0
  mkdir -p "$TRASH_DIR"
  trash --trash-dir "$TRASH_DIR" "$path" || true
}

cleanup_tmp() {
  trash_path "$TMP_DIR"
}

trap cleanup_tmp EXIT

require_cmds() {
  local missing=0
  for cmd in curl jq awk sed date mktemp rg; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

require_cmds || exit 1

mkdir -p "$OUT_DIR"

urlencode() {
  local raw="$1"
  printf '%s' "$raw" | jq -sRr @uri
}

probe_live() {
  local url="$1"
  local metrics="$TMP_DIR/live-metrics.txt"
  local err="$TMP_DIR/live-err.txt"
  local code effective error

  if curl -sS -L --max-time "$CURL_TIMEOUT_SEC" -o /dev/null -w '%{http_code}\t%{url_effective}' "$url" >"$metrics" 2>"$err"; then
    code="$(awk -F'\t' '{print $1}' "$metrics")"
    effective="$(awk -F'\t' '{print $2}' "$metrics")"
    error=""
  else
    code="000"
    effective=""
    error="$(tr '\n' ' ' <"$err" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')"
  fi

  jq -n \
    --arg code "$code" \
    --arg effective "$effective" \
    --arg error "$error" \
    '
    {
      http_code: $code,
      effective_url: $effective,
      error: $error,
      ok: (
        ($error == "") and
        (($code | tonumber) >= 200) and
        (($code | tonumber) < 400)
      )
    }'
}

probe_archive_org() {
  local url="$1"
  local encoded output err line ts orig
  local query

  encoded="$(urlencode "$url")"
  query="https://web.archive.org/cdx/search/cdx?url=${encoded}&fl=timestamp,original,statuscode&filter=statuscode:200&limit=1&from=2000&to=2026&sort=reverse"
  err="$TMP_DIR/ao-err.txt"

  if ! output="$(curl -sS -L --max-time "$CURL_TIMEOUT_SEC" "$query" 2>"$err")"; then
    jq -n \
      --arg state "error" \
      --arg error "$(tr '\n' ' ' <"$err" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')" \
      --arg snapshot_ts "" \
      --arg snapshot_url "" \
      '{
        state: $state,
        error: $error,
        snapshot_ts: $snapshot_ts,
        snapshot_url: $snapshot_url
      }'
    return 0
  fi

  if printf '%s' "$output" | rg -q '<h1>503 Service Unavailable</h1>'; then
    jq -n \
      --arg state "service_unavailable" \
      --arg error "archive.org CDX returned 503 HTML" \
      --arg snapshot_ts "" \
      --arg snapshot_url "" \
      '{
        state: $state,
        error: $error,
        snapshot_ts: $snapshot_ts,
        snapshot_url: $snapshot_url
      }'
    return 0
  fi

  line="$(printf '%s' "$output" | sed -n '1p')"
  if [ -z "$line" ]; then
    jq -n \
      --arg state "no_snapshot" \
      --arg error "" \
      --arg snapshot_ts "" \
      --arg snapshot_url "" \
      '{
        state: $state,
        error: $error,
        snapshot_ts: $snapshot_ts,
        snapshot_url: $snapshot_url
      }'
    return 0
  fi

  ts="$(printf '%s' "$line" | awk '{print $1}')"
  orig="$(printf '%s' "$line" | awk '{print $2}')"

  if printf '%s' "$ts" | rg -q '^[0-9]{14}$'; then
    jq -n \
      --arg state "snapshot" \
      --arg error "" \
      --arg snapshot_ts "$ts" \
      --arg snapshot_url "https://web.archive.org/web/${ts}/${orig}" \
      '{
        state: $state,
        error: $error,
        snapshot_ts: $snapshot_ts,
        snapshot_url: $snapshot_url
      }'
  else
    jq -n \
      --arg state "unknown_response" \
      --arg error "$(printf '%s' "$line")" \
      --arg snapshot_ts "" \
      --arg snapshot_url "" \
      '{
        state: $state,
        error: $error,
        snapshot_ts: $snapshot_ts,
        snapshot_url: $snapshot_url
      }'
  fi
}

probe_archive_is() {
  local url="$1"
  local metrics="$TMP_DIR/ais-metrics.txt"
  local err="$TMP_DIR/ais-err.txt"
  local code effective error state snapshot_url
  local endpoint

  endpoint="https://archive.is/timegate/${url}"

  if curl -sS -L --max-time "$CURL_TIMEOUT_SEC" -o /dev/null -w '%{http_code}\t%{url_effective}' "$endpoint" >"$metrics" 2>"$err"; then
    code="$(awk -F'\t' '{print $1}' "$metrics")"
    effective="$(awk -F'\t' '{print $2}' "$metrics")"
    error=""
  else
    code="000"
    effective=""
    error="$(tr '\n' ' ' <"$err" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')"
  fi

  state="unknown"
  snapshot_url=""
  if [ -n "$error" ]; then
    state="error"
  elif printf '%s' "$effective" | rg -q '^https://archive\.(is|ph|today|md)/[0-9]{14}/'; then
    if [ "$code" = "429" ]; then
      state="snapshot_rate_limited"
    else
      state="snapshot"
    fi
    snapshot_url="$effective"
  elif [ "$code" = "404" ]; then
    state="no_snapshot"
  elif [ "$code" = "429" ]; then
    state="rate_limited"
  elif [ "$code" = "000" ]; then
    state="error"
  fi

  jq -n \
    --arg state "$state" \
    --arg code "$code" \
    --arg effective "$effective" \
    --arg error "$error" \
    --arg snapshot_url "$snapshot_url" \
    '{
      state: $state,
      http_code: $code,
      effective_url: $effective,
      error: $error,
      snapshot_url: $snapshot_url
    }'
}

classify_status() {
  local live_ok="$1"
  local ao_state="$2"
  local ais_state="$3"

  if [ "$live_ok" = "true" ]; then
    echo "available_live"
    return 0
  fi

  if [ "$ao_state" = "snapshot" ] || [ "$ais_state" = "snapshot" ] || [ "$ais_state" = "snapshot_rate_limited" ]; then
    echo "live_unavailable_archived"
    return 0
  fi

  if [ "$ao_state" = "no_snapshot" ] && [ "$ais_state" = "no_snapshot" ]; then
    echo "vanished_candidate"
    return 0
  fi

  echo "unavailable_archive_unknown"
}

records_jsonl="$TMP_DIR/records.jsonl"
: > "$records_jsonl"

known_catalog_github_urls="$TMP_DIR/catalog-github-urls.txt"
awk 'NF && $1 !~ /^#/ {print "https://github.com/"$3}' "$CATALOG" | sort -u > "$known_catalog_github_urls"

catalog_total="$(awk 'NF && $1 !~ /^#/' "$CATALOG" | wc -l | awk '{print $1}')"
pdf_total="$(awk 'NF && $1 !~ /^#/' "$PDF_LINKS" | wc -l | awk '{print $1}')"
catalog_i=0
pdf_i=0

# Tiered candidate repos.
while IFS=$'\t' read -r tier label repo kind oracle_priority corpus_priority source status; do
  [ -z "$tier" ] && continue
  if printf '%s' "$tier" | rg -q '^#'; then
    continue
  fi

  catalog_i=$((catalog_i + 1))
  echo "[catalog ${catalog_i}/${catalog_total}] ${repo}" >&2

  url="https://github.com/$repo"
  live="$(probe_live "$url")"
  ao="$(probe_archive_org "$url")"

  live_ok="$(printf '%s' "$live" | jq -r '.ok')"
  ao_state="$(printf '%s' "$ao" | jq -r '.state')"
  if [ "$live_ok" = "true" ]; then
    ais='{"state":"skipped_live_available","http_code":"","effective_url":"","error":"","snapshot_url":""}'
  else
    ais="$(probe_archive_is "$url")"
  fi
  ais_state="$(printf '%s' "$ais" | jq -r '.state')"
  verdict="$(classify_status "$live_ok" "$ao_state" "$ais_state")"

  gh_api_body="$TMP_DIR/gh-${label}.json"
  gh_api_err="$TMP_DIR/gh-${label}.err"
  gh_api_code="$(
    curl -sS -L --max-time "$CURL_TIMEOUT_SEC" -o "$gh_api_body" -w '%{http_code}' "https://api.github.com/repos/$repo" 2>"$gh_api_err" \
      || echo "000"
  )"
  if [ ! -s "$gh_api_body" ]; then
    printf '{}' > "$gh_api_body"
  fi

  jq -n \
    --arg source_kind "catalog" \
    --arg tier "$tier" \
    --arg label "$label" \
    --arg repo "$repo" \
    --arg kind "$kind" \
    --arg oracle_priority "$oracle_priority" \
    --arg corpus_priority "$corpus_priority" \
    --arg source "$source" \
    --arg status "$status" \
    --arg url "$url" \
    --arg verdict "$verdict" \
    --arg gh_api_code "$gh_api_code" \
    --arg gh_full_name "$(jq -r '.full_name // empty' "$gh_api_body")" \
    --arg gh_archived "$(jq -r '.archived // empty' "$gh_api_body")" \
    --arg gh_disabled "$(jq -r '.disabled // empty' "$gh_api_body")" \
    --arg gh_pushed_at "$(jq -r '.pushed_at // empty' "$gh_api_body")" \
    --arg gh_message "$(jq -r '.message // empty' "$gh_api_body")" \
    --argjson live "$live" \
    --argjson archive_org "$ao" \
    --argjson archive_is "$ais" \
    '
    {
      source_kind: $source_kind,
      tier: $tier,
      label: $label,
      repo: $repo,
      kind: $kind,
      oracle_priority: $oracle_priority,
      corpus_priority: $corpus_priority,
      source: $source,
      catalog_status: $status,
      url: $url,
      verdict: $verdict,
      github: {
        api_http_code: $gh_api_code,
        full_name: $gh_full_name,
        archived: $gh_archived,
        disabled: $gh_disabled,
        pushed_at: $gh_pushed_at,
        message: $gh_message
      },
      live: $live,
      archive_org: $archive_org,
      archive_is: $archive_is
    }' >> "$records_jsonl"
done < "$CATALOG"

# Additional historical links from PDF citations.
while IFS= read -r url; do
  [ -z "$url" ] && continue
  if printf '%s' "$url" | rg -q '^#'; then
    continue
  fi
  # Skip links already covered by catalog GitHub URLs.
  if printf '%s' "$url" | rg -q '^https://github.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$'; then
    if rg -qx "$url" "$known_catalog_github_urls"; then
      continue
    fi
  fi

  pdf_i=$((pdf_i + 1))
  echo "[pdf ${pdf_i}/${pdf_total}] ${url}" >&2

  live="$(probe_live "$url")"
  ao="$(probe_archive_org "$url")"

  live_ok="$(printf '%s' "$live" | jq -r '.ok')"
  ao_state="$(printf '%s' "$ao" | jq -r '.state')"
  if [ "$live_ok" = "true" ]; then
    ais='{"state":"skipped_live_available","http_code":"","effective_url":"","error":"","snapshot_url":""}'
  else
    ais="$(probe_archive_is "$url")"
  fi
  ais_state="$(printf '%s' "$ais" | jq -r '.state')"
  verdict="$(classify_status "$live_ok" "$ao_state" "$ais_state")"

  jq -n \
    --arg source_kind "pdf_link" \
    --arg url "$url" \
    --arg verdict "$verdict" \
    --argjson live "$live" \
    --argjson archive_org "$ao" \
    --argjson archive_is "$ais" \
    '{
      source_kind: $source_kind,
      url: $url,
      verdict: $verdict,
      live: $live,
      archive_org: $archive_org,
      archive_is: $archive_is
    }' >> "$records_jsonl"
done < "$PDF_LINKS"

generated_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -s \
  --arg generated_at "$generated_at" \
  --arg catalog_path "corpus/tier2/CANDIDATE_REPOS.tsv" \
  --arg pdf_links_path "corpus/tier2/PDF_LINKS.txt" \
  '
  {
    generated_at: $generated_at,
    catalog_path: $catalog_path,
    pdf_links_path: $pdf_links_path,
    records: .
  }' \
  "$records_jsonl" > "$OUT_JSON"

{
  echo "# Implementation Availability Report"
  echo
  echo "Generated: \`$generated_at\`"
  echo
  echo "Policy:"
  echo
  echo "- \`vanished_candidate\` means live probe failed **and** both archive checks were definitively \`no_snapshot\`."
  echo "- If any archive endpoint is rate-limited, timed out, or unavailable, verdict stays conservative (\`unavailable_archive_unknown\`)."
  echo
  echo "## Catalog Repos"
  echo
  echo "| Tier | Label | Repo | Verdict | GitHub API | Live | Archive.org | Archive.is |"
  echo "| --- | --- | --- | --- | --- | --- | --- | --- |"
  jq -r '
    .records[]
    | select(.source_kind == "catalog")
    | [
        .tier,
        .label,
        .repo,
        .verdict,
        .github.api_http_code,
        (.live.http_code + (if .live.error != "" then " err" else "" end)),
        .archive_org.state,
        .archive_is.state
      ]
    | "| " + join(" | ") + " |"
  ' "$OUT_JSON"
  echo
  echo "## PDF Citation Links"
  echo
  echo "| URL | Verdict | Live | Archive.org | Archive.is |"
  echo "| --- | --- | --- | --- | --- |"
  jq -r '
    .records[]
    | select(.source_kind == "pdf_link")
    | [
        .url,
        .verdict,
        (.live.http_code + (if .live.error != "" then " err" else "" end)),
        .archive_org.state,
        .archive_is.state
      ]
    | "| " + join(" | ") + " |"
  ' "$OUT_JSON"
  echo
  echo "## Vanished Candidates"
  echo
  jq -r '
    [
      .records[]
      | select(.verdict == "vanished_candidate")
      | if .source_kind == "catalog"
        then "- " + .source_kind + ": " + .repo + " (" + .url + ")"
        else "- " + .source_kind + ": " + .url
        end
    ]
    | if length == 0 then "- none" else .[] end
  ' "$OUT_JSON"
  echo
  echo "## Archive Evidence Notes"
  echo
  jq -r '
    .records[]
    | select(.archive_org.state == "snapshot" or .archive_is.state == "snapshot" or .archive_is.state == "snapshot_rate_limited")
    | if .source_kind == "catalog"
      then
        "- " + .repo +
        (if .archive_org.snapshot_url != "" then " | archive.org: " + .archive_org.snapshot_url else "" end) +
        (if .archive_is.snapshot_url != "" then " | archive.is: " + .archive_is.snapshot_url else "" end)
      else
        "- " + .url +
        (if .archive_org.snapshot_url != "" then " | archive.org: " + .archive_org.snapshot_url else "" end) +
        (if .archive_is.snapshot_url != "" then " | archive.is: " + .archive_is.snapshot_url else "" end)
      end
  ' "$OUT_JSON"
} > "$OUT_MD"

echo "Wrote:"
echo "- $OUT_JSON"
echo "- $OUT_MD"
