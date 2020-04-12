NAME=$(find /input -type f -exec md5sum {} \; | md5sum | cut -d " " -f1)
ENV_NAMES=$(conda info --envs)

if [[ $NAME != *$ENV_NAMES* ]]; then
  conda env create -f /input/code_kmer/src/conda_env.yml -n $NAME
fi

conda init bash
conda activate $NAME
python /input/code_kmer/src/KmerReverseComplement.py < /input/input.data > /output/output.md