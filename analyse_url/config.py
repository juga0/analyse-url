"""fetch-rul configuration."""
from os.path import join, abspath, dirname


BASE_PATH = abspath(__file__)
# BASE_PATH = abspath('.')
ROOT_PATH = dirname(BASE_PATH)
PROJECT_PATH = dirname(ROOT_PATH)
ROOT_PROJECT_PATH = dirname(PROJECT_PATH)
# in case agents-common-code is not installed, the path to it is requered
AGENTS_MODULE_DIR = 'agents-common-code'
AGENTS_MODULE_PATH = join(ROOT_PROJECT_PATH, AGENTS_MODULE_DIR)

AGENT_TYPE = 'analyse-url'
SERVICE_NAME = 'analyseurl'

FS_PATH = join(PROJECT_PATH, 'data')

# couchdb configuration and urls
STORE_URL = 'https://staging-store.openintegrity.org'
URLS_DB = 'url'
URLS_DB_URL = '/'.join([STORE_URL, URLS_DB])
URLS_DOC_URL = '/'.join([URLS_DB_URL, "%s"])


# rabbitmq configuration
AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}

# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "%(levelname)s:%(name)s - %(module)s - %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    # 'loggers': {
    #     'nameko': {
    #         'level': 'DEBUG',
    #         'handlers': ['console']
    #     }
    # },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}
