#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$REPO_ROOT/corpus/research/github_language_lolcode"
REPOS_JSON="$DISCOVERY_DIR/repos.json"
SUMMARY_JSON="$DISCOVERY_DIR/summary.json"
TOP_N="${TOP_N:-50}"
SOURCE_TAG="${SOURCE_TAG:-github-language-lolcode-curated-$(date -u +%F)}"

OUT_SCORED_JSON="$DISCOVERY_DIR/curation_scored.json"
OUT_ALL_TSV="$DISCOVERY_DIR/curated_candidates.tsv"
OUT_TOP_TSV="$DISCOVERY_DIR/curated_top50.tsv"
OUT_EXCLUDED_TSV="$DISCOVERY_DIR/excluded_noise.tsv"
OUT_REPORT_MD="$DISCOVERY_DIR/CURATION_REPORT.md"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/curate_github_language_lolcode_candidates.sh
  ./scripts/curate_github_language_lolcode_candidates.sh --top 75
  ./scripts/curate_github_language_lolcode_candidates.sh --source-tag custom-tag

Inputs:
  - corpus/research/github_language_lolcode/repos.json
  - corpus/research/github_language_lolcode/summary.json (optional)

Outputs:
  - corpus/research/github_language_lolcode/curation_scored.json
  - corpus/research/github_language_lolcode/curated_candidates.tsv
  - corpus/research/github_language_lolcode/curated_top50.tsv
  - corpus/research/github_language_lolcode/excluded_noise.tsv
  - corpus/research/github_language_lolcode/CURATION_REPORT.md
EOF
}

is_posint() {
  [[ "$1" =~ ^[0-9]+$ ]] && [ "$1" -gt 0 ]
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --top)
      [ "$#" -lt 2 ] && { echo "Missing value for --top" >&2; exit 2; }
      TOP_N="$2"
      shift 2
      ;;
    --source-tag)
      [ "$#" -lt 2 ] && { echo "Missing value for --source-tag" >&2; exit 2; }
      SOURCE_TAG="$2"
      shift 2
      ;;
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

if ! command -v jq >/dev/null 2>&1; then
  echo "Missing required command: jq" >&2
  exit 1
fi

is_posint "$TOP_N" || { echo "--top must be a positive integer" >&2; exit 2; }

[ -f "$REPOS_JSON" ] || {
  echo "Missing input: $REPOS_JSON" >&2
  echo "Run ./scripts/sync_github_language_lolcode.sh first." >&2
  exit 1
}

SELF_REPO=""
if remote_url="$(git config --get remote.origin.url 2>/dev/null || true)"; then
  if [[ "$remote_url" =~ github\.com[:/]([^/]+/[^/.]+)(\.git)?$ ]]; then
    SELF_REPO="${BASH_REMATCH[1]}"
  fi
fi

jq --arg self_repo "$SELF_REPO" '
  def reason($flag; $msg):
    if $flag then [$msg] else [] end;
  def to_label:
    ascii_downcase
    | gsub("[^a-z0-9]+"; "-")
    | gsub("^-+"; "")
    | gsub("-+$"; "");

  def repo_lc: (.repo | ascii_downcase);
  def path_blob: (.sample_paths | map(ascii_downcase) | join(" "));

  map(
    . as $r
    | (repo_lc) as $repo_lc
    | (path_blob) as $paths
    | ($r.code_hit_count // 0) as $hits
    | ($r.stars // 0) as $stars
    | ($r.in_catalog // false) as $in_catalog
    | (($self_repo != "") and ($r.repo == $self_repo)) as $is_self
    | ($repo_lc | test("(^|/)(lolcode|loljs|lolcomp|lolterpreter|lolcodec?|lolc|lci|lulz|layo|eulol|loleuler|lollm)(-|$|/)")) as $repo_lol_signal
    | ($repo_lc | test("interpreter|compiler|parser")) as $repo_impl_signal
    | ($paths | test("(^|/)1\\.3-tests/|(^|/)test/|(^|/)tests/|(^|/)examples?/|(^|/)sample|project-testcases|interpreter|compiler|parser|spec/")) as $path_test_signal
    | ($paths | test("\\.lol$|\\.lol;|\\.lolcode$|\\.lci\\.lol")) as $path_lol_signal
    | ($repo_lc | test("aoc|advent|portfolio|dataset|templates|hello-world|wuhan|iiser|chemistry|electrical|bio|mongodb|fizzbuzz|fibonacci|record|roadside|ctf|challenges")) as $repo_noise_signal
    | ($paths | test("proteinsparams|/record/|language-dataset|advent|aoc|chemistry|electrical|bio|hello-world|templates|wuhan|roadside|mongodb|ctf|challenges")) as $path_noise_signal
    | ($paths | test("src/lci/test/1\\.3-tests/")) as $embedded_lci_fixture_signal
    | (reason($repo_lol_signal; "repo-name-lolcode-signal")
       + reason($repo_impl_signal; "repo-name-impl-signal")
       + reason($path_test_signal; "path-test-or-example-signal")
       + reason($path_lol_signal; "path-lol-extension-signal")
      ) as $positive
    | (reason($repo_noise_signal; "repo-name-noise-signal")
       + reason($path_noise_signal; "path-noise-signal")
       + reason($embedded_lci_fixture_signal; "embedded-lci-fixtures-signal")
      ) as $negative
    | (
        $hits
        + (if $repo_lol_signal then 18 else 0 end)
        + (if $repo_impl_signal then 8 else 0 end)
        + (if $path_test_signal then 8 else 0 end)
        + (if $path_lol_signal then 6 else 0 end)
        + (if $stars > 0 then (if $stars > 10 then 6 else 2 end) else 0 end)
        - (if $repo_noise_signal then 22 else 0 end)
        - (if $path_noise_signal then 18 else 0 end)
        - (if $embedded_lci_fixture_signal then 14 else 0 end)
      ) as $score
    | ($hits > 0
       and $score >= 18
       and ($in_catalog | not)
       and ($is_self | not)
       and (($hits <= 2 and ($repo_noise_signal or $path_noise_signal)) | not)
      ) as $include
    | $r + {
        label: ($r.repo | to_label),
        curation_score: $score,
        include_candidate: $include,
        is_self_repo: $is_self,
        positive_reasons: $positive,
        negative_reasons: $negative
      }
  )
  | sort_by(-.curation_score, -.code_hit_count, -.stars, .repo)
' "$REPOS_JSON" > "$OUT_SCORED_JSON"

{
  printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tcode_hit_count\tstars\thtml_url\tpositive_reasons\tnegative_reasons\n'
  jq -r --arg source_tag "$SOURCE_TAG" '
    [ .[] | select(.include_candidate) ]
    | .[]
    | [
        "tier2",
        .label,
        .repo,
        (if (.positive_reasons | index("repo-name-impl-signal")) then "interpreter" else "corpus" end),
        (if (.positive_reasons | index("repo-name-impl-signal")) then "P2" else "P3" end),
        "P2",
        $source_tag,
        "curated-discovered",
        (.curation_score | tostring),
        (.code_hit_count | tostring),
        (.stars | tostring),
        .html_url,
        (.positive_reasons | join(",")),
        (.negative_reasons | join(","))
      ] | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_ALL_TSV"

{
  printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tcode_hit_count\tstars\thtml_url\tpositive_reasons\tnegative_reasons\n'
  jq -r --arg source_tag "$SOURCE_TAG" --argjson top_n "$TOP_N" '
    [ .[] | select(.include_candidate) ]
    | .[:$top_n]
    | .[]
    | [
        "tier2",
        .label,
        .repo,
        (if (.positive_reasons | index("repo-name-impl-signal")) then "interpreter" else "corpus" end),
        (if (.positive_reasons | index("repo-name-impl-signal")) then "P2" else "P3" end),
        "P2",
        $source_tag,
        "curated-discovered",
        (.curation_score | tostring),
        (.code_hit_count | tostring),
        (.stars | tostring),
        .html_url,
        (.positive_reasons | join(",")),
        (.negative_reasons | join(","))
      ] | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_TOP_TSV"

{
  printf 'repo\tcuration_score\tcode_hit_count\tstars\thtml_url\treasons\n'
  jq -r '
    [ .[] | select(.include_candidate | not) | select(.in_catalog | not) | select(.is_self_repo | not) ]
    | .[]
    | [
        .repo,
        (.curation_score | tostring),
        (.code_hit_count | tostring),
        (.stars | tostring),
        .html_url,
        ((.negative_reasons + (if (.include_candidate | not) then ["below-threshold-or-hard-excluded"] else [] end)) | unique | join(","))
      ] | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_EXCLUDED_TSV"

total_new=0
if [ -f "$SUMMARY_JSON" ]; then
  total_new="$(jq -r '.totals.repos_new_not_in_catalog // 0' "$SUMMARY_JSON" 2>/dev/null || echo 0)"
fi

included_count="$(jq '[.[] | select(.include_candidate)] | length' "$OUT_SCORED_JSON")"
excluded_count="$(jq '[.[] | select(.include_candidate | not) | select(.in_catalog | not) | select(.is_self_repo | not)] | length' "$OUT_SCORED_JSON")"

{
  echo "# GitHub LOLCODE Curation Report"
  echo
  echo "- Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo "- Source snapshot: \`corpus/research/github_language_lolcode/repos.json\`"
  echo "- Total new repos in discovery snapshot: \`$total_new\`"
  echo "- Included by curation heuristics: \`$included_count\`"
  echo "- Excluded/not-selected: \`$excluded_count\`"
  echo "- Top preview cap: \`$TOP_N\`"
  echo
  echo "## Heuristic Summary"
  echo
  echo "- Positive signals: repo-name LOLCODE/impl markers, test/example path structure, \`.lol\` path evidence."
  echo "- Negative signals: obvious non-LOLCODE domains (AoC/dataset/record/template/etc), embedded third-party fixture copies."
  echo "- Final gate: score threshold + hard exclusion for very-low-hit noisy repos."
  echo
  echo "## Top Included Candidates"
  echo
  echo "| Repo | Score | Hits | Stars | Reasons |"
  echo "|---|---:|---:|---:|---|"
  jq -r --argjson top_n "$TOP_N" '
    [ .[] | select(.include_candidate) ]
    | .[:$top_n]
    | .[]
    | "| `\(.repo)` | \(.curation_score) | \(.code_hit_count) | \(.stars) | \((.positive_reasons | join(", "))) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo "## Output Files"
  echo
  echo "- \`corpus/research/github_language_lolcode/curation_scored.json\`"
  echo "- \`corpus/research/github_language_lolcode/curated_candidates.tsv\` (all included candidates)"
  echo "- \`corpus/research/github_language_lolcode/curated_top50.tsv\`"
  echo "- \`corpus/research/github_language_lolcode/excluded_noise.tsv\` (all excluded candidates)"
} > "$OUT_REPORT_MD"

echo "wrote $OUT_REPORT_MD"
echo "wrote $OUT_ALL_TSV"
echo "wrote $OUT_TOP_TSV"
