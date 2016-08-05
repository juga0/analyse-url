"""analyse_url util functions."""
from os.path import isfile, isdir, dirname
from os import makedirs
import requests
import sys
import codecs
import logging

try:
    from agents_common.scraper_utils import url2filenamedashes, \
        now_timestamp_ISO_8601
    from agents_common.system_utils import obtain_public_ip
    from agents_common.data_structures_utils import get_value_from_key_index
except ImportError as e:
    print('agents_common is not installed '
          'or does not contain one of the required modules,'
          ' trying to find it inside this program path')
    try:
        from config import AGENTS_MODULE_PATH
        sys.path.append(AGENTS_MODULE_PATH)
        from agents_common.scraper_utils import url2filenamedashes, \
            now_timestamp_ISO_8601
        from agents_common.system_utils import obtain_public_ip
        from agents_common.data_structures_utils import get_value_from_key_index
    except ImportError as e:
        print('agents_common not found in this program path, '
              'you need to install it or'
              ' create a symlink inside this program path')
        sys.exit()

from config_common import AGENT_ATTRIBUTE, AGENT_PAYLOAD

logger = logging.getLogger(__name__)


def generate_doc_id(agent_type, url, url_path_id=''):
    """
    Return and string like:
    analyse-url-192.168.1.1-https-www.whispersystems.org-signal-privacy-20160613T190136Z.
    """
    ip = obtain_public_ip()
    urlfilename = url2filenamedashes(url)
    doc_id = '-'.join([agent_type, ip, urlfilename, url_path_id])
    logger.debug('doc_id %s', doc_id)
    return doc_id


# def generate_urls_data(agent_type, page_type, url, etag, last_modified,
#                        xpath='', content='', attribute=AGENT_ATTRIBUTE,
#                        hash_html='', hash_md=''):


def generate_urls_data(dict_data, content, hash_md, agent_type):
    """
    {"attribute": "page/content", "context": {"xpath": "//div[@id='body']", "agent_type": "watch", "timestamp_measurement": "2016-08-05T13:21:40.396293Z", "page_type": "tos", "agent_ip": "65.181.112.128"}, "value": {"header": {"last-modified": "Mon, 01 Sep 1997 01:03:33 GMT", "etag": "None"}, "sha256_html": "43fa5a6f123a2cbb7a6c84b6ca9511b26ffef385121d026fdbab2202b7534e1f"}, "entity": "http://www.t-mobile.com/Templates/Popup.aspx?PAsset=Ftr_Ftr_TermsAndConditions&amp;print=true"}
     {
         "entity": "%(entity)",
         "attribute": "page/content",
         "value": {
             "header": {
                 "etag": "%(etag)",
                 "last-modified": "%(last_modified)"
             },
             "content": "%(content)",
             "sha256_html": "%(sha256_html)",
             "sha256_md": "%(sha256_md)"
         },
         "context": {
             "timestamp_measurement": "%(timestamp_measurement)",
             "agent_type": "%(agent_type)",
             "agent_ip": "%(agent_ip)",
             "page_type": "%(page_type)",
             "xpath": "%(xpath)"
         }
     }
    """
    logger.debug('Generating payload.')
    dict_data['value']['sha256_md'] = hash_md
    dict_data['value']['content'] = content
    dict_data['context']['agent_type'] = agent_type
    dict_data['context']['timestamp_measurement'] = now_timestamp_ISO_8601()
    dict_data['context']['agent_ip'] = obtain_public_ip()
    return dict_data


def retrieve_content_store(filepath, encoding='utf-8'):
    """
    """
    # filepath = join(dirpath, url + hash_content)
    logger.debug('Checking whether %s exists.', filepath)
    if isfile(filepath):
        logger.info('%s exists.', filepath)
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


def get_store(url, json_key=None):
    logger.debug('GET url %s', url)
    r = requests.get(url)
    logger.info('Reguest GET %s returns %s', url, r.reason)
    logger.debug('Response: %s', r)
    try:
        logger.debug('Response content is json.')
        data = r.json()
    except ValueError:
        logger.debug('Response content is not json')
        return r.text
    if json_key:
        logger.debug('Searching for json key %s in the response.', json_key)
        value = get_value_from_key_index(data, json_key)
        logger.debug('The value of the key is %s', value)
        return value
    return data


def get_store_hash(url):
    # TODO: manage conflict when status code 409
    hash = last_modified = ''
    logger.debug('Contacting store.')
    rows = get_store(url, 'rows')
    if rows:
        keys_indexes = [0, 'value', 'sha256']
        try:
            hash = get_value_from_key_index(rows, keys_indexes)
        except (KeyError, IndexError):
            keys_indexes = ['rows', 0, 'value', 'sha256']
            try:
                last_modified = get_value_from_key_index(rows, keys_indexes)
            except (KeyError, IndexError):
                pass
    return hash, last_modified


def get_store_hash_md(url):
    # TODO: manage conflict when status code 409
    hash = ''
    rows = get_store(url, 'rows')
    if rows:
        keys_indexes = ['rows', 0, 'value', 'sha256_md']
        try:
            hash = get_value_from_key_index(rows, keys_indexes)
        except (KeyError, IndexError):
            pass
    return hash


def post_store(url, data, only_status_code=False):
    logger.info('POST url %s' % url)
    if isinstance(data, dict):
        try:
            r = requests.post(url, json=data)
        except ConnectionError as e:
            logger.error(e)
            return None
    else:
        try:
            r = requests.post(url, data=data)
        except ConnectionError as e:
            logger.error(e)
            return None
    logger.info('Request POST %s returned %s', url, r.reason)
    if only_status_code:
        return r.status_code
    return r


def post_store_hash(url, data):
    """
    Like put_store_hash but using method POST
    """
    logger.info('post_store_hash being called')
    return post_store(url, data, only_status_code=True)


def put_store(url, data, only_status_code=False):
    logger.debug('PUT url %s' % url)
    # TODO: create database if it doesn't exist
    if isinstance(data, dict):
        r = requests.put(url, json=data)
    else:
        r = requests.put(url, data=data)
    logger.info('Reguest PUT %s returns %s', url, r.reason)
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
