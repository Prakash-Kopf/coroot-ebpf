**Coroot eBPF Tool**
This tool will be useful for zero code instrumentation with eBPF technology enabled. So that we dont need to write any additional programs to capture kernel level processes.

This tool will automatically captures once we installed as a daemonset in K8s or in Docker or bare metal, it can fetch all the applications logs, traces, profiles and metrics 
In the containers or pods. 


Installing Coroot on Ubuntu/Debian

Step #1: Installing ClickHouse
sudo apt install -y apt-transport-https ca-certificates curl gnupg
curl -fsSL 'https://packages.clickhouse.com/rpm/lts/repodata/repomd.xml.key' | sudo gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg] https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y clickhouse-server clickhouse-client
sudo service clickhouse-server start


Step #2: Installing Prometheus
Coroot requires Prometheus with support for Remote Write Receiver, which has been available since v2.25.0.
sudo apt install -y prometheus
sudo service prometheus start


Enable Remote Write Receiver in Prometheus by adding the --enable-feature=remote-write-receiver argument to the /etc/default/prometheus file:
# Set the command-line arguments to pass to the server.
# Due to shell escaping, to pass backslashes for regexes, you need to double
# them (\\d for \d). If running under systemd, you need to double them again
# (\\\\d to mean \d), and escape newlines too.
ARGS="--enable-feature=remote-write-receiver"


Restart Prometheus:
sudo service prometheus restart


Step #3: Installing Coroot
curl -sfL https://raw.githubusercontent.com/coroot/coroot/main/deploy/install.sh | \
  BOOTSTRAP_PROMETHEUS_URL="http://127.0.0.1:9090" \
  BOOTSTRAP_REFRESH_INTERVAL=15s \
  BOOTSTRAP_CLICKHOUSE_ADDRESS=127.0.0.1:9000 \
  sh -


Step #4: Installing coroot-node-agent
curl -sfL https://raw.githubusercontent.com/coroot/coroot-node-agent/main/install.sh | \
  COLLECTOR_ENDPOINT=http://127.0.0.1:8080 \
  SCRAPE_INTERVAL=15s \
  sh -


Step #5: Accessing Coroot
Access Coroot at: http://NODE_IP:8080.
Uninstall Coroot
To uninstall Coroot run the following command:
/usr/bin/coroot-uninstall.sh


Uninstall coroot-node-agent:
/usr/bin/coroot-node-agent-uninstall.sh


This script downloads the latest version of the agent and installs it as a Systemd service. Additionally, it generates an uninstall script.
curl -sfL https://raw.githubusercontent.com/coroot/coroot-node-agent/main/install.sh | \
  COLLECTOR_ENDPOINT=http://13.127.155.200:8080 \
  API_KEY=cxxxxxx \
  SCRAPE_INTERVAL=15s \
  sh -


In this demo project, i just created a python flask based application to capture MELT of an application
2nd I used Open Telemetry also to capture MELT both we can see it on Coroot UI

So, basically this application I used manual instrumentaion and agent based Instumetation (Coroot Node Agent) which captures MELT and by agent, export to Coroot 
And by Open Telemetry, I used SDK based OTEL collector which collects the application MELT.

