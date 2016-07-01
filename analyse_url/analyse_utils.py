"""analyse_url util functions."""
from os.path import isfile, isdir, dirname
from os import makedirs
import requests
import sys
import codecs
import logging
try:
    from agents_common.scraper_utils import url2filenamedashes, \
        now_timestamp_str_nodashes
    from agents_common.system_utils import obtain_public_ip
except:
    from config import AGENTS_MODULE_PATH
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.scraper_utils import url2filenamedashes, \
        now_timestamp_str_nodashes
    from agents_common.system_utils import obtain_public_ip

logger = logging.getLogger(__name__)


def generate_doc_id(agent_type, url, url_path_id=''):
    """
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-sha
    """
    ip = obtain_public_ip()
    urlfilename = url2filenamedashes(url)
    doc_id = '-'.join([agent_type, ip, urlfilename, url_path_id])
    logger.debug('doc_id %s', doc_id)
    return doc_id


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


def save_content_store(filepath, content, encoding='utf-8'):
    """
    """
    logger.debug('writing content to %s', filepath)
    logger.debug('content type %s', type(content))
    if not isdir(dirname(filepath)):
        logger.debug('creating dir %s', dirname(filepath))
        makedirs(dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(content.encode(encoding))


def generate_urls_data(agent_type, url, etag, last_modified,
                       content=''):
    """
    https://api.openintegrity.org/url/analyse-url-https-guardianproject.info/home-data-usage-and-protection-policies-sha
    data = {
       "key": "https://guardianproject.info/home/data-usage-and-protection-policies/",
       "agent_ip": 1.2.3.4
       "agent_type": "watch-url",
       "timestamp": $AGENT_TIMESTAMP,
       "header": {
           "etag": ""
           "last_modified": "Mon, 13 Jun 2016 19:01:36 GMT"
       },
       "content": "### Policy/n * blah/n"
    }
    """
    data = {
       "key": url,
       "agent_ip": obtain_public_ip(),
       "agent_type": agent_type,
       "timestamp": now_timestamp_str_nodashes(),
       "header": {
           "etag": etag,
           "last_modified": last_modified
       },
       "content": content
    }
    return data


def put_store(url, data, only_status_code=False):
    logger.debug('PUT url %s' % url)
    if isinstance(data, dict):
        r = requests.put(url, json=data)
    else:
        r = requests.put(url, data=data)
    if only_status_code:
        return r.status_code
    return r


def put_store_hash(url, data):
   """
   Put in the store the etag or last_modified for a given url.
   The url of the store is like this:
   watch-url-89.31.96.168-https-guardianproject.info-home-data-usage-and-\
   protection-policies--\
   308260b059be166829326014df56da5d5b59b3157944f8612cfe51925aacc0ae
   The json data structure is like this:
   {
   "key":"https://www.whispersystems.org/signal/privacy/",
   "agent_ip": "1.2.3.4",
   "agent_type":"analyse-url",
   "timestamp": "20160623T120243Z",
   "header":{
       "etag":"",
       "last-modified":"Mon, 13 Jun 2016 19:01:36 GMT"
       },
   "content":"# Privacy Policy\n\n..."
   }
   """
   # To create new document you can either use a POST operation or a PUT operation. To create/update a named document using the PUT operation
   # To update an existing document, you also issue a PUT request. In this case, the JSON body must contain a _rev property, which lets CouchDB know which revision the edits are based on. If the revision of the document currently stored in the database doesn't match, then a 409 conflict error is returned.
   # It is recommended that you avoid POST when possible, because proxies and other network intermediaries will occasionally resend POST requests, which can result in duplicate document creation. If your client software is not capable of guaranteeing uniqueness of generated UUIDs, use a GET to /_uuids?count=100 to retrieve a list of document IDs for future PUT requests. Please note that the /_uuids-call does not check for existing document ids; collision-detection happens when you are trying to save a document.
   # FIXME: manage conflict
   return put_store(url, data, only_status_code=True)



def scraper_content(xpath, content):
    logger.debug('content type %s', type(content))
    from lxml import html, etree
    tree = html.fromstring(content)
    e = tree.xpath(xpath)
    html_text = etree.tostring(e[0])
    logger.debug('content type after xpath %s', type(html_text))
    return html_text
