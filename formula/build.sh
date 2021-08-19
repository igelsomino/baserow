#!/bin/bash
# Bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

echo "Ensuring output folder is clean..."
rm out/ -rf

USER_ID="$(id -u "$USER")"
GROUP_ID="$(id -g "$USER")"

echo "Building antlr4 build image and generating parsers, might take a while..."
docker run -it --rm \
    -v "$(pwd)":/workspace/src \
    -u "$USER_ID":"$GROUP_ID" \
    "$(docker build -q --build-arg UID="$USER_ID" --build-arg GID="$GROUP_ID" . )" sh -c "
        cd src
        java -jar ../antlr.jar -Dlanguage=JavaScript -o out/frontend_parser -visitor -listener BaserowFormulaLexer.g4
        java -jar ../antlr.jar -Dlanguage=JavaScript -o out/frontend_parser -visitor -listener BaserowFormula.g4
        java -jar ../antlr.jar -Dlanguage=Python3 -o out/backend_parser -visitor -listener BaserowFormulaLexer.g4
        java -jar ../antlr.jar -Dlanguage=Python3 -o out/backend_parser -visitor -listener BaserowFormula.g4
    "

echo "Moving generated parsers into the Baserow source code..."
FRONTEND_OUTPUT_DIR=./../web-frontend/modules/database/formula/parser/generated/
mkdir -p $FRONTEND_OUTPUT_DIR
rm -f "$FRONTEND_OUTPUT_DIR"BaserowFormula*
cp out/frontend_parser/* $FRONTEND_OUTPUT_DIR

BACKEND_OUTPUT_DIR=./../backend/src/baserow/contrib/database/formula/parser/generated/
mkdir -p $BACKEND_OUTPUT_DIR
rm -f "$BACKEND_OUTPUT_DIR"BaserowFormula*
cp out/backend_parser/* $BACKEND_OUTPUT_DIR

echo "Moving tokens next to grammar files.."
# Place the generated tokens next to the grammar files also so IDE plugins can use them
# to show more details about the grammar files themselves.
cp out/backend_parser/*.tokens .

echo "Cleaning up out folder..."
rm out/ -rf

GREEN=$(tput setaf 2)
NC=$(tput sgr0) # No Color
echo "${GREEN}Build successfully finished!${NC}"