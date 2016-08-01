""" Unit testing...
"""
# run with  py.test -s tests/test.py
import sys
import json
import logging

from os.path import join
import logging.config

from nameko.web.handlers import http
from werkzeug.wrappers import Response
from werkzeug import exceptions

try:
    from agents_common.html_utils import html2md
    from agents_common.policies_util import generate_hash
    from agents_common.scraper_utils import url2filenamedashes
except ImportError:
    print('agents_common is not installed '
          'or does not contain one of the required modules,'
          ' trying to find it inside this program path')
    try:
        from config import AGENTS_MODULE_PATH
        sys.path.append(AGENTS_MODULE_PATH)
        from agents_common.html_utils import html2md
        from agents_common.policies_util import generate_hash
        from agents_common.scraper_utils import url2filenamedashes
    except ImportError:
        print('agents_common not found in this program path, '
              'you need to install it or'
              ' create a symlink inside this program path')
        sys.exit()

from analyse_url.config import STORE_UPDATE_DOC_URL, AGENT_TYPE, SERVICE_NAME
from analyse_url.config_common import FS_PATH, PAGE_TYPE

from analyse_url.analyse_utils import retrieve_content_store, retrieve_hash_store, \
    save_content_store, post_store_hash, generate_urls_data, generate_doc_id, \
    scraper_content, post_store


logger = logging.getLogger(__name__)


def test_gen_store_update_url_hash_payload():
    url = 'https://guardianproject.info/home/data-usage-and-protection-policies/'
    etag = ''
    last_modified = ''
    hash_md = "577cd1563b7d08dea2864cad528bdc3d3b8ab64e1ecd49a092e95535e9d1cdcc"
    xpath = '//article'
    content = """# Data Usage and Protection Policies

**May the 4th, 2016**
..."""
    url_store_update = 'https://staging-store.openintegrity.org/pages-juga/_design/page/_update/timestamped/watch-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-577cd1563b7d08dea2864cad528bdc3d3b8ab64e1ecd49a092e95535e9d1cdcc'
    payload = {
        "xpath": "//article",
        "agent_ip": "78.142.19.213",
        "content": """# Data Usage and Protection Policies

**May the 4th, 2016**
...""",
        "header": {"etag": "", "last_modified": ""},
        "agent_type": "analyse",
        "page_type": "tos",
        "key": "https://guardianproject.info/home/data-usage-and-protection-policies/",
        "timestamp_measurement": "2016-07-29T23:13:15.511Z",
        "sha256": "577cd1563b7d08dea2864cad528bdc3d3b8ab64e1ecd49a092e95535e9d1cdcc"
    }

    doc_id = generate_doc_id(AGENT_TYPE, url, hash_md)
    logger.debug('Id of the document to store %s', doc_id)
    store_url = STORE_UPDATE_DOC_URL % doc_id
    logger.debug('The URL to store the page is %s', store_url)

    urls_data_dict = generate_urls_data(AGENT_TYPE, PAGE_TYPE,
                                        url,
                                        etag, last_modified,
                                        hash_md, content, xpath)
    # logger.debug('The data to store the page is %s', urls_data_dict)
    # ip will be different, remove the ip
    u = '-'.join(url_store_update.split('-')[0:2] +
                 url_store_update.split('-')[4:])
    e = '-'.join(store_url.split('-')[0:2] +
                 store_url.split('-')[4:])
    assert u == e
    payload.pop('agent_ip')
    payload.pop('timestamp_measurement')
    urls_data_dict.pop('agent_ip')
    urls_data_dict.pop('timestamp_measurement')
    assert payload == urls_data_dict


def test_post_update_pages_hash():
    store_url = 'https://staging-store.openintegrity.org/pages-juga/_design/page/_update/timestamped/analyse-176.10.104.243-httpsguardianproject.infohomedata-usage-and-protection-policies-577cd1563b7d08dea2864cad528bdc3d3b8ab64e1ecd49a092e95535e9d1cdcc'
    payload = {
        "xpath": "//article",
        "agent_ip": "78.142.19.213",
        "content": """# Data Usage and Protection Policies

**May the 4th, 2016**
...""",
        "header": {"etag": "", "last_modified": ""},
        "agent_type": "analyse",
        "page_type": "tos",
        "key": "https://guardianproject.info/home/data-usage-and-protection-policies/",
        "timestamp_measurement": "2016-07-29T23:13:15.511Z",
        "sha256": "577cd1563b7d08dea2864cad528bdc3d3b8ab64e1ecd49a092e95535e9d1cdcc"
    }
    r = post_store_hash(store_url, payload)
    assert r == 201
