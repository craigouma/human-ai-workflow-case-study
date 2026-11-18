#!/usr/bin/env bash
# Builds case_study.md, case_study.docx and case_study.pdf from build/build_case_study.js and diagram/workflow.png.
#
# Needs: node with the `docx` package, Python with fonttools, LibreOffice (soffice), poppler (pdfinfo), and the four Computer Modern
# Unicode OpenType files (CMU Serif, SIL Open Font License) from
#   https://mirrors.ctan.org/fonts/cm-unicode/fonts/otf/{cmunrm,cmunbx,cmunti,cmunbi}.otf
#
# Usage (from the repository root):
#   FONT_DIR=/path/to/cmu-fonts DOCX_MODULE=/path/to/node_modules/docx bash build/build.sh
# The fonts are loaded through a throwaway LibreOffice profile, so nothing is installed on the system.

set -euo pipefail

: "${FONT_DIR:?Set FONT_DIR to the folder holding cmunrm.otf, cmunbx.otf, cmunti.otf and cmunbi.otf}"
export DOCX_MODULE="${DOCX_MODULE:-docx}"

PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT
mkdir -p "$PROFILE/user/fonts"
cp "$FONT_DIR"/cmun{rm,bx,ti,bi}.otf "$PROFILE/user/fonts/"

node build/build_case_study.js

# Embed Computer Modern so the .docx keeps its one-page layout where the font is not installed.
# Needs fonttools; set PYTHON to an interpreter that has it (default: python3).
"${PYTHON:-python3}" build/embed_fonts.py case_study.docx "$FONT_DIR"

soffice -env:UserInstallation="file://$PROFILE" --headless --convert-to pdf --outdir . case_study.docx >/dev/null 2>&1

PAGES="$(pdfinfo case_study.pdf | awk '/^Pages:/ {print $2}')"
echo "case_study.pdf has $PAGES page(s)"
if [ "$PAGES" != "1" ]; then
  echo "ERROR: the case study must fit exactly one A4 page" >&2
  exit 1
fi
