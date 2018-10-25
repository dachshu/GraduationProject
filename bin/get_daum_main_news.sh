#!/bin/bash

ARTICLE_TITLES_LINKS=$(./GetDaumMainNews.py)
INDEX=$(shuf -i 1-5 -n 1)
SELECTED_TITLE=$(echo "${ARTICLE_TITLES_LINKS}" | awk "NR == (${INDEX}*2-1)")
SELECTED_LINK=$(echo "${ARTICLE_TITLES_LINKS}" | awk "NR == ${INDEX}*2")
echo -e "${SELECTED_TITLE}\n${SELECTED_LINK}"
