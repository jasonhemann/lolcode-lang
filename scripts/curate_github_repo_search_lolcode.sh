#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$REPO_ROOT/corpus/research/github_repo_search_lolcode"
REPOS_JSON="$DISCOVERY_DIR/repos.json"
ENRICHED_JSON="$DISCOVERY_DIR/repos_enriched.json"
SUMMARY_JSON="$DISCOVERY_DIR/summary.json"
SOURCE_TAG="${SOURCE_TAG:-github-repo-search-lolcode-curated-$(date -u +%F)}"

OUT_SCORED_JSON="$DISCOVERY_DIR/curation_scored.json"
OUT_ALL_TSV="$DISCOVERY_DIR/classified_repos.tsv"
OUT_PRIORITY_TSV="$DISCOVERY_DIR/priority_candidates.tsv"
OUT_OBVIOUS_TSV="$DISCOVERY_DIR/obvious_keep.tsv"
OUT_MANUAL_TSV="$DISCOVERY_DIR/manual_review.tsv"
OUT_UNLIKELY_TSV="$DISCOVERY_DIR/unlikely_keep.tsv"
OUT_REPORT_MD="$DISCOVERY_DIR/CURATION_REPORT.md"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/curate_github_repo_search_lolcode.sh
  ./scripts/curate_github_repo_search_lolcode.sh --source-tag custom-tag

Inputs:
  - corpus/research/github_repo_search_lolcode/repos.json
  - corpus/research/github_repo_search_lolcode/repos_enriched.json (preferred if present)
  - corpus/research/github_repo_search_lolcode/summary.json (optional)

Outputs:
  - corpus/research/github_repo_search_lolcode/curation_scored.json
  - corpus/research/github_repo_search_lolcode/classified_repos.tsv
  - corpus/research/github_repo_search_lolcode/priority_candidates.tsv
  - corpus/research/github_repo_search_lolcode/obvious_keep.tsv
  - corpus/research/github_repo_search_lolcode/manual_review.tsv
  - corpus/research/github_repo_search_lolcode/unlikely_keep.tsv
  - corpus/research/github_repo_search_lolcode/CURATION_REPORT.md
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
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

[ -f "$REPOS_JSON" ] || {
  echo "Missing input: $REPOS_JSON" >&2
  echo "Run ./scripts/sync_github_repo_search_lolcode.sh first." >&2
  exit 1
}

INPUT_JSON="$REPOS_JSON"
if [ -f "$ENRICHED_JSON" ]; then
  INPUT_JSON="$ENRICHED_JSON"
fi

jq '
  def reason($flag; $msg):
    if $flag then [$msg] else [] end;

  def repo_lc: (.repo | ascii_downcase);
  def repo_name_lc: (.repo | split("/") | .[1] | ascii_downcase);
  def desc_lc: ((.description // "") | ascii_downcase);
  def language_lc: ((.language // "") | ascii_downcase);
  def topics_lc: ((.topics // []) | map(ascii_downcase) | join(" "));
  def root_blob: ((.root_names // []) | map(ascii_downcase) | join(" "));

  map(
    . as $r
    | (repo_lc) as $repo_lc
    | (repo_name_lc) as $repo_name_lc
    | (desc_lc) as $desc_lc
    | (language_lc) as $lang_lc
    | (topics_lc) as $topics_lc
    | (root_blob) as $root_blob
    | ($r.stars // 0) as $stars
    | ($r.code_hit_count // 0) as $hits
    | (
        ($repo_name_lc | test("vscode|vim|mode|tmlanguage|npp|gtksourceview|textmate"))
        or ($desc_lc | test("language support|syntax highlighting|syntax highlight|editor extension|editor support"))
        or ($topics_lc | test("vscode|vim|syntax|extension"))
        or ($root_blob | test("syntaxes|language-configuration.json|package.json|lol.xshd|\\.vim|tmlanguage"))
      ) as $editor_tooling_signal
    | (
        ($repo_name_lc | test("playground|action|macro|dsl"))
        or ($desc_lc | test("github action|babel macro|dsl|playground"))
      ) as $aux_tooling_signal
    | (
        ($repo_name_lc | test("spec|reference|docs|docsite|guide"))
        or ($desc_lc | test("reference|documentation|specification|spec\\b|manual|tutorial"))
      ) as $docs_signal
    | (
        ($r.root_fetch_ok // false)
        and (($r.root_entry_count // 0) == 0)
      ) as $empty_root_signal
    | (
        ($root_blob
         | test("cargo.toml|cargo.lock|\\.sln|\\.csproj|pom.xml|build.gradle|makefile|src|main.py|build.sh|build.bat"))
      ) as $code_root_signal
    | (
        ($root_blob | test("grammar\\.ebnf|\\.g4|\\.l(,|$)|\\.y(,|$)|lexer|parser"))
      ) as $grammar_root_signal
    | (
        ($root_blob
         | test("grammar\\.ebnf|\\.g4|\\.l(,|$)|\\.y(,|$)|parser|lexer|interpreter\\.cs|compiler|runtime|evaluator|transpil|translator"))
      ) as $impl_root_signal
    | (
        ($root_blob | test("^readme(\\.md|\\.txt)?(, |$)|(^|, )license(|\\.txt)(, |$)|(^|, )copying(, |$)|(^|, )spec\\.txt(, |$)"))
        and ($code_root_signal | not)
        and ($editor_tooling_signal | not)
        and (($r.root_entry_count // 0) <= 4)
      ) as $docs_only_root_signal
    | (
        ($desc_lc
         | test("installs .* interpreter|github action installs|language support for|syntax highlighting|syntax highlighter"))
      ) as $desc_not_impl_signal
    | (
        $editor_tooling_signal or $aux_tooling_signal
      ) as $tooling_signal
    | (
        ($docs_signal or $docs_only_root_signal)
      ) as $docs_signal2
    | (
        ($desc_lc | test("interpreter|compiler|parser|transpil|translator|runtime"))
      ) as $weak_impl_signal
    | (
        ($repo_name_lc | test("(^|[-_.])(interpreter|compiler|parser|transpil|translator|protointerpreter|runtime)($|[-_.])"))
        or ($repo_name_lc | test("^(lci|rlci|hlci|lulz|layo|lolcomp|lolterpreter|lolc|lolcodec|lolcode-rb|clj-lolcode|lolcode-dot-net|dotnet-lolcode|lolsharp|ruby2lolz)$"))
        or ($repo_name_lc | test("to[-_]?c|2cplusplus|antlr|sharp|llvm"))
        or $impl_root_signal
        or ($code_root_signal
            and $weak_impl_signal
            and ($tooling_signal | not)
            and ($docs_signal2 | not)
            and ($desc_not_impl_signal | not))
        or (($repo_name_lc == "lolcode") and ($lang_lc != "lolcode") and ($lang_lc != ""))
      ) as $strong_impl_signal
    | (
        $strong_impl_signal
        or ($weak_impl_signal
            and ($tooling_signal | not)
            and ($docs_signal2 | not)
            and ($desc_not_impl_signal | not))
      ) as $implementation_signal
    | (
        ($lang_lc == "lolcode")
        or ($hits > 0)
        or ($root_blob | test("\\.lol(,|$)|examples?|testcases|tests|perfs|benchmark|bench|samples?"))
        or ($repo_name_lc | test("examples|example|snake|equation|fibonacci|matrix|game|calculator|tictactoe|ttt|json|quine|samples?"))
      ) as $corpus_signal
    | (
        ($repo_name_lc | test("ctf|challenge|portfolio|dataset|archive|template|course|thesis|hello-world|helloworld|learning-progress|browser"))
        or ($desc_lc | test("challenge|course|dataset|portfolio|template"))
        or ($empty_root_signal and ($stars == 0) and ($hits == 0))
      ) as $noise_signal
    | (if $docs_signal2 and ($implementation_signal | not) then "docs"
       elif $tooling_signal and ($implementation_signal | not) then "tooling"
       elif $implementation_signal then "implementation"
       elif $corpus_signal then "corpus"
       else "noise"
       end) as $kind
    | (if $kind == "implementation"
          and (($repo_name_lc | test("parser|antlr")) or $grammar_root_signal)
       then "parser"
       elif $kind == "implementation"
            and (($repo_name_lc | test("compiler|llvm|jvm"))
                 or ($desc_lc | test("compiler|jvm|llvm")))
       then "compiler"
       elif $kind == "implementation"
            and (($repo_name_lc
                  | test("transpil|translator|to[-_]?c|2cplusplus"))
                 or ($desc_lc | test("transpil|translator")))
       then "transpiler"
       elif $kind == "implementation"
            and (($repo_name_lc | test("dsl|macro"))
                 or ($desc_lc | test("\\bdsl\\b|macro")))
       then "dsl"
       elif $kind == "implementation" then "interpreter"
       elif $kind == "tooling" then "tooling"
       elif $kind == "docs" then "docs"
       elif $kind == "corpus" then "corpus"
       else "noise"
       end) as $subkind
    | (
        $hits
        + (if $implementation_signal then 24 else 0 end)
        + (if $grammar_root_signal then 6 else 0 end)
        + (if $tooling_signal then 12 else 0 end)
        + (if $docs_signal2 then 8 else 0 end)
        + (if $corpus_signal then 10 else 0 end)
        + (if $stars > 0 then (if $stars > 10 then 8 else 3 end) else 0 end)
        - (if ($noise_signal and ($implementation_signal | not)) then 16 else 0 end)
      ) as $score
    | (
        if $kind == "implementation" then "P1"
        elif $kind == "tooling" then "P2"
        elif $kind == "docs" then "P2"
        elif $kind == "corpus" then "P3"
        else "P4"
        end
      ) as $priority
    | (
        reason($implementation_signal; "implementation-signal")
        + reason($impl_root_signal; "impl-root-signal")
        + reason($grammar_root_signal; "grammar-root-signal")
        + reason($tooling_signal; "tooling-signal")
        + reason($docs_signal2; "docs-signal")
        + reason($corpus_signal; "corpus-signal")
        + reason($noise_signal; "noise-signal")
        + reason($r.in_language_snapshot; "also-in-language-snapshot")
        + reason($r.in_candidate_catalog; "already-in-candidate-catalog")
      ) as $reasons
    | (
        if $r.in_candidate_catalog then "already-tracked"
        elif ($kind == "noise") then "unlikely-keep"
        elif ($kind == "implementation"
              and (($hits >= 2)
                   or ($stars >= 3)
                   or $r.in_language_snapshot
                   or $grammar_root_signal)) then "obvious-keep"
        elif ($kind == "corpus"
              and (($hits >= 2)
                   or ($stars >= 3))) then "obvious-keep"
        elif (($kind == "tooling" or $kind == "docs")
              and (($stars >= 5)
                   or ($hits >= 2)
                   or $r.in_language_snapshot)) then "manual-review"
        elif (($stars == 0)
              and ($hits == 0)
              and ($r.in_language_snapshot | not)
              and ($kind != "implementation")) then "unlikely-keep"
        else "manual-review"
        end
      ) as $bucket
    | $r + {
        kind: $kind,
        subkind: $subkind,
        priority: $priority,
        bucket: $bucket,
        curation_score: $score,
        include_candidate:
          ((.in_candidate_catalog | not)
           and ($kind != "noise")
           and (($noise_signal and ($implementation_signal | not) and ($hits == 0) and ($stars == 0)) | not)),
        reasons: $reasons
      }
  )
  | sort_by(-.curation_score, -.stars, -.code_hit_count, .repo)
' "$INPUT_JSON" > "$OUT_SCORED_JSON"

{
  printf 'repo\tkind\tpriority\tcuration_score\tlanguage\tstars\tcode_hit_count\tin_candidate_catalog\tin_language_snapshot\treasons\thtml_url\n'
  jq -r '
    .[]
    | [
        .repo,
        .kind,
        .priority,
        (.curation_score | tostring),
        .language,
        (.stars | tostring),
        (.code_hit_count | tostring),
        (if .in_candidate_catalog then "yes" else "no" end),
        (if .in_language_snapshot then "yes" else "no" end),
        (.reasons | join(",")),
        .html_url
      ]
    | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_ALL_TSV"

{
  printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcuration_score\tstars\tcode_hit_count\thtml_url\treasons\tdiscovery_kind\tsubkind\tbucket\n'
  jq -r --arg source_tag "$SOURCE_TAG" '
    [ .[] | select(.include_candidate) | select(.bucket != "unlikely-keep") ]
    | .[]
    | [
        "tier2",
        (.repo
         | ascii_downcase
         | gsub("[^a-z0-9]+"; "-")
         | gsub("^-+"; "")
         | gsub("-+$"; "")),
        .repo,
        (if .kind == "implementation" then .subkind else .kind end),
        .priority,
        (if .kind == "corpus" then "P2" else "P3" end),
        $source_tag,
        "curated-discovered",
        (.curation_score | tostring),
        (.stars | tostring),
        (.code_hit_count | tostring),
        .html_url,
        (.reasons | join(",")),
        .kind,
        .subkind,
        .bucket
      ]
    | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_PRIORITY_TSV"

{
  printf 'repo\tkind\tpriority\tcuration_score\tlanguage\tstars\tcode_hit_count\treasons\thtml_url\n'
  jq -r '
    [ .[]
      | select(.include_candidate)
      | select(.bucket == "obvious-keep")
    ]
    | .[]
    | [
        .repo,
        .kind,
        .priority,
        (.curation_score | tostring),
        .language,
        (.stars | tostring),
        (.code_hit_count | tostring),
        (.reasons | join(",")),
        .html_url
      ]
    | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_OBVIOUS_TSV"

{
  printf 'repo\tkind\tpriority\tcuration_score\tlanguage\tstars\tcode_hit_count\treasons\thtml_url\n'
  jq -r '
    [ .[]
      | select(.include_candidate)
      | select(.bucket == "manual-review")
    ]
    | .[]
    | [
        .repo,
        .kind,
        .priority,
        (.curation_score | tostring),
        .language,
        (.stars | tostring),
        (.code_hit_count | tostring),
        (.reasons | join(",")),
        .html_url
      ]
    | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_MANUAL_TSV"

{
  printf 'repo\tkind\tpriority\tcuration_score\tlanguage\tstars\tcode_hit_count\treasons\thtml_url\n'
  jq -r '
    [ .[]
      | select(.in_candidate_catalog | not)
      | select(.bucket == "unlikely-keep")
    ]
    | .[]
    | [
        .repo,
        .kind,
        .priority,
        (.curation_score | tostring),
        .language,
        (.stars | tostring),
        (.code_hit_count | tostring),
        (.reasons | join(",")),
        .html_url
      ]
    | @tsv
  ' "$OUT_SCORED_JSON"
} > "$OUT_UNLIKELY_TSV"

total_seen=0
if [ -f "$SUMMARY_JSON" ]; then
  total_seen="$(jq -r '.totals.repos_seen // 0' "$SUMMARY_JSON" 2>/dev/null || echo 0)"
fi

{
  echo '# GitHub Broad `lolcode` Curation Report'
  echo
  printf -- '- Generated: %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo '- Source snapshot: `corpus/research/github_repo_search_lolcode/repos.json`'
  printf -- '- Total repos seen: `%s`\n' "$total_seen"
  printf -- '- Classified rows: `%s`\n' "$(jq 'length' "$OUT_SCORED_JSON")"
  printf -- '- Priority candidate rows: `%s`\n' \
    "$(jq '[.[] | select(.include_candidate)] | length' "$OUT_SCORED_JSON")"
  echo
  echo '## Kind Counts'
  echo
  echo '| Kind | Count |'
  echo '|---|---:|'
  jq -r '
    group_by(.kind)
    | map({kind: .[0].kind, count: length})
    | sort_by(.kind)
    | .[]
    | "| `\(.kind)` | \(.count) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Bucket Counts'
  echo
  echo '| Bucket | Count |'
  echo '|---|---:|'
  jq -r '
    [ .[] | select(.in_candidate_catalog | not) ]
    | group_by(.bucket)
    | map({bucket: .[0].bucket, count: length})
    | sort_by(.bucket)
    | .[]
    | "| `\(.bucket)` | \(.count) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Obvious Keep'
  echo
  echo '| Repo | Kind | Priority | Score | Stars | Code hits | Reasons |'
  echo '|---|---|---|---:|---:|---:|---|'
  jq -r '
    [ .[]
      | select(.include_candidate)
      | select(.bucket == "obvious-keep")
    ]
    | .[:60]
    | .[]
    | "| `\(.repo)` | \(.kind) | \(.priority) | \(.curation_score) | \(.stars) | \(.code_hit_count) | \((.reasons | join(", "))) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Manual Review'
  echo
  echo '| Repo | Kind | Priority | Score | Stars | Code hits | Reasons |'
  echo '|---|---|---|---:|---:|---:|---|'
  jq -r '
    [ .[]
      | select(.include_candidate)
      | select(.bucket == "manual-review")
    ]
    | .[:60]
    | .[]
    | "| `\(.repo)` | \(.kind) | \(.priority) | \(.curation_score) | \(.stars) | \(.code_hit_count) | \((.reasons | join(", "))) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Unlikely Keep'
  echo
  echo '| Repo | Kind | Score | Stars | Code hits | Reasons |'
  echo '|---|---|---:|---:|---:|---|'
  jq -r '
    [ .[]
      | select(.in_candidate_catalog | not)
      | select(.bucket == "unlikely-keep")
    ]
    | .[:60]
    | .[]
    | "| `\(.repo)` | \(.kind) | \(.curation_score) | \(.stars) | \(.code_hit_count) | \((.reasons | join(", "))) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Top Missing Implementations and Tooling'
  echo
  echo '| Repo | Kind | Priority | Score | Stars | Code hits | Reasons |'
  echo '|---|---|---|---:|---:|---:|---|'
  jq -r '
    [ .[]
      | select(.include_candidate)
      | select(.kind == "implementation" or .kind == "tooling" or .kind == "docs")
    ]
    | .[:40]
    | .[]
    | "| `\(.repo)` | \(.kind) | \(.priority) | \(.curation_score) | \(.stars) | \(.code_hit_count) | \((.reasons | join(", "))) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Top Missing Corpora'
  echo
  echo '| Repo | Score | Stars | Code hits | Reasons |'
  echo '|---|---:|---:|---:|---|'
  jq -r '
    [ .[]
      | select(.include_candidate)
      | select(.kind == "corpus")
    ]
    | .[:40]
    | .[]
    | "| `\(.repo)` | \(.curation_score) | \(.stars) | \(.code_hit_count) | \((.reasons | join(", "))) |"
  ' "$OUT_SCORED_JSON"
  echo
  echo '## Output Files'
  echo
  echo '- `corpus/research/github_repo_search_lolcode/curation_scored.json`'
  echo '- `corpus/research/github_repo_search_lolcode/classified_repos.tsv`'
  echo '- `corpus/research/github_repo_search_lolcode/priority_candidates.tsv`'
  echo '- `corpus/research/github_repo_search_lolcode/obvious_keep.tsv`'
  echo '- `corpus/research/github_repo_search_lolcode/manual_review.tsv`'
  echo '- `corpus/research/github_repo_search_lolcode/unlikely_keep.tsv`'
} > "$OUT_REPORT_MD"

echo "wrote $OUT_REPORT_MD"
echo "wrote $OUT_ALL_TSV"
echo "wrote $OUT_PRIORITY_TSV"
