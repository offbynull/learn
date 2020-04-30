NAME=$(find /input/ch1_code -type f -exec md5sum {} \; | md5sum | cut -d " " -f1)
ENV_NAMES=$(conda info --envs)

if [[ $NAME != *$ENV_NAMES* ]]; then
  conda env create -f /input/ch1_code/src/conda_env.yml -n $NAME
fi

source /opt/conda/etc/profile.d/conda.sh
conda activate $NAME
python /input/ch1_code/src/Router.py < /input/input.data > /output/output.md