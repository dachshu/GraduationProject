#!/bin/bash

# This script remove hyperlinks, mentioned nicknames, and blank lines in tweet

REMOVE_HYPERLINK="perl -p -e 's|https?://.*?(\s)|$1|g'"
REMOVE_MENTION_ID="perl -p -e 's|@.*?\s?||g'"

cat | sed -r '/^\s*$/d' | perl -p -e 's| ?https?://.*?(\s)|$1|g' | sed -r 's/(^|\s)@\S*/\1@/g'
