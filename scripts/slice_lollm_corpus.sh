#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INPUT_PATH="${1:-$REPO_ROOT/corpus/research/lollm/lolspeak.txt}"
OUT_DIR="${2:-$REPO_ROOT/corpus/research/lollm/sliced}"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/lollm-slice.XXXXXX")"

trash_path() {
  local path="$1"
  [ -e "$path" ] || return 0
  if ! command -v trash >/dev/null 2>&1; then
    echo "Missing required command: trash" >&2
    return 1
  fi
  mkdir -p "$TRASH_DIR"
  trash --trash-dir "$TRASH_DIR" "$path"
}

cleanup_tmp() {
  trash_path "$TMP_DIR" || true
}

trap cleanup_tmp EXIT

if [ ! -f "$INPUT_PATH" ]; then
  echo "Input not found: $INPUT_PATH" >&2
  exit 1
fi

tmp_out="$TMP_DIR/out"
mkdir -p "$tmp_out/programs"

manifest_tsv="$tmp_out/manifest.tsv"
outside_text="$tmp_out/non_program_text.txt"
summary_md="$tmp_out/SUMMARY.md"

printf 'id\ttitle\tstart_line\tend_line\tline_count\tfile\tstatus\n' > "$manifest_tsv"
: > "$outside_text"

awk \
  -v out_root="$tmp_out/programs" \
  -v manifest="$manifest_tsv" \
  -v outside="$outside_text" \
  '
  function trim(s) {
    gsub(/^[[:space:]]+/, "", s)
    gsub(/[[:space:]]+$/, "", s)
    return s
  }
  BEGIN {
    in_program = 0
    prog_id = 0
    last_title = ""
    program_file = ""
    start_line = 0
  }
  {
    line = $0

    if (line ~ /^[[:space:]]*BTW[[:space:]]*---[[:space:]]*.*[[:space:]]*---[[:space:]]*$/) {
      title_line = line
      sub(/^[[:space:]]*BTW[[:space:]]*---[[:space:]]*/, "", title_line)
      sub(/[[:space:]]*---[[:space:]]*$/, "", title_line)
      last_title = trim(title_line)
    }

    if (!in_program) {
      if (line ~ /^[[:space:]]*HAI[[:space:]]+[0-9]+\.[0-9]+([[:space:]].*)?$/) {
        in_program = 1
        prog_id++
        start_line = NR
        program_file = sprintf("%s/program_%03d.lol", out_root, prog_id)
        title = (last_title == "" ? "(untitled)" : last_title)
        print line >> program_file
      } else {
        print line >> outside
      }
      next
    }

    print line >> program_file

    if (line ~ /^[[:space:]]*KTHXBYE[[:space:]]*$/) {
      end_line = NR
      line_count = end_line - start_line + 1
      printf "%03d\t%s\t%d\t%d\t%d\t%s\tcomplete\n",
        prog_id, title, start_line, end_line, line_count,
        sprintf("programs/program_%03d.lol", prog_id) >> manifest
      close(program_file)
      in_program = 0
      program_file = ""
      start_line = 0
      title = ""
      last_title = ""
    }
  }
  END {
    if (in_program) {
      line_count = NR - start_line + 1
      printf "%03d\t%s\t%d\t\t%d\t%s\tincomplete\n",
        prog_id, title, start_line, line_count,
        sprintf("programs/program_%03d.lol", prog_id) >> manifest
      close(program_file)
    }
  }
  ' "$INPUT_PATH"

program_total="$(awk -F'\t' 'NR>1 && $7=="complete" {c++} END {print c+0}' "$manifest_tsv")"
incomplete_total="$(awk -F'\t' 'NR>1 && $7=="incomplete" {c++} END {print c+0}' "$manifest_tsv")"
outside_total="$(wc -l < "$outside_text" | awk "{print \$1}")"
outside_nonblank="$(awk 'NF {c++} END {print c+0}' "$outside_text")"

{
  echo "# LOLLM Corpus Slice Summary"
  echo
  echo "Generated: \`$(date -u +%Y-%m-%dT%H:%M:%SZ)\`"
  echo
  echo "- Input: \`$INPUT_PATH\`"
  echo "- Extracted programs: \`$program_total\`"
  echo "- Incomplete program fragments: \`$incomplete_total\`"
  echo "- Non-program lines dropped: \`$outside_total\`"
  echo "- Non-program non-empty lines dropped: \`$outside_nonblank\`"
  echo
  echo "Files:"
  echo
  echo "- \`manifest.tsv\`"
  echo "- \`programs/program_*.lol\`"
} > "$summary_md"

trash_path "$outside_text"

trash_path "$OUT_DIR"
mkdir -p "$OUT_DIR"
cp -R "$tmp_out"/. "$OUT_DIR"/

echo "Wrote sliced corpus:"
echo "- $OUT_DIR"
echo "- programs=$program_total incomplete=$incomplete_total outside_lines=$outside_total"
