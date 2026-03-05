#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANDIDATE_TSV="$ROOT_DIR/corpus/research/external_issues/candidate_repros.tsv"
EVIDENCE_DIR="$ROOT_DIR/tests/regression-evidence/external"
FIXTURES_DIR="$EVIDENCE_DIR/fixtures"
MANIFEST="$EVIDENCE_DIR/manifest.rktd"
RAW_ISSUES_DIR="$ROOT_DIR/corpus/research/external_issues/raw"

usage() {
  cat <<USAGE
usage: $0 WAVE_NUMBER [--refresh-existing]

Imports one wave from candidate_repros.tsv into:
  - tests/regression-evidence/external/manifest.rktd
  - tests/regression-evidence/external/fixtures/<project>/wave_<NN>/<kind>_<id>/repro.lol

When --refresh-existing is supplied, existing manifest entries are retained
but scaffold fixture files are re-attempted for snippet extraction.
USAGE
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

WAVE="$1"
if ! [[ "$WAVE" =~ ^[0-9]+$ ]] || [[ "$WAVE" -le 0 ]]; then
  echo "error: WAVE_NUMBER must be a positive integer" >&2
  exit 1
fi

REFRESH_EXISTING=0
if [[ $# -eq 2 ]]; then
  case "$2" in
    --refresh-existing) REFRESH_EXISTING=1 ;;
    *)
      echo "error: unknown option '$2'" >&2
      usage
      exit 1
      ;;
  esac
fi

if [[ ! -f "$CANDIDATE_TSV" ]]; then
  echo "error: missing candidate repro list: $CANDIDATE_TSV" >&2
  exit 1
fi

mkdir -p "$FIXTURES_DIR"
if [[ ! -f "$MANIFEST" ]]; then
  cat > "$MANIFEST" <<'EOF_MANIFEST'
(
)
EOF_MANIFEST
fi

sanitize_slug() {
  local s="$1"
  s="$(printf '%s' "$s" | tr '[:upper:]' '[:lower:]')"
  s="$(printf '%s' "$s" | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')"
  if [[ -z "$s" ]]; then
    s="unknown"
  fi
  printf '%s' "$s"
}

sanitize_id_token() {
  local s="$1"
  s="$(printf '%s' "$s" | tr '[:upper:]' '[:lower:]')"
  s="$(printf '%s' "$s" | sed -E 's/[^a-z0-9]+/_/g; s/^_+//; s/_+$//')"
  if [[ -z "$s" ]]; then
    s="unknown"
  fi
  printf '%s' "$s"
}

raw_pages_path() {
  local project_slug="$1"
  local kind="$2"

  case "$kind" in
    issue) printf '%s' "$RAW_ISSUES_DIR/${project_slug}.issues.pages.json" ;;
    pr) printf '%s' "$RAW_ISSUES_DIR/${project_slug}.pulls.pages.json" ;;
    commit) printf '%s' "$RAW_ISSUES_DIR/${project_slug}.commits.pages.json" ;;
    *) printf '' ;;
  esac
}

extract_source_text() {
  local project_slug="$1"
  local kind="$2"
  local source_id="$3"
  local source_url="$4"
  local raw_pages
  raw_pages="$(raw_pages_path "$project_slug" "$kind")"

  if [[ -z "$raw_pages" || ! -f "$raw_pages" ]]; then
    return 1
  fi

  case "$kind" in
    issue|pr)
      local source_num=""
      if [[ "$source_id" =~ ^[0-9]+$ ]]; then
        source_num="$source_id"
      elif [[ "$source_url" =~ /([0-9]+)$ ]]; then
        source_num="${BASH_REMATCH[1]}"
      fi

      if [[ -n "$source_num" ]]; then
        jq -r --argjson n "$source_num" '
          .[][] | select((.number // -1) == $n)
          | ((.title // "") + "\n\n" + (.body // ""))
        ' "$raw_pages" | awk 'NF || p{print; p=1}' | sed -n '1,4000p'
      else
        jq -r --arg url "$source_url" '
          .[][] | select((.html_url // .url // "") == $url or (.url // "") == $url)
          | ((.title // "") + "\n\n" + (.body // ""))
        ' "$raw_pages" | awk 'NF || p{print; p=1}' | sed -n '1,4000p'
      fi
      ;;
    commit)
      local source_sha="$source_id"
      if [[ -z "$source_sha" && "$source_url" =~ /([0-9a-fA-F]{7,40})$ ]]; then
        source_sha="${BASH_REMATCH[1]}"
      fi
      if [[ -z "$source_sha" ]]; then
        return 1
      fi
      jq -r --arg sha "$source_sha" '
        .[][] | select(((.sha // "") | ascii_downcase) | startswith(($sha | ascii_downcase)))
        | ((.commit.message // "")
           + "\n\n"
           + (([.files[]?.patch // empty] | join("\n\n")) // ""))
      ' "$raw_pages" | awk 'NF || p{print; p=1}' | sed -n '1,4000p'
      ;;
    *)
      return 1
      ;;
  esac
}

extract_lolcode_snippet_from_markdown() {
  perl -0777 -ne '
    my $text = $_ // "";
    my @blocks;
    while ($text =~ /```([^\n`]*)\n(.*?)```/sg) {
      push @blocks, [$1, $2];
    }

    sub looks_lol {
      my ($info, $code) = @_;
      return 1 if defined($info) && $info =~ /\blol(?:code)?\b/i;
      return 1 if defined($code) && $code =~ /\bHAI\b/i;
      return 1 if defined($code) && $code =~ /\bKTHXBYE\b/i;
      return 1 if defined($code) && $code =~ /\bVISIBLE\b/i;
      return 1 if defined($code) && $code =~ /\bI HAS A\b/i;
      return 0;
    }

    for my $b (@blocks) {
      my ($info, $code) = @$b;
      if (looks_lol($info, $code)) {
        print $code;
        exit 0;
      }
    }

    if ($text =~ /(\bHAI\b.*?\bKTHXBYE\b)/is) {
      print $1;
      exit 0;
    }

    exit 1;
  '
}

write_fixture_file() {
  local fixture_abs="$1"
  local project_slug="$2"
  local kind="$3"
  local source_id="$4"
  local source_url="$5"
  local source_title="$6"
  local write_scaffold_on_miss="${7:-1}"

  local source_text=""
  local extracted_snippet=""
  source_text="$(extract_source_text "$project_slug" "$kind" "$source_id" "$source_url" | sed -n '1,4000p' || true)"

  if [[ -n "$source_text" ]]; then
    extracted_snippet="$(printf '%s' "$source_text" | extract_lolcode_snippet_from_markdown || true)"
  fi

  if [[ -n "$extracted_snippet" ]]; then
    if printf '%s' "$extracted_snippet" | rg -q '(?i)\bHAI\b'; then
      printf '%s\n' "$extracted_snippet" > "$fixture_abs"
    else
      cat > "$fixture_abs" <<EOF_EXTRACTED
HAI 1.3
BTW External evidence extracted snippet (wrapped in HAI/KTHXBYE).
BTW Source: $source_url
$extracted_snippet
KTHXBYE
EOF_EXTRACTED
    fi
    printf 'extracted'
    return 0
  fi

  if [[ "$write_scaffold_on_miss" -eq 0 ]]; then
    printf 'unchanged'
    return 0
  fi

  cat > "$fixture_abs" <<EOF_FIXTURE
HAI 1.2
BTW External evidence fixture scaffold.
BTW Source: $source_url
BTW Title: $source_title
KTHXBYE
EOF_FIXTURE
  printf 'scaffold'
}

append_manifest_entry() {
  local manifest_path="$1"
  local entry="$2"
  local tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/manifest-entry.XXXXXX")"

  local last
  last="$(
    awk '/^[[:space:]]*\)[[:space:]]*$/ { line = NR } END { print line + 0 }' "$manifest_path"
  )"

  if [[ "$last" -eq 0 ]]; then
    {
      echo "("
      cat "$manifest_path"
      echo
      printf '%s\n' "$entry"
      echo ")"
    } > "$tmp"
  else
    awk -v last="$last" 'NR < last { print }' "$manifest_path" > "$tmp"
    echo >> "$tmp"
    printf '%s\n' "$entry" >> "$tmp"
    echo ")" >> "$tmp"
    awk -v last="$last" 'NR > last { print }' "$manifest_path" >> "$tmp"
  fi

  mv "$tmp" "$manifest_path"
}

printf -v wave_dir "wave_%02d" "$WAVE"
today="$(date +%F)"

imported=0
existing=0
skipped=0
extracted_fixtures=0
scaffold_fixtures=0
refreshed_extracted=0

while IFS= read -r line; do
  if [[ -z "$line" ]]; then
    continue
  fi

  IFS=$'\t' read -r -a fields <<< "$line"
  if [[ "${#fields[@]}" -lt 11 ]]; then
    echo "skip: malformed row (expected >= 11 tab-separated fields): $line" >&2
    skipped=$((skipped + 1))
    continue
  fi

  rank="${fields[0]}"
  wave="${fields[1]}"
  repo="${fields[2]}"
  label="${fields[3]}"
  item_type="${fields[4]}"
  number="${fields[5]}"
  state="${fields[6]}"
  category="${fields[7]}"
  score="${fields[8]}"
  last_idx=$((${#fields[@]} - 1))
  url="${fields[$last_idx]}"

  title="${fields[9]}"
  if [[ "${#fields[@]}" -gt 11 ]]; then
    for ((idx = 10; idx < ${#fields[@]} - 1; idx++)); do
      title+=$'\t'"${fields[$idx]}"
    done
  fi

  if [[ "$wave" == "wave" ]]; then
    continue
  fi

  if [[ "$wave" != "$WAVE" ]]; then
    continue
  fi

  kind="$item_type"
  case "$kind" in
    issue) source_origin="issue-body" ;;
    pr) source_origin="pr-description" ;;
    commit) source_origin="commit-message" ;;
    *)
      echo "skip: unsupported item_type '$kind' for row rank=$rank" >&2
      skipped=$((skipped + 1))
      continue
      ;;
  esac

  project="${label:-}"
  if [[ -z "$project" ]]; then
    project="${repo##*/}"
  fi

  project_slug="$(sanitize_slug "$project")"
  project_id="$(sanitize_id_token "$project_slug")"

  source_id="${number:-}"
  source_token=""
  if [[ -n "$source_id" && "$source_id" =~ ^[0-9]+$ ]]; then
    printf -v source_token "%04d" "$source_id"
  else
    if [[ -z "$source_id" ]]; then
      source_id="${url##*/}"
    fi
    source_token="$(sanitize_id_token "$source_id")"
  fi

  case_id="ext_${project_id}_${kind}_${source_token}"

  fixture_rel="fixtures/${project_slug}/${wave_dir}/${kind}_${source_token}/repro.lol"
  fixture_abs="$EVIDENCE_DIR/$fixture_rel"

  if rg -Fq "(id . \"$case_id\")" "$MANIFEST"; then
    existing=$((existing + 1))
    if [[ "$REFRESH_EXISTING" -eq 1 && -f "$fixture_abs" ]] \
      && rg -Fq "BTW External evidence fixture scaffold." "$fixture_abs"; then
      refreshed_mode="$(write_fixture_file "$fixture_abs" "$project_slug" "$kind" "$source_id" "$url" "$title" 0)"
      if [[ "$refreshed_mode" == "extracted" ]]; then
        refreshed_extracted=$((refreshed_extracted + 1))
      fi
    fi
    continue
  fi

  mkdir -p "$(dirname "$fixture_abs")"
  if [[ ! -f "$fixture_abs" ]]; then
    fixture_mode="$(write_fixture_file "$fixture_abs" "$project_slug" "$kind" "$source_id" "$url" "$title")"
    if [[ "$fixture_mode" == "extracted" ]]; then
      extracted_fixtures=$((extracted_fixtures + 1))
    else
      scaffold_fixtures=$((scaffold_fixtures + 1))
    fi
  else
    fixture_mode="existing"
  fi

  title_for_notes="${title//$'\t'/ }"
  notes="Imported from candidate_repros.tsv rank=${rank} state=${state} category=${category} score=${score} fixture=${fixture_mode} title=${title_for_notes}"
  notes_escaped="${notes//\"/\\\"}"

  entry=$(
    printf '%s\n' \
      "  #hasheq(" \
      "    (id . \"$case_id\")" \
      "    (wave . $WAVE)" \
      "    (source-file . \"$fixture_rel\")" \
      "    (source-project . \"$project_slug\")" \
      "    (source-repo . \"$repo\")" \
      "    (source-kind . \"$kind\")" \
      "    (source-id . \"$source_id\")" \
      "    (source-url . \"$url\")" \
      "    (source-origin . \"$source_origin\")" \
      "    (spec-scope . (\"unknown\"))" \
      "    (spec-refs . ())" \
      "    (oracle-class . \"external-evidence\")" \
      "    (triage-status . \"candidate\")" \
      "    (hypothesis . \"unknown\")" \
      "    (notes . \"$notes_escaped\")" \
      "    (added-on . \"$today\"))"
  )

  append_manifest_entry "$MANIFEST" "$entry"
  imported=$((imported + 1))
done < "$CANDIDATE_TSV"

echo "wave=$WAVE imported=$imported existing=$existing skipped=$skipped"
echo "fixtures: extracted=$extracted_fixtures scaffold=$scaffold_fixtures"
if [[ "$REFRESH_EXISTING" -eq 1 ]]; then
  echo "refresh: extracted-from-existing=$refreshed_extracted"
fi
echo "manifest=$MANIFEST"
