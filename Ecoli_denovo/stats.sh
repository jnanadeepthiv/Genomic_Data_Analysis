#!/bin/bash
awk '/^>/{if(seq) print length(seq); seq=""; next}{seq=seq$0}END{if(seq) print length(seq)}' "$1" \
| sort -nr | awk '{a[NR]=$1; s+=$1} END{
    t=0; for(i=1;i<=NR;i++){t+=a[i]; if(t>=s/2){n50=a[i]; break}}
    printf "contigs=%d\ttotal=%d\tlongest=%d\tN50=%d\n", NR, s, a[1], n50}'
