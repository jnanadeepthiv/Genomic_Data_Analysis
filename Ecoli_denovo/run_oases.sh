

module load conda
conda activate assignment1
cd /N/slate/jvishnu/B636_course/Assignment_1
export OMP_NUM_THREADS=16

R1=trimmed_1.fastq
R2=trimmed_2.fastq

for K in 21 31 41 51 61 71 81 91 101 111 121 131 141; do
    echo "===== Oases k=${K} started: $(date) ====="
    /usr/bin/time -v -o time_oases_k${K}.txt bash -c "
      velveth oases_k${K} ${K} -fastq -shortPaired -separate ${R1} ${R2} &&
      velvetg oases_k${K} -read_trkg yes -exp_cov auto -cov_cutoff auto &&
      oases oases_k${K} -min_trans_lgth 200"
    echo "===== Oases k=${K} finished: $(date) ====="
done
