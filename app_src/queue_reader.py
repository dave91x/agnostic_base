import os
import json
import dramatiq
import requests
from dramatiq.brokers.redis import RedisBroker


redis_broker = RedisBroker(host="redis", port=6379, db=0)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def process_event(event):
    # base_url = 'https://staging.captricity.com/'
    # vault_token = os.environ['VAULT_TOKEN']

    e = json.loads(event)
    print('picked up event:  {}'.format(e))

    # userid = e['userid']
    # event_name = e['name']
    # details = e['details']
    #
    # vault_url = 'http://vault:8200/v1/customer_configs/data/config_{}'.format(userid)
    # vault_headers = {'X-Vault-Token': vault_token}
    #
    # vault_resp = requests.get(vault_url, headers=vault_headers).json()
    #
    # pipeline_config = vault_resp['data']['data']
    #
    # if event_name == 'batch-digitized':
    #     api_endpoint = 'api/v1/batch/{}'.format(details['batch_id'])
    #
    #     action = requests.get('{}{}'.format(base_url, api_endpoint),
    #                           headers={'Captricity-API-Token': pipeline_config['customer']['shreddr_api_token']})
    #
    #     print(json.dumps(action.json(), indent=2))

    print('processed event:  {}'.format(e))
