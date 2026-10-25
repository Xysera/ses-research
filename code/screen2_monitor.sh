#!/bin/bash
for j in 6adbf5c1046eb82b1ecd89cf 6adbf5c6046eb82b1ecd89d1 6adbf5cc1e112550ce7da7f7; do
  echo "== $j: $(hf jobs inspect $j 2>&1 | grep -oE '\"stage\": *\"[A-Z]+\"' | head -1)"; hf jobs logs $j 2>&1 | grep -E "jobs [0-9]+|done [0-9]+|COMPLETE|Traceback|Error" | tail -2 | cut -c1-200
done
