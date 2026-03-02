#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORPUS_ROOT="$REPO_ROOT/corpus"
CATALOG_PATH="$CORPUS_ROOT/tier2/CANDIDATE_REPOS.tsv"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/corpus-sync.XXXXXX")"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"
EXTERNAL_ISSUES_DIR="$CORPUS_ROOT/research/external_issues"
EXTERNAL_RANKED_ALL_PATH="$EXTERNAL_ISSUES_DIR/ranked_all_items.json"
EXTERNAL_CANDIDATE_PATH="$EXTERNAL_ISSUES_DIR/candidate_repros_ranked.json"
EXTERNAL_FIXTURE_MANIFEST_PATH="$REPO_ROOT/tests/regression-evidence/external/manifest.rktd"
EXTERNAL_PROGRESS_INDEX_PATH="$TMP_DIR/external-progress-index.json"

trash_path() {
  local path="$1"
  [ -e "$path" ] || return 0

  if ! command -v trash >/dev/null 2>&1; then
    echo "Missing required command: trash" >&2
    return 1
  fi

  mkdir -p "$TRASH_DIR"

  # Prefer `sudo trash` when non-interactive sudo is available; otherwise use trash.
  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    sudo trash --trash-dir "$TRASH_DIR" "$path" || trash --trash-dir "$TRASH_DIR" "$path"
  else
    trash --trash-dir "$TRASH_DIR" "$path"
  fi
}

cleanup_tmp() {
  trash_path "$TMP_DIR" || true
}

trap cleanup_tmp EXIT

declare -a TARGET_TIERS=()
SYNC_ALL=true

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync_corpus.sh
  ./scripts/sync_corpus.sh --tier tier1 --tier tier2

Behavior:
  - No flags: sync all tiers found in corpus/tier2/CANDIDATE_REPOS.tsv.
  - --tier: sync only the specified tier(s).
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --tier)
      [ "$#" -lt 2 ] && { echo "Missing value for --tier" >&2; exit 1; }
      TARGET_TIERS+=("$2")
      SYNC_ALL=false
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_cmds() {
  local missing=0
  for cmd in curl jq rg awk sed xargs find wc date mktemp trash git; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

require_cmds || exit 1

write_empty_json() {
  local path="$1"
  printf '{}\n' > "$path"
}

build_external_progress_index() {
  local issue_stats="$TMP_DIR/external-issue-stats.json"
  local candidate_stats="$TMP_DIR/external-candidate-stats.json"
  local fixture_stats="$TMP_DIR/external-fixture-stats.json"
  local fixture_pairs="$TMP_DIR/external-fixture-pairs.tsv"

  write_empty_json "$issue_stats"
  write_empty_json "$candidate_stats"
  write_empty_json "$fixture_stats"

  if [ -s "$EXTERNAL_RANKED_ALL_PATH" ]; then
    jq '
      sort_by(.repo)
      | group_by(.repo)
      | map({
          key: .[0].repo,
          value: {
            external_items_total: length,
            external_issues_total: (map(select(.item_type == "issue")) | length),
            external_prs_total: (map(select(.item_type == "pr")) | length)
          }
        })
      | from_entries
    ' "$EXTERNAL_RANKED_ALL_PATH" > "$issue_stats" || write_empty_json "$issue_stats"
  fi

  if [ -s "$EXTERNAL_CANDIDATE_PATH" ]; then
    jq '
      sort_by(.repo)
      | group_by(.repo)
      | map({
          key: .[0].repo,
          value: {
            candidate_repros_total: length,
            candidate_runtime_safety_total: (map(select(.category == "runtime-safety")) | length),
            candidate_language_total: (map(select(.category == "language")) | length)
          }
        })
      | from_entries
    ' "$EXTERNAL_CANDIDATE_PATH" > "$candidate_stats" || write_empty_json "$candidate_stats"
  fi

  if [ -s "$EXTERNAL_FIXTURE_MANIFEST_PATH" ]; then
    awk '
      /\(source-repo \. "/ {
        line = $0
        sub(/^.*\(source-repo \. "/, "", line)
        sub(/"\).*$/, "", line)
        repo = line
      }
      /\(triage-status \. "/ {
        line = $0
        sub(/^.*\(triage-status \. "/, "", line)
        sub(/"\).*$/, "", line)
        status = line
      }
      /\)\)$/ {
        if (repo != "" && status != "") {
          print repo "\t" status
          repo = ""
          status = ""
        }
      }
    ' "$EXTERNAL_FIXTURE_MANIFEST_PATH" > "$fixture_pairs" || true

    if [ -s "$fixture_pairs" ]; then
      jq -Rn '
        def init: { imported_test_cases_total: 0, triage_status_counts: {} };
        reduce inputs as $line ({};
          if $line == "" then .
          else
            ($line | split("\t")) as $p
            | if ($p | length) < 2 then .
              else
                ($p[0]) as $repo
                | ($p[1]) as $status
                | .[$repo] = (
                    (.[$repo] // init)
                    | .imported_test_cases_total += 1
                    | .triage_status_counts[$status] = ((.triage_status_counts[$status] // 0) + 1)
                  )
              end
          end
        )
      ' < "$fixture_pairs" > "$fixture_stats" || write_empty_json "$fixture_stats"
    fi
  fi

  jq -s '
    reduce .[] as $obj ({};
      reduce ($obj | keys_unsorted[]) as $repo (.;
        .[$repo] = ((.[$repo] // {}) + ($obj[$repo] // {}))
      )
    )
  ' "$issue_stats" "$candidate_stats" "$fixture_stats" > "$EXTERNAL_PROGRESS_INDEX_PATH"
}

declare -a FEATURE_PATTERNS=(
  "CAN HAS [A-Z]+\\?"
  "HAI [0-9]+\\.[0-9]+"
  "HOW IZ I"
  "IF U SAY SO"
  "FOUND YR"
  "IM IN YR"
  "IM OUTTA YR"
  "UPPIN YR"
  "NERFIN YR"
  "TIL"
  "WILE"
  "O RLY\\?"
  "YA RLY"
  "MEBBE"
  "NO WAI"
  "OIC"
  "WTF\\?"
  "OMGWTF"
  "OMG "
  "SMOOSH"
  "MAEK"
  "IS NOW A"
  "I IZ"
  "I HAS A"
  "HAS A"
  "ITZ A BUKKIT"
  "LIEK A"
  "'Z "
  "SRS "
  "GIMMEH"
  "VISIBLE"
  "INVISIBLE"
  "BOTH SAEM"
  "DIFFRINT"
  "BOTH OF"
  "EITHER OF"
  "WON OF"
  "ALL OF"
  "ANY OF"
  "NOT"
)

mkdir -p "$CORPUS_ROOT"

matches_requested_tier() {
  local tier="$1"
  if [ "$SYNC_ALL" = true ]; then
    return 0
  fi
  local t
  for t in "${TARGET_TIERS[@]}"; do
    if [ "$t" = "$tier" ]; then
      return 0
    fi
  done
  return 1
}

download_repo_snapshot() {
  local tier="$1"
  local label="$2"
  local repo="$3"
  local kind="$4"
  local out="$CORPUS_ROOT/$tier/$label"
  local tree_json="$TMP_DIR/${tier}-${label}-tree.json"
  local all_paths="$TMP_DIR/${tier}-${label}-all-paths.txt"
  local selected="$TMP_DIR/${tier}-${label}-files.txt"
  local branch
  local file_failures=0
  local include_impl=0
  local fallback_note=""

  trash_path "$out"
  mkdir -p "$out/files"

  if ! curl -sS -L --max-time 20 "https://api.github.com/repos/$repo" > "$out/metadata.json"; then
    fallback_note="$(download_repo_snapshot_via_git "$tier" "$label" "$repo" "$kind" || true)"
    if [ -n "$fallback_note" ]; then
      echo "$fallback_note"
      return 0
    fi
    echo "failed:metadata-fetch"
    return 1
  fi

  branch="$(jq -r '.default_branch // empty' "$out/metadata.json")"
  if [ -z "$branch" ]; then
    fallback_note="$(download_repo_snapshot_via_git "$tier" "$label" "$repo" "$kind" || true)"
    if [ -n "$fallback_note" ]; then
      echo "$fallback_note"
      return 0
    fi
    echo "failed:no-default-branch"
    return 1
  fi

  if ! curl -sS -L --max-time 20 "https://api.github.com/repos/$repo/git/trees/$branch?recursive=1" > "$tree_json"; then
    fallback_note="$(download_repo_snapshot_via_git "$tier" "$label" "$repo" "$kind" || true)"
    if [ -n "$fallback_note" ]; then
      echo "$fallback_note"
      return 0
    fi
    echo "failed:tree-fetch"
    return 1
  fi

  case "$kind" in
    interpreter|compiler)
      include_impl=1
      ;;
  esac

  jq -r '.tree[]? | select(.type=="blob") | .path' "$tree_json" > "$all_paths"

  awk '
      /\.lol$/ { print; next }
      /^README(\..*)?$/ || /(^|\/)README(\..*)?$/ { print; next }
      /(^|\/)Makefile$/ || /(^|\/)Dockerfile$/ { print; next }
      /\.sh$/ || /\.tsv$/ { print; next }
    ' \
    "$all_paths" \
    > "$selected"

  if [ "$include_impl" -eq 1 ]; then
    rg -N \
      '(\.rkt$|\.scm$|\.ss$|\.py$|\.js$|\.mjs$|\.cjs$|\.ts$|\.tsx$|\.java$|\.kt$|\.kts$|\.scala$|\.rb$|\.go$|\.rs$|\.hs$|\.lhs$|\.ml$|\.mli$|\.php$|\.pl$|\.pm$|\.swift$|\.cs$|(^|/)Cargo\.toml$|(^|/)package\.json$|(^|/)pyproject\.toml$|(^|/)setup\.py$|(^|/)\.cabal$)' \
      "$all_paths" \
      >> "$selected" || true
  fi

  while IFS= read -r path; do
    [ -z "$path" ] && continue
    mkdir -p "$out/files/$(dirname "$path")"
    if ! curl -sS -L --max-time 20 "https://raw.githubusercontent.com/$repo/$branch/$path" > "$out/files/$path"; then
      file_failures=$((file_failures + 1))
    fi
  done < "$selected"

  if [ "$file_failures" -gt 0 ]; then
    echo "ok:partial:$file_failures"
  else
    echo "ok"
  fi
  return 0
}

download_repo_snapshot_via_git() {
  local tier="$1"
  local label="$2"
  local repo="$3"
  local kind="$4"
  local out="$CORPUS_ROOT/$tier/$label"
  local tmp_clone="$TMP_DIR/${tier}-${label}-clone"
  local all_paths="$TMP_DIR/${tier}-${label}-all-paths.txt"
  local selected="$TMP_DIR/${tier}-${label}-files.txt"
  local selected_uniq="$TMP_DIR/${tier}-${label}-files-uniq.txt"
  local include_impl=0
  local file_failures=0
  local branch=""
  local commit=""

  case "$kind" in
    interpreter|compiler)
      include_impl=1
      ;;
  esac

  trash_path "$out"
  mkdir -p "$out/files"

  if ! git clone --depth 1 "https://github.com/$repo.git" "$tmp_clone" >/dev/null 2>&1; then
    return 1
  fi

  branch="$(git -C "$tmp_clone" symbolic-ref --short HEAD 2>/dev/null || true)"
  commit="$(git -C "$tmp_clone" rev-parse HEAD 2>/dev/null || true)"

  jq -n \
    --arg full_name "$repo" \
    --arg default_branch "$branch" \
    --arg head_commit "$commit" \
    --arg fetched_via "git-clone-fallback" \
    '
    {
      full_name: $full_name,
      default_branch: $default_branch,
      head_commit: $head_commit,
      fetched_via: $fetched_via
    }' > "$out/metadata.json"

  git -C "$tmp_clone" ls-files > "$all_paths"

  awk '
    /\.lol$/ { print; next }
    /^README(\..*)?$/ || /(^|\/)README(\..*)?$/ { print; next }
    /(^|\/)Makefile$/ || /(^|\/)Dockerfile$/ { print; next }
    /\.sh$/ || /\.tsv$/ { print; next }
  ' "$all_paths" > "$selected"

  if [ "$include_impl" -eq 1 ]; then
    rg -N \
      '(\.rkt$|\.scm$|\.ss$|\.py$|\.js$|\.mjs$|\.cjs$|\.ts$|\.tsx$|\.java$|\.kt$|\.kts$|\.scala$|\.rb$|\.go$|\.rs$|\.hs$|\.lhs$|\.ml$|\.mli$|\.php$|\.pl$|\.pm$|\.swift$|\.cs$|(^|/)Cargo\.toml$|(^|/)package\.json$|(^|/)pyproject\.toml$|(^|/)setup\.py$|(^|/)\.cabal$)' \
      "$all_paths" \
      >> "$selected" || true
  fi

  awk 'NF && !seen[$0]++ { print }' "$selected" > "$selected_uniq"

  while IFS= read -r path; do
    [ -z "$path" ] && continue
    mkdir -p "$out/files/$(dirname "$path")"
    if ! cp "$tmp_clone/$path" "$out/files/$path" 2>/dev/null; then
      file_failures=$((file_failures + 1))
    fi
  done < "$selected_uniq"

  if [ "$file_failures" -gt 0 ]; then
    echo "ok:git-fallback:partial:$file_failures"
  else
    echo "ok:git-fallback"
  fi
  return 0
}

build_repo_annotation_json() {
  local tier="$1"
  local label="$2"
  local kind="$3"
  local status="$4"
  local source="$5"
  local repo_dir="$CORPUS_ROOT/$tier/$label/files"
  local total_files=0
  local sample_lol_files=0
  local implementation_files=0
  local capture_type="none"
  local initially_missing=false
  local recovered_from_initially_missing=false
  local recovery_state="not-applicable"
  local recovery_basis="none"

  if [ -d "$repo_dir" ]; then
    total_files="$(find "$repo_dir" -type f | wc -l | awk "{print \$1}")"
    sample_lol_files="$(find "$repo_dir" -type f -name "*.lol" | wc -l | awk "{print \$1}")"
    implementation_files="$(
      find "$repo_dir" -type f \
        | rg -N '\.(rkt|scm|ss|py|js|mjs|cjs|ts|tsx|java|kt|kts|scala|rb|go|rs|hs|lhs|ml|mli|php|pl|pm|swift|cs|c|cc|cpp|cxx|h|hh|hpp|hxx)$' \
        | wc -l \
        | awk "{print \$1}"
    )"
  fi

  if [ "$implementation_files" -gt 0 ] && [ "$sample_lol_files" -gt 0 ]; then
    capture_type="implementation+sample-code"
  elif [ "$implementation_files" -gt 0 ]; then
    capture_type="implementation-only"
  elif [ "$sample_lol_files" -gt 0 ]; then
    capture_type="sample-only"
  elif [ "$total_files" -gt 0 ]; then
    capture_type="metadata-only"
  fi

  if [ "$status" = "archive" ]; then
    initially_missing=true
    recovery_basis="archived-candidate"
    if [ "$total_files" -gt 0 ]; then
      recovered_from_initially_missing=true
      recovery_state="recovered-direct-archive"
    else
      recovery_state="initially-missing-unrecovered"
    fi
  else
    case "$source" in
      shadow-mirror-search-*)
        initially_missing=true
        recovered_from_initially_missing=true
        recovery_state="recovered-replacement-candidate"
        recovery_basis="shadow-mirror-search"
        ;;
    esac
  fi

  jq -n \
    --arg kind "$kind" \
    --arg source "$source" \
    --arg recovery_state "$recovery_state" \
    --arg recovery_basis "$recovery_basis" \
    --arg capture_type "$capture_type" \
    --argjson initially_missing "$initially_missing" \
    --argjson recovered_from_initially_missing "$recovered_from_initially_missing" \
    --argjson total_files "$total_files" \
    --argjson sample_lol_files "$sample_lol_files" \
    --argjson implementation_files "$implementation_files" \
    '
    {
      recovery_tracking: {
        initially_missing: $initially_missing,
        recovered_from_initially_missing: $recovered_from_initially_missing,
        recovery_state: $recovery_state,
        recovery_source: $source,
        recovery_basis: $recovery_basis
      },
      corpus_capture: {
        repo_kind: $kind,
        total_files: $total_files,
        sample_lol_files: $sample_lol_files,
        implementation_files: $implementation_files,
        capture_type: $capture_type
      }
    }'
}

append_entry_json() {
  local tier="$1"
  local label="$2"
  local repo="$3"
  local kind="$4"
  local oracle_priority="$5"
  local corpus_priority="$6"
  local source="$7"
  local status="$8"
  local sync_state="$9"
  local sync_note="${10}"
  local repo_annotation_json="${11}"
  local external_progress_json="${12}"

  jq -n \
    --arg tier "$tier" \
    --arg label "$label" \
    --arg repo "$repo" \
    --arg kind "$kind" \
    --arg oracle_priority "$oracle_priority" \
    --arg corpus_priority "$corpus_priority" \
    --arg source "$source" \
    --arg status "$status" \
    --arg sync_state "$sync_state" \
    --arg sync_note "$sync_note" \
    --argjson repo_annotation "$repo_annotation_json" \
    --argjson external_progress "$external_progress_json" \
    '
    {
      tier: $tier,
      label: $label,
      repo: $repo,
      kind: $kind,
      oracle_priority: $oracle_priority,
      corpus_priority: $corpus_priority,
      source: $source,
      status: $status,
      sync_state: $sync_state,
      sync_note: $sync_note,
      recovery_tracking: $repo_annotation.recovery_tracking,
      corpus_capture: $repo_annotation.corpus_capture,
      extraction_progress: (
        ($external_progress // {})
        | .external_items_total = (.external_items_total // 0)
        | .external_issues_total = (.external_issues_total // 0)
        | .external_prs_total = (.external_prs_total // 0)
        | .candidate_repros_total = (.candidate_repros_total // 0)
        | .candidate_runtime_safety_total = (.candidate_runtime_safety_total // 0)
        | .candidate_language_total = (.candidate_language_total // 0)
        | .imported_test_cases_total = (.imported_test_cases_total // 0)
        | .triage_status_counts = (.triage_status_counts // {})
        | .known_divergences_total = (.triage_status_counts["known-divergence"] // 0)
        | .known_failures_total = (
            (.triage_status_counts["known-divergence"] // 0)
            + (.triage_status_counts["spec-ambiguous"] // 0)
            + (.triage_status_counts["out-of-spec"] // 0)
          )
        | .fixed_here_total = (.triage_status_counts["fixed-here"] // 0)
        | .candidate_triage_total = (.triage_status_counts["candidate"] // 0)
      )
    }' >> "$entries_jsonl"
}

rows_path="$TMP_DIR/catalog-rows.tsv"
awk 'NF && $1 !~ /^#/' "$CATALOG_PATH" > "$rows_path"

entries_jsonl="$TMP_DIR/entries.jsonl"
: > "$entries_jsonl"

build_external_progress_index

declare -a SELECTED_TIERS=()

tier_in_selected() {
  local needle="$1"
  local t
  for t in "${SELECTED_TIERS[@]}"; do
    if [ "$t" = "$needle" ]; then
      return 0
    fi
  done
  return 1
}

while IFS=$'\t' read -r tier label repo kind oracle_priority corpus_priority source status; do
  [ -z "$tier" ] && continue

  if ! matches_requested_tier "$tier"; then
    continue
  fi

  if ! tier_in_selected "$tier"; then
    SELECTED_TIERS+=("$tier")
  fi

  external_progress_json="$(jq -c --arg repo "$repo" '.[$repo] // {}' "$EXTERNAL_PROGRESS_INDEX_PATH")"

  if [ "$status" = "archive" ]; then
    repo_annotation_json="$(build_repo_annotation_json "$tier" "$label" "$kind" "$status" "$source")"
    append_entry_json \
      "$tier" "$label" "$repo" "$kind" \
      "$oracle_priority" "$corpus_priority" "$source" "$status" \
      "skipped" "archive-entry" \
      "$repo_annotation_json" "$external_progress_json"
    continue
  fi

  sync_note="$(download_repo_snapshot "$tier" "$label" "$repo" "$kind" || true)"
  sync_state="ok"
  case "$sync_note" in
    ok|ok:partial:*|ok:git-fallback|ok:git-fallback:partial:*)
      sync_state="ok"
      ;;
    failed:*)
      sync_state="failed"
      ;;
    *)
      sync_state="failed"
      [ -z "$sync_note" ] && sync_note="failed:unknown"
      ;;
  esac

  repo_annotation_json="$(build_repo_annotation_json "$tier" "$label" "$kind" "$status" "$source")"
  append_entry_json \
    "$tier" "$label" "$repo" "$kind" \
    "$oracle_priority" "$corpus_priority" "$source" "$status" \
    "$sync_state" "$sync_note" \
    "$repo_annotation_json" "$external_progress_json"
done < "$rows_path"

if [ "${#SELECTED_TIERS[@]}" -eq 0 ]; then
  echo "No matching tiers selected. Available tiers are defined in $CATALOG_PATH." >&2
  exit 1
fi

now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -s \
  --arg generated_at "$now" \
  --arg catalog "corpus/tier2/CANDIDATE_REPOS.tsv" \
  '
  {
    generated_at: $generated_at,
    catalog: $catalog,
    entries: .
  }' \
  "$entries_jsonl" \
  > "$CORPUS_ROOT/manifest.json"

generate_feature_profile() {
  local tier="$1"
  local out="$CORPUS_ROOT/$tier/FEATURE_PROFILE.md"
  local summary_json
  local recovered_total=0
  local recovered_impl_sample_total=0
  local recovered_sample_only_total=0
  local candidate_repros_total=0
  local imported_test_cases_total=0
  local known_failures_total=0
  local known_divergences_total=0

  mkdir -p "$CORPUS_ROOT/$tier"

  summary_json="$(
    jq -c \
      --arg tier "$tier" \
      '
      {
        recovered_total: ([.entries[] | select(.tier == $tier and (.recovery_tracking.recovered_from_initially_missing // false))] | length),
        recovered_impl_sample_total: ([.entries[] | select(.tier == $tier and (.recovery_tracking.recovered_from_initially_missing // false) and ((.corpus_capture.capture_type // "") == "implementation+sample-code"))] | length),
        recovered_sample_only_total: ([.entries[] | select(.tier == $tier and (.recovery_tracking.recovered_from_initially_missing // false) and ((.corpus_capture.capture_type // "") == "sample-only"))] | length),
        candidate_repros_total: ([.entries[] | select(.tier == $tier) | (.extraction_progress.candidate_repros_total // 0)] | add // 0),
        imported_test_cases_total: ([.entries[] | select(.tier == $tier) | (.extraction_progress.imported_test_cases_total // 0)] | add // 0),
        known_failures_total: ([.entries[] | select(.tier == $tier) | (.extraction_progress.known_failures_total // 0)] | add // 0),
        known_divergences_total: ([.entries[] | select(.tier == $tier) | (.extraction_progress.known_divergences_total // 0)] | add // 0)
      }
      ' \
      "$CORPUS_ROOT/manifest.json"
  )"

  recovered_total="$(printf '%s' "$summary_json" | jq -r '.recovered_total // 0')"
  recovered_impl_sample_total="$(printf '%s' "$summary_json" | jq -r '.recovered_impl_sample_total // 0')"
  recovered_sample_only_total="$(printf '%s' "$summary_json" | jq -r '.recovered_sample_only_total // 0')"
  candidate_repros_total="$(printf '%s' "$summary_json" | jq -r '.candidate_repros_total // 0')"
  imported_test_cases_total="$(printf '%s' "$summary_json" | jq -r '.imported_test_cases_total // 0')"
  known_failures_total="$(printf '%s' "$summary_json" | jq -r '.known_failures_total // 0')"
  known_divergences_total="$(printf '%s' "$summary_json" | jq -r '.known_divergences_total // 0')"

  {
    echo "# $tier Feature Profile"
    echo
    echo "Generated: \`$now\`"
    echo
    echo "## Recovery + Extraction Summary"
    echo
    echo "- Recovered from initially-missing set: \`$recovered_total\`"
    echo "- Recovered with implementation+sample code: \`$recovered_impl_sample_total\`"
    echo "- Recovered with sample-only capture: \`$recovered_sample_only_total\`"
    echo "- Bugs extracted (candidate repro items): \`$candidate_repros_total\`"
    echo "- Test cases extracted (imported external fixtures): \`$imported_test_cases_total\`"
    echo "- Known failures (triaged unresolved): \`$known_failures_total\`"
    echo "- Known divergences: \`$known_divergences_total\`"
    echo
  } > "$out"

  while IFS=$'\t' read -r row_tier label repo kind oracle_priority corpus_priority source status; do
    [ -z "$row_tier" ] && continue
    [ "$row_tier" != "$tier" ] && continue

    local entry_json
    local repo_dir="$CORPUS_ROOT/$tier/$label/files"
    local lol_count=0
    local line_count=0
    local recovered_from_initially_missing="false"
    local recovery_state="unknown"
    local capture_type="none"
    local implementation_files=0
    local candidate_repros=0
    local imported_test_cases=0
    local known_failures=0
    local known_divergences=0

    if [ -d "$repo_dir" ]; then
      lol_count="$(find "$repo_dir" -type f -name "*.lol" | wc -l | awk "{print \$1}")"
      if [ "$lol_count" -gt 0 ]; then
        line_count="$(find "$repo_dir" -type f -name "*.lol" -print0 | xargs -0 cat | wc -l | awk "{print \$1}")"
      fi
    fi

    entry_json="$(
      jq -c \
        --arg tier "$tier" \
        --arg label "$label" \
        '.entries[] | select(.tier == $tier and .label == $label)' \
        "$CORPUS_ROOT/manifest.json" \
        | sed -n '1p'
    )"

    if [ -n "$entry_json" ]; then
      recovered_from_initially_missing="$(printf '%s' "$entry_json" | jq -r '.recovery_tracking.recovered_from_initially_missing // false')"
      recovery_state="$(printf '%s' "$entry_json" | jq -r '.recovery_tracking.recovery_state // "unknown"')"
      capture_type="$(printf '%s' "$entry_json" | jq -r '.corpus_capture.capture_type // "none"')"
      implementation_files="$(printf '%s' "$entry_json" | jq -r '.corpus_capture.implementation_files // 0')"
      candidate_repros="$(printf '%s' "$entry_json" | jq -r '.extraction_progress.candidate_repros_total // 0')"
      imported_test_cases="$(printf '%s' "$entry_json" | jq -r '.extraction_progress.imported_test_cases_total // 0')"
      known_failures="$(printf '%s' "$entry_json" | jq -r '.extraction_progress.known_failures_total // 0')"
      known_divergences="$(printf '%s' "$entry_json" | jq -r '.extraction_progress.known_divergences_total // 0')"
    fi

    {
      echo "## $label"
      echo
      echo "- Repo: \`$repo\`"
      echo "- Kind: \`$kind\`"
      echo "- Status: \`$status\`"
      echo "- Recovered from initially-missing set: \`$recovered_from_initially_missing\`"
      echo "- Recovery state: \`$recovery_state\`"
      echo "- Capture type: \`$capture_type\`"
      echo "- Captured implementation files: \`$implementation_files\`"
      echo "- LOLCODE files: \`$lol_count\`"
      echo "- Total LOLCODE lines: \`$line_count\`"
      echo "- Bugs extracted (candidate repro items): \`$candidate_repros\`"
      echo "- Test cases extracted (imported fixtures): \`$imported_test_cases\`"
      echo "- Known failures (triaged unresolved): \`$known_failures\`"
      echo "- Known divergences: \`$known_divergences\`"
      echo
      echo "| Construct | Count |"
      echo "| --- | ---: |"
    } >> "$out"

    for pattern in "${FEATURE_PATTERNS[@]}"; do
      local count=0
      if [ "$lol_count" -gt 0 ]; then
        count="$(
          find "$repo_dir" -type f -name "*.lol" -print0 \
            | xargs -0 rg -o -N "$pattern" \
            | wc -l \
            | awk "{print \$1}" \
            || true
        )"
      fi
      if [ "$count" -gt 0 ]; then
        printf '| `%s` | %s |\n' "$pattern" "$count" >> "$out"
      fi
    done
    echo >> "$out"
  done < "$rows_path"
}

for tier in "${SELECTED_TIERS[@]}"; do
  mkdir -p "$CORPUS_ROOT/$tier"

  jq \
    --arg tier "$tier" \
    --arg generated_at "$now" \
    '
    {
      generated_at: $generated_at,
      tier: $tier,
      entries: [.entries[] | select(.tier == $tier)]
    }' \
    "$CORPUS_ROOT/manifest.json" \
    > "$CORPUS_ROOT/$tier/manifest.json"

  generate_feature_profile "$tier"
done

echo "Synced corpus tiers: ${SELECTED_TIERS[*]}"
echo "Manifest: $CORPUS_ROOT/manifest.json"
