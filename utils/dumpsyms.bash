#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <trace_file>"
  echo "you copy/paste the text that DumpStackTraceLinux() function in .cpp (see the patch) outputs"
  echo "firefox must be built with 'ac_add_options --enable-debug-symbols' OR if u're brave with '--enable-debug'"
  TRACE_FILE="trace.txt"
  #exit 1
else
  TRACE_FILE="$1"
fi


#while IFS= read -r line || [ -n "$line" ]; do
#  # Skip empty lines.
#  [ -z "$line" ] && continue
#
#  # Check if the line refers to libxul.so (adjust the pattern if needed).
#  if [[ "$line" =~ libxul\.so ]]; then
#    # Extract the library path: everything until the first '('.
#    #libpath=$(echo "$line" | sed 's/^$[^()]*\.so$.*/\1/')
#    # Extract the offset (inside the parentheses).
#    #offset=$(echo "$line" | sed -n 's/.*(\+$0x[0-9a-fA-F]*$).*/\1/p')
#
#    # Extract the library path: match from the beginning until ".so"
#    libpath=$(echo "$line" | sed -E 's/^(.*\.so).*/\1/')
#    # Extract the offset: match a '(+<hex>)' pattern
#    offset=$(echo "$line" | sed -E -n 's/.*\[(0x[0-9a-fA-F]+)\]$/\1/')
#    echo "$libpath $offset"
#
#    if [ -n "$libpath" ] && [ -n "$offset" ]; then
#      echo "Line: $line"
#      echo "-> Resolving: addr2line -e $libpath $offset"
#      addr2line -e "$libpath" "$offset"
#      echo "-----------------------------------"
#    else
#      echo "Could not extract info from: $line"
#    fi
#  else
#    # For lines not referencing libxul.so you may skip or handle differently.
#    echo "Skipping line: $line"
#  fi
#
#done < "$TRACE_FILE"
#
##!/bin/bash

## Path to libxul.so
#LIBXUL="/home/user/SOURCE/firefox-developer-edition/src/firefox-137.0/obj/dist/bin/libxul.so"
#TRACE_FILE="trace.txt"

# Check Bash version (needs 4+ for associative arrays)
if (( BASH_VERSINFO[0] < 4 )); then
  echo "Error: Bash 4.0+ required for associative arrays!"
  exit 1
fi

# Check if trace.txt exists
if [ ! -f "$TRACE_FILE" ]; then
  echo "Error: $TRACE_FILE not found!"
  exit 1
fi

## Read trace.txt, extract offsets, and run addr2line
#time while IFS= read -r line; do
#  # Match lines with offsets like (+0xHEX)
#  if [[ $line =~ \+0x([0-9a-fA-F]+) ]]; then
#    offset="0x${BASH_REMATCH[1]}"
#    echo "Line: $line"
#    echo "Offset: $offset"
#    addr2line -e "$LIBXUL" -f -C "$offset"
#    echo "----"
#  fi
#done < "$TRACE_FILE"


## Extract offsets into a single string
#offsets=""
#while IFS= read -r line; do
#  if [[ $line =~ \+0x([0-9a-fA-F]+) ]]; then
#    offset="0x${BASH_REMATCH[1]}"
#    offsets="$offsets $offset"
#  fi
#done < "$TRACE_FILE"
#
## Run addr2line once with all offsets
#if [ -n "$offsets" ]; then
#  echo "Mapping offsets: $offsets"
#  echo "----"
#  # Use xargs to pass offsets to addr2line
#  echo "$offsets" | xargs addr2line -e "$LIBXUL" -f -C
#else
#  echo "No offsets found in $TRACE_FILE!"
#fi

# Associative array for offsets
declare -A offsets_by_file

# Read trace.txt and group offsets
while IFS= read -r line; do
  if [[ $line =~ ^(.+)\(\+0x([0-9a-fA-F]+)\) ]]; then
    filename="${BASH_REMATCH[1]}"
    offset="0x${BASH_REMATCH[2]}"
    #offsets_by_file["$filename"]="${offsets_by_file["$filename"]} $offset"
    offsets_by_file["$filename"]+=" $offset"
  fi
done < "$TRACE_FILE"

## Process each file with its offsets
#for file in "${!offsets_by_file[@]}"; do
#  offsets="${offsets_by_file["$file"]}"
#  echo "Mapping $file offsets:$offsets"
#  echo "----"
#  # Batch addr2line for this file
#  echo "$offsets" | xargs addr2line -e "$file" -f -C
#  echo "----"
#done

# Process each file
for file in "${!offsets_by_file[@]}"; do
  offsets="${offsets_by_file["$file"]}"
  echo "Mapping $file offsets:$offsets"
  echo "----"
  # Trim leading space
  offsets="${offsets#" "}"
  addr2line -e "$file" -f -C $offsets
  echo "----"
done
