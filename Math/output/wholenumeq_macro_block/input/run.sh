rm -rf /tmp/proj
mkdir /tmp/proj
cp -r /input/arithmetic_code/* /tmp/proj/
cd /tmp/proj
cat /input/input.data
python WholeNumberEqLauncher.py < /input/input.data > /output/output.md