rm -rf /tmp/proj
mkdir /tmp/proj
cp -r /chemeq/* /tmp/proj/
cd /tmp/proj

# -Dexec.args="arg0 arg1 arg2"
mvn clean install exec:java -Dexec.mainClass="com.offbynull.chemeq.Main"