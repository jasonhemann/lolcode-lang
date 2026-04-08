#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT_TSV="$REPO_ROOT/corpus/research/github_repo_search_lolcode/priority_candidates.tsv"
CATALOG_TSV="$REPO_ROOT/corpus/tier2/CANDIDATE_REPOS.tsv"
REPORT_MD="$REPO_ROOT/corpus/research/github_repo_search_lolcode/PROMOTION_REPORT.md"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/promote-github-repo-search.XXXXXX")"

cleanup_tmp() {
  rm -f "$TMP_DIR"/* 2>/dev/null || true
  rmdir "$TMP_DIR" 2>/dev/null || true
}
trap cleanup_tmp EXIT

usage() {
  cat <<'EOF'
Usage:
  ./scripts/promote_github_repo_search_lolcode_candidates.sh

Reads the broad-search priority queue and appends eligible rows into:
  - corpus/tier2/CANDIDATE_REPOS.tsv

Also writes:
  - corpus/research/github_repo_search_lolcode/PROMOTION_REPORT.md
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for cmd in awk sort date; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

[ -f "$INPUT_TSV" ] || {
  echo "Missing input: $INPUT_TSV" >&2
  echo "Run ./scripts/curate_github_repo_search_lolcode.sh first." >&2
  exit 1
}

[ -f "$CATALOG_TSV" ] || {
  echo "Missing catalog: $CATALOG_TSV" >&2
  exit 1
}

expected_header=$'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tstars\tcode_hit_count\thtml_url\treasons\tdiscovery_kind\tsubkind\tbucket'
actual_header="$(head -n 1 "$INPUT_TSV")"
[ "$actual_header" = "$expected_header" ] || {
  echo "Unexpected input header in $INPUT_TSV" >&2
  echo "Run ./scripts/curate_github_repo_search_lolcode.sh with the current script first." >&2
  exit 1
}

existing_repos="$TMP_DIR/existing-repos.txt"
eligible_rows="$TMP_DIR/eligible-rows.tsv"
added_rows="$TMP_DIR/added-rows.tsv"
duplicate_rows="$TMP_DIR/duplicate-rows.tsv"
non_catalog_rows="$TMP_DIR/non-catalog-rows.tsv"
new_catalog="$TMP_DIR/CANDIDATE_REPOS.tsv"

awk -F '\t' 'NF && $1 !~ /^#/ { print $3 }' "$CATALOG_TSV" > "$existing_repos"

{
  printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tstars\tcode_hit_count\thtml_url\treasons\tdiscovery_kind\tsubkind\tbucket\n'
  awk -F '\t' '
    NR == 1 { next }
    $16 == "obvious-keep" && ($14 == "implementation" || $14 == "corpus") { print }
  ' "$INPUT_TSV" \
    | sort -t "$(printf '\t')" -k9,9nr -k10,10nr -k11,11nr -k3,3
} > "$eligible_rows"

{
  printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tstars\tcode_hit_count\thtml_url\treasons\tdiscovery_kind\tsubkind\tbucket\n'
  awk -F '\t' '
    NR == 1 { next }
    $16 == "obvious-keep" && !($14 == "implementation" || $14 == "corpus") { print }
  ' "$INPUT_TSV" \
    | sort -t "$(printf '\t')" -k9,9nr -k10,10nr -k11,11nr -k3,3
} > "$non_catalog_rows"

printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\n' > "$added_rows"
printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tstars\tcode_hit_count\thtml_url\treasons\tdiscovery_kind\tsubkind\tbucket\n' > "$duplicate_rows"

while IFS=$'\t' read -r tier label repo kind oracle_priority corpus_priority source status curation_score stars code_hit_count html_url reasons discovery_kind subkind bucket; do
  [ -n "${tier:-}" ] || continue
  if grep -Fqx "$repo" "$existing_repos"; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$tier" "$label" "$repo" "$kind" "$oracle_priority" "$corpus_priority" "$source" "$status" \
      "$curation_score" "$stars" "$code_hit_count" "$html_url" "$reasons" "$discovery_kind" "$subkind" "$bucket" \
      >> "$duplicate_rows"
    continue
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$tier" "$label" "$repo" "$kind" "$oracle_priority" "$corpus_priority" "$source" "$status" \
    >> "$added_rows"
  printf '%s\n' "$repo" >> "$existing_repos"
done < <(awk 'NR > 1 { print }' "$eligible_rows")

cp "$CATALOG_TSV" "$new_catalog"
if [ "$(wc -l < "$added_rows")" -gt 1 ]; then
  awk 'NR > 1 { print }' "$added_rows" >> "$new_catalog"
fi
mv "$new_catalog" "$CATALOG_TSV"

added_count=$(( $(wc -l < "$added_rows") - 1 ))
duplicate_count=$(( $(wc -l < "$duplicate_rows") - 1 ))
non_catalog_count=$(( $(wc -l < "$non_catalog_rows") - 1 ))
generated_at="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

{
  echo '# Broad GitHub `lolcode` Promotion Report'
  echo
  printf -- '- Generated: %s\n' "$generated_at"
  echo "- Source queue: \`corpus/research/github_repo_search_lolcode/priority_candidates.tsv\`"
  echo "- Catalog updated: \`corpus/tier2/CANDIDATE_REPOS.tsv\`"
  printf -- '- Added rows: `%s`\n' "$added_count"
  printf -- '- Skipped as duplicates: `%s`\n' "$duplicate_count"
  printf -- '- Obvious-keep rows intentionally not promoted because they are non-catalog kinds: `%s`\n' "$non_catalog_count"
  echo

  echo '## Added Rows'
  echo
  echo '| Repo | Kind | Oracle | Corpus | Source |'
  echo '|---|---|---|---|---|'
  awk -F '\t' '
    NR > 1 {
      printf "| `%s` | `%s` | `%s` | `%s` | `%s` |\n",
        $3, $4, $5, $6, $7
    }
  ' "$added_rows"
  echo

  echo '## Duplicate Rows'
  echo
  echo '| Repo | Kind | Discovery Kind | Bucket |'
  echo '|---|---|---|---|'
  awk -F '\t' '
    NR > 1 {
      printf "| `%s` | `%s` | `%s` | `%s` |\n",
        $3, $4, $14, $16
    }
  ' "$duplicate_rows"
  echo

  echo '## Obvious-Keep Non-Catalog Kinds'
  echo
  echo '| Repo | Discovery Kind | Subkind | Bucket |'
  echo '|---|---|---|---|'
  awk -F '\t' '
    NR > 1 {
      printf "| `%s` | `%s` | `%s` | `%s` |\n",
        $3, $14, $15, $16
    }
  ' "$non_catalog_rows"
} > "$REPORT_MD"

echo "wrote $REPORT_MD"
echo "updated $CATALOG_TSV"
