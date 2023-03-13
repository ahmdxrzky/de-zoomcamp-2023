
## Linux

Here we'll show you how to install Spark 3.3.2 for Linux.
We tested it on Ubuntu 20.04 (also WSL), but it should work
for other Linux distros as well


### Installing Java

Download OpenJDK 11 or Oracle JDK 11 (It's important that the version is 11 - spark requires 8 or 11)

We'll use [OpenJDK](https://jdk.java.net/archive/)

Download it (e.g. to `~/spark`):

```
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```

Unpack it:

```bash
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
```

define `JAVA_HOME` and add it to `PATH`:

```bash
export JAVA_HOME="${HOME}/zoomcamp/week6/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```

check that it works:

```bash
java --version
```

Output:

```
openjdk 11.0.2 2019-01-15
OpenJDK Runtime Environment 18.9 (build 11.0.2+9)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.2+9, mixed mode)
```

Remove the archive:

```bash
rm openjdk-11.0.2_linux-x64_bin.tar.gz
```

### Installing Kafka

Download Kafka. Use 3.3.2 version:

```bash
wget https://downloads.apache.org/kafka/3.3.2/kafka_2.12-3.3.2.tgz
```

Unpack:

```bash
tar xzfv kafka_2.12-3.3.2.tgz
```

Add it to `PATH`:

```bash
export KAFKA_HOME="${HOME}/zoomcamp/week6/kafka_2.12-3.3.2"
export PATH="${KAFKA_HOME}/bin:${PATH}"
```

Remove the archive:

```bash
rm kafka_2.12-3.3.2.tgz
```

Start ZooKeeper:

```bash
${KAFKA_HOME}/bin/zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties
```

Start Kafka Broker/Server:

```bash
${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/server.properties
```