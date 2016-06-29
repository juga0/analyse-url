"""analyse_url util functions."""
from os.path import join, isfile, isdir, dirname
from os import makedirs
import requests
import sys
import codecs
import logging
try:
    from agents_common.scraper_utils import timestamp, url2filenamedashes
    from agents_common.system_utils import obtain_public_ip
except:
    from config import AGENTS_MODULE_PATH
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.scraper_utils import timestamp, url2filenamedashes
    from agents_common.system_utils import obtain_public_ip

# from config import AGENT_ID

logger = logging.getLogger(__name__)


def retrieve_content_store(filepath, encoding='utf-8'):
    """
    """
    # filepath = join(dirpath, url + hash_content)
    logger.debug('checking whether %s exists', filepath)
    if isfile(filepath):
        logger.info('html with with path %s exists', filepath)
        with codecs.open(filepath, "r", encoding) as f:
            content = f.read()
        return content
    return ''


def retrieve_hash_store(filepath):
    """
    """
    # filepath = join(dirpath, url + hash_content)
    logger.debug('checking whether %s exists', filepath)
    if isfile(filepath):
        logger.info('html with with path %s exists', filepath)
        return True
    return False


def store(filepath, content, encoding='utf-8'):
    """
    """
    # filepath = join(dirpath, url + hash_page_html)
    if not isdir(dirname(filepath)):
        logger.debug('creating dir %s', dirname(filepath))
        makedirs(dirname(filepath))
    logger.debug('writing content to %s', filepath)
    with open(filepath, 'w') as f:
        f.write(content)


def generate_agent_id(url, agent_type, etag=None, last_modified=None):
    """
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-20160613T190136Z
    """
    ip = obtain_public_ip()
    urlfilename = url2filenamedashes(url)
    # timestamp is not the the system timestamp but the etag/last_modified
    # dt = timestamp()

    agent_id = '-'.join([agent_type, ip, urlfilename, dt])
    return agent_id


def generate_agent_hash_id(url, agent_type, sha):
    """
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-sha
    """
    ip = obtain_public_ip()
    urlfilename = url2filenamedashes(url)
    # FIXME: do we need the timestamp
    # dt = timestamp()
    agent_id = '-'.join([agent_type, ip, urlfilename, sha])
    return agent_id


def put_md_url(db_url, url, hash_content, content_md, etag, last_modified,
               agent_type):
    """
    https://api.openintegrity.org/policies/https://guardianproject.info/home/data-usage-and-protection-policies/
    data = {
       "_id": "tos-1",
       "key": "https://guardianproject.info/home/data-usage-and-protection-policies/",
       "agent_id": "agent-tos-1",
       "agent_type": "analyse-tos",
       "timestamp": $AGENT_TIMESTAMP,
       "header": {
           "etag": ""
           "last_modified": "Mon, 13 Jun 2016 19:01:36 GMT""
       },
       "content": "### Policy/n * blah/n"
    }
    """
    data = {
       "_id": generate_agent_hash_id(url, agent_type, hash_content),
       "key": url,
       "agent_ip": obtain_public_ip(),
       "agent_type": agent_type,
       "timestamp": timestamp(),
       "header": {
           "etag": etag,
           "last_modified": last_modified
       },
       "content": content_md
    }
    logger.debug('post store_url %s with json %s', db_url, data)
    r = requests.post(db_url, json=data)
    return r.status_code
