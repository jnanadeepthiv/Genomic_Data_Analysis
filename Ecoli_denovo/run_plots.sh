

# Makes fig1-fig4 (Velvet vs Oases) from velvet_summary.txt and oases_summary.txt.
# Takes a few seconds, so it can run directly:  bash run_plots.sh
# (or as a job:  sbatch run_plots.sh)

cd /N/slate/jvishnu/B636_course/Assignment_1

# Check that the input files exist
for f in velvet_summary.txt oases_summary.txt plot_assembly.py; do
    if [ ! -f "$f" ]; then
        echo "ERROR: $f not found in $(pwd)"; exit 1
    fi
done

# Load Python; install matplotlib for this user only if it is missing
module load python
python3 -c "import matplotlib" 2>/dev/null || pip install --user matplotlib

python3 plot_assembly.py
ls -lh fig*.png
