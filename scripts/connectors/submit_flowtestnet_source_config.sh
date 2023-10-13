#!/bin/bash

HEADER="Content-Type: application/json"
DATA=$( cat << EOF
{
  "name": "flowtestnet-source",
  "config": {
        "connector.class": "com.github.castorm.kafka.connect.http.HttpSourceConnector",
        "tasks.max": "2",
        "http.offset.initial": "cursor=",
        "http.request.url": "https://us-west1-dl-engplay-eric-ren.cloudfunctions.net/flow-paginator-mainnet",
        "http.request.headers": "Accept: application/json",
        "http.request.params": "beginHeight=123352941&v=local2&fetchByBlock=true&pageToken=\${offset.cursor}&useTestnet=true",
        "http.auth.type": "Basic",
        "http.auth.user": "connectorSA",
        "http.auth.password": "connectorSA",
        "http.response.list.pointer": "/results",
        "http.response.record.offset.pointer": "cursor=/nextPageToken",
        "http.timer.interval.millis": "250",
        "http.client.connection.timeout.millis": "600000",
        "kafka.topic": "flow-testnet",
        "principal.service.name": "connectorSA",
        "principal.service.password": "connectorSA",
        "http.response.record.mapper": "com.github.castorm.kafka.connect.http.record.StringKvSourceRecordMapper"
  }
}
EOF
)

docker-compose exec connect curl -X POST -H "${HEADER}" --data "${DATA}" --cert /etc/kafka/secrets/connect.certificate.pem --key /etc/kafka/secrets/connect.key --tlsv1.2 --cacert /etc/kafka/secrets/snakeoil-ca-1.crt -u connectorSubmitter:connectorSubmitter https://connect:8083/connectors || exit 1
