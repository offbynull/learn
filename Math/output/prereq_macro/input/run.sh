rm -rf /tmp/proj
mkdir /tmp/proj
cp -r /input/prereq_code/* /tmp/proj/
cd /tmp/proj
cat /input/input.data
python PreReq.py < /input/input.data > /output/output.md