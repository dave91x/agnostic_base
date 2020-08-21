import os
import json
import dramatiq
import requests
from dramatiq.brokers.redis import RedisBroker
from titanium_core.transaction_services import TransactionLogger


redis_broker = RedisBroker(host="redis", port=6379, db=0)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def process_event(event):
    base_url = os.environ['BASE_URL']
    vault_role_id = os.environ['VAULT_ROLE_ID']
    vault_secret_id = os.environ['VAULT_SECRET_ID']
    logger_creds = {
        "user": "vidado_serverless",
        "host": "postgres",
        "port": 5432,
        "database": "agnostic",
        "password": os.environ['POSTGRES_PASSWORD'],
        "use_ssl": False
    }

    try:
        logger = TransactionLogger(logger_creds)
    except:
        logger = None

    e = json.loads(event)
    print('picked up event:  {}'.format(e))

    userid = e['userid']
    event_name = e['name']
    details = e['details']

    transaction = {
        'event_name': event_name,
        'action': 'none',
        'user_id': userid,
        'object_parent_id': 0,
        'object_id': details.get('batch_id', 0),
        'notes': {
            'conductor_event_id': e.get('id', 1),
        },
        'status': 'failed'
    }

    # request short-lived token from vault to access secrets
    vault_token_request_url = 'http://vault:8200/v1/auth/approle/login'
    vault_token_request_payload = {
        'role_id': vault_role_id,
        'secret_id': vault_secret_id
    }
    auth_resp = requests.post(vault_token_request_url, json=vault_token_request_payload).json()
    # print(auth_resp)
    vault_token = auth_resp['auth']['client_token']

    # use the generated token to retrieve the customer pipeline config and database creds from vault
    vault_url = 'http://vault:8200/v1/vidado/customer_configs/data/config_{}'.format(userid)
    vault_headers = {'X-Vault-Token': vault_token}

    vault_resp = requests.get(vault_url, headers=vault_headers).json()
    # print(vault_resp)
    pipeline_config = vault_resp['data']['data']

    if event_name == 'batch-digitized':
        api_endpoint = '/api/v1/batch/{}'.format(details['batch_id'])

        action = requests.get('{}{}'.format(base_url, api_endpoint),
                              headers={'Captricity-API-Token': pipeline_config['customer']['shreddr_api_token']})

        print(json.dumps(action.json(), indent=2))

    wrap_logger(logger, transaction, status='exported', verbose=True)

    print('processed event:  {}'.format(e))


def wrap_logger(logger, transaction, status, verbose=False):
    # code to prevent the transaction logging from burying the entire execution
    if logger:
        try:
            logger.log_event_with_status(transaction, status=status)
            if verbose:
                print('transaction status:  {}'.format(status))
                print(json.dumps(transaction, indent=2))
                print('\n----------------------------\n')
        except:
            print('Status:  {}'.format(status))
            print('Failed to connect for logging:  {}'.format(transaction))
    else:
        print('NO LOGGER PRESENT')
        print('Status:  {}'.format(status))
        print('Failed to connect for logging:  {}'.format(transaction))
