

# Extracts the length of every contig in the optimal assemblies,
# then makes tables and plots with plot_contigs.py.
# Run with:  bash contig_lengths.sh   (or: sbatch contig_lengths.sh)

cd /N/slate/jvishnu/B636_course/Assignment_1

VELVET_FA=velvet_k81/contigs.fa       # optimal Velvet assembly
OASES_FA=oases_k71/transcripts.fa     # optimal Oases assembly

for f in "$VELVET_FA" "$OASES_FA" plot_contigs.py; do
    if [ ! -f "$f" ]; then echo "ERROR: $f not found"; exit 1; fi
done

# One line per contig: <contig name><TAB><length in bp>, longest first.
# Length is measured from the sequence itself (not the FASTA header).
lengths () {
    awk '/^>/{if(id) print id"\t"length(seq); id=substr($0,2); seq=""; next}
         {seq=seq$0}
         END{if(id) print id"\t"length(seq)}' "$1" | sort -t$'\t' -k2,2nr
}

lengths "$VELVET_FA" > velvet_k81_contig_lengths.tsv
lengths "$OASES_FA"  > oases_k71_contig_lengths.tsv

echo "== Check: counts and totals =="
for f in velvet_k81_contig_lengths.tsv oases_k71_contig_lengths.tsv; do
    awk -v f="$f" '{s+=$2} END{print f": "NR" contigs, total "s" bp"}' "$f"
done

# Tables + plots
module load python
python3 -c "import matplotlib" 2>/dev/null || pip install --user matplotlib
python3 plot_contigs.py
