NAME=$(find /input -type f -exec md5sum {} \; | md5sum | cut -d " " -f1)
ENV_NAMES=$(conda info --envs)

if [[ $NAME != *$ENV_NAMES* ]]; then
  conda env create -f conda_env.yml -n $NAME
fi

conda run -n $NAME python /input/Main.py < /input/input.data > /output/output.md 2>/tmp/err.txt

# Why have this? The current version of conda run doesn't get back exit codes. There's a fix in progress but
# it hasn't been released yet. This workaround says that if there's anything dumped to stderr, then treat it
# as a failure.
if [[ -s "/tmp/err.txt" ]]; then
  cat /tmp/err.txt >&2
  exit 1
fi