rm -rf /tmp/proj
mkdir /tmp/proj
cp -r /input/pvshelper_code/* /tmp/proj/
cd /tmp/proj

# -Dexec.args="arg0 arg1 arg2"
mvn clean install exec:java -q -Dexec.mainClass="com.offbynull.pvshelper.MainPartialConceptRecurseDraw"