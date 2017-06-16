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
    sleep 5
done 

echo '******************** Starting telegraf agent ...'
pushd /opt/telegraf
telegraf --config telegraf.conf
popd
echo 'done.'

