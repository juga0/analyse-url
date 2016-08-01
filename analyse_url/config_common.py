"""Common configuration for watch/fetch/analyse-page-tos agents."""
# urljoin only join with one argument
# from urlparse import urljoin
from os.path import join, abspath, dirname
from os import environ

# FIXME: set default to false
DEBUG = environ.get('DEBUG') or True

PAGE_TYPE = 'tos'
AGENT_NAME = 'pages'
AGENT_SUFFIX = 'juga'
NAME_SEPARATOR = '-'
# this will be overwroten by the config interval in the store
INTERVAL = 60
CONFIG_DOC_KEY = 'config'

# paths
############################
BASE_PATH = abspath(__file__)
# BASE_PATH = abspath('.')
ROOT_PATH = dirname(BASE_PATH)
PROJECT_PATH = dirname(ROOT_PATH)
ROOT_PROJECT_PATH = dirname(PROJECT_PATH)
# in case agents-common-code is not installed, the path to it is requered
AGENTS_MODULE_DIR = 'agents-common-code'
AGENTS_MODULE_PATH = join(ROOT_PROJECT_PATH, AGENTS_MODULE_DIR)

# fs store
FS_PATH = join(PROJECT_PATH, 'data')

# URLs
############################
# couchdb configuration and urls
STORE_URL = environ.get('STORE_URL') or \
    'https://staging-store.openintegrity.org'
STORE_CONFIG_DB = environ.get('STORE_CONFIG_DB') or 'config'
STORE_CONFIG_DOC = environ.get('STORE_CONFIG_DOC') or \
                    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_CONFIG_URL = '/'.join([STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC])
# STORE_CONFIG_URL = https://staging-store.openintegrity.org/config/page-tos-juga

# data
############################
AGENT_PAYLOAD = """{
    "key": "%(key)",
    "agent_ip": "%(agent_ip)",
    "agent_type": "%(agent_type)",
    "page_type": "%(page_type)",
    "header": {
        "etag": "%(etag)",
        "last-modified": "%(last_modified)"
    },
    "content": "%(content)"
    "timestamp_measurement": "%(timestamp_measurement)"
}"""

# nameko
############################
CONFIG_YAML_PATH = join(ROOT_PATH, 'config.yaml')
WEB_SERVER_ADDRESS = '127.0.0.1:8002'
# rabbitmq configuration
AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}

LOG_LEVEL = environ.get('LOG_LEVEL') or 'DEBUG'
# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "%(levelname)s:%(module)s - %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'nameko': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'analyse_url': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'analyse_utils': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    },
    # 'root': {
    #     'level': 'DEBUG',
    #     'handlers': ['console']
    # }
}
