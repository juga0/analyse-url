"""Configuration for fetch-url agent."""
from os import environ
from config_common import NAME_SEPARATOR, AGENT_NAME, AGENT_SUFFIX,\
    STORE_URL, STORE_CONFIG_DB, PAGE_TYPE

AGENT_TYPE = 'analyse'
SERVICE_NAME = 'analyse_page_tos'

# configuration that depends on common constants
STORE_DB = environ.get('STORE_CONFIG_DOC') or \
    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_DB_URL = '/'.join([STORE_URL, STORE_DB])
STORE_LATEST_VIEW = '_design/page/_view/latest?group=true&' \
    'startkey=["page", "%s"]'
STORE_LATEST_VIEW_URL = '/'.join([STORE_DB_URL, STORE_LATEST_VIEW])
# https://staging-store.openintegrity.org/pages-juga/_design/page/_view/latest?reduce=true&group_level=2&startkey=["page","tos","https://guardianproject.info/home/data-usage-and-protection-policies/"]&endkey=["page","tos","https://guardianproject.info/home/data-usage-and-protection-policies/",{}]

STORE_UPDATE_DOC = "_design/page/_update/timestamped/%s"
STORE_UPDATE_DOC_URL = '/'.join([STORE_DB_URL, STORE_UPDATE_DOC])

STORE_CONFIG_DOC = environ.get('STORE_CONFIG_DOC') or \
                    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_CONFIG_URL = '/'.join([STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC])
# STORE_CONFIG_URL = https://staging-store.openintegrity.org/config/pages-juga

