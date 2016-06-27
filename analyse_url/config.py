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

# FIXME: the ide should be generated other way
AGENT_ID = 'agent-tos-1'
# agent_id, doc_id
AGENT_TYPE = 'analyse-url'

# configuration yaml file. All the configuration here could go there
CONFIG = join(ROOT_PATH, 'config.yaml')

FS_PATH = join(PROJECT_PATH, 'policies', 'data')

# analyse-url configuration
# https://api.openintegrity.org/policies/https://guardianproject.info/home/data-usage-and-protection-policies/
COUCHDB_URL = 'https://staging-store.openintegrity.org'
MD_DB = 'tos'
MD_URL = '/'.join([COUCHDB_URL,MD_DB,'%s'])

# COUCHDB_URL = 'https://api.openintegrity.org'
# MD_DB = 'policies'
# MD_DOC = 'watch-url'


# rabbitmq configuration
AMQP_CONFIG = {'AMQP_URI': 'amqp://guest:guest@localhost'}

# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': "%(levelname)s:%(name)s - %(module)s - %(message)s"
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'nameko': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}
