"""Configuration for fetch-url agent."""
from os import environ
from config_common import NAME_SEPARATOR, AGENT_NAME, AGENT_SUFFIX,\
    STORE_URL, STORE_CONFIG_DB

AGENT_TYPE = 'analyse'
SERVICE_NAME = 'analyse_page_tos'

# configuration that depends on common constants
STORE_DB = environ.get('STORE_CONFIG_DOC') or \
    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_DB_URL = '/'.join([STORE_URL, STORE_DB])

STORE_LATEST_VIEW = "_design/" + STORE_DB +\
    """/_view/latest?reduce=true&group_level=2&""" \
    """startkey=["%s"]&endkey=["%s",{}]"""
STORE_LATEST_VIEW_URL = '/'.join([STORE_DB_URL, STORE_LATEST_VIEW])
# STORE_LATEST_VIEW_URL = """https://staging-store.openintegrity.org/github-repo-issues/_design/github-repo-issues/_view/latest?reduce=true&group_level=2&startkey=["%s"]&endkey=["%s",{}]"""

STORE_UPDATE_DOC = "_design/" + STORE_DB + "/_update/timestamped/%s"
STORE_UPDATE_DOC_URL = '/'.join([STORE_DB_URL, STORE_UPDATE_DOC])
# STORE_UPDATE_DOC_URL = "https://staging-store.openintegrity.org/github-repo-issues/_design/github-repo-issues/_update/timestamped/analyse-github-repo-issues-84.251.91.165-https-guardianproject.info-home-data-usage-and-protection-policies--etag"

STORE_CONFIG_DOC = environ.get('STORE_CONFIG_DOC') or \
                    NAME_SEPARATOR.join([AGENT_NAME, AGENT_SUFFIX])
STORE_CONFIG_URL = '/'.join([STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC])
# STORE_CONFIG_URL = https://staging-store.openintegrity.org/config/page-tos-juga

