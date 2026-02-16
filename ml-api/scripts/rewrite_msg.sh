#!/bin/bash

# Script to clean up commit messages for conventional commits
# - Make first line lowercase
# - Truncate first line to 60 characters
# - Keep the rest of the message unchanged

msg=$(cat)
first_line=$(echo "$msg" | head -n1)

# Make lowercase
first_line=$(echo "$first_line" | tr '[:upper:]' '[:lower:]')

# Truncate to 60 chars
if [[ ${#first_line} -gt 60 ]]; then
    first_line=${first_line:0:60}
fi

# Output the new first line
echo "$first_line"

# Output the rest of the message
echo "$msg" | tail -n +2