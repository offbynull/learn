rm -rf /tmp/proj
mkdir /tmp/proj
cp -r /input/arithmetic_code/* /tmp/proj/
cd /tmp/proj
python WholeNumberDivLauncher.py < /input/input.data > /output/output.md