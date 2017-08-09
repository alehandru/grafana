import os
import json
import requests

# Grafana settings
grafana_host = 'localhost'
grafana_port = 3000
grafana_user = 'admin'
grafana_password = 'admin'
grafana_url = os.path.join('http://', '%s:%u' % (grafana_host, grafana_port))

# Elastic search settings
elasticsearch_host = 'localhost'
elasticsearch_port = 9200

# Connection settings
max_number_retries = 100

def print_data_sources(session):
    url_data_sources = os.path.join(grafana_url, 'api', 'datasources')
    datasources_get = session.get(url_data_sources)
    datasources = datasources_get.json()
    print '*********************************'
    print 'DATA SOURCES:'
    print '*********************************'
    for d in datasources:
        print 'data source: ', d

def add_snap_data_source(session):
    url_data_sources = os.path.join(grafana_url, 'api', 'datasources')
    response = session.post(
       url_data_sources,
       data=json.dumps({
          'name': 'Snap',
          'type': 'elasticsearch',
          'url': 'http://%s:%u' % (elasticsearch_host, elasticsearch_port),
          'access': 'proxy',
          'isDefault': False,
          'database': 'snap*',
          'jsonData': {'timeField': 'Timestamp'},
          'basicAuth': False}),
          headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print 'Add Snap source - OK'
    else:
        print 'Add Snap source - FAILED'

def add_dashboard(filename):
    with open(filename) as json_data:
        dashboard_json = json.load(json_data)
        body = {}
        body['dashboard'] = dashboard_json
        body['overwrite'] = True
        url_dashboards = os.path.join(grafana_url, 'api', 'dashboards', 'db')
        response = session.post(
                url_dashboards,
                data=json.dumps(body),
                headers={'Content-Type': 'application/json',
                         'Accept': 'application/json'})
        if response.status_code == 200:
            print 'Add %s dashboard - OK' %(filename)
        else:
            print 'Add %s dashboard - FAILED' %(filename)

def login():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=max_number_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.post(
       os.path.join(grafana_url, 'login'),
       data=json.dumps({
          'user': grafana_user,
          'email': '',
          'password': grafana_password }),
       headers={'content-type': 'application/json'})
    if response.status_code == 200:
        print 'connected'
        return session
    print 'failed to connect'
    return None

session = login()
add_snap_data_source(session)
print_data_sources(session)
add_dashboard('snap-metrics.json')

