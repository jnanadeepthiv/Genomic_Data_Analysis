#!/bin/bash
#SBATCH -J ecoli_asm
#SBATCH -p debug
#SBATCH -A r00302
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=500G
#SBATCH --time=1:00:00
#SBATCH -o asm_%j.out
#SBATCH -e asm_%j.err
#SBATCH --mail-user=jvishnu@iu.edu
#SBATCH --mail-type=ALL

module load conda
conda activate assignment1
cd /N/slate/jvishnu/B636_course/Assignment_1
export OMP_NUM_THREADS=16

R1=trimmed_1.fastq
R2=trimmed_2.fastq

for K in 15 21 31 41 51 61 71 81 91 101 111 121 131 141; do
    echo "===== Velvet k=${K} started: $(date) ====="
    /usr/bin/time -v -o time_velvet_k${K}.txt bash -c "
      velveth velvet_k${K} ${K} -fastq -shortPaired -separate ${R1} ${R2} &&
      velvetg velvet_k${K} -exp_cov auto -cov_cutoff auto -min_contig_lgth 200"
    echo "===== Velvet k=${K} finished: $(date) ====="
done
