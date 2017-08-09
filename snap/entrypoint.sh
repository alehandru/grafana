#!/bin/bash

echo '******************** Checking connection to Elastic Search ...'
while true
do
    curl -IGET http://grafana:9200
    curl_exit_code=$?
    if [[ "$curl_exit_code" = "0" ]]; then
       echo "Elastic Search service is ONLINE."
       break
    else
       echo "Elastic Search service is OFFLINE($curl_exit_code)."
    fi
    sleep 10
done 

echo '******************** Starting snap agent ...'
pushd /opt/snap
/opt/snap/sbin/snapteld --config /opt/snap/sbin/config.yaml --log-path '' --log-level 1
popd
echo 'done.'

