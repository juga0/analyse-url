"""analyse_url."""
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
    from agents_common.data_structures_utils import get_value_from_key_index
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
        from agents_common.data_structures_utils import get_value_from_key_index
    except ImportError:
        print('agents_common not found in this program path, '
              'you need to install it or'
              ' create a symlink inside this program path')
        sys.exit()

from config import STORE_UPDATE_DOC_URL, AGENT_TYPE, SERVICE_NAME, \
    STORE_LATEST_VIEW_URL
from config_common import FS_PATH, PAGE_TYPE

from analyse_utils import retrieve_content_store, retrieve_hash_store, \
    save_content_store, post_store_hash, generate_urls_data, generate_doc_id, \
    scraper_content, get_store_hash, get_store_hash_md, get_store

from config_common import LOGGING
logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)


class AnalyseURLService(object):
    name = SERVICE_NAME

    # TODO: handle errors
    # TODO: use nameko events
    # FIXME: instead of getting xpath from requests,
    # it should query again the store and get the xpath
    # for the url in the request ?
    @http('POST', '/' + SERVICE_NAME)
    def analyse_url(self, request):
        """
        """
        if request.method != "POST":
            raise exceptions.MethodNotAllowed
        # FIXME: is this the best way to obtain post payload?
        #        or should insted use .form or .vaules or .data?
        data = request.get_data()
        logger.debug('Received payload %s', data)
        fetch_data = json.loads(data)
        url = fetch_data.get('entity')
        logger.debug('entity: %s', url)

        xpath = fetch_data.get("context").get("xpath")
        logger.debug('xpath %s', xpath)
        hash_html_fetch = fetch_data.get("value").get("sha256_html")
        logger.debug('hash %s', hash_html_fetch)
        # hash_md_fetch = fetch_data.get('sha256_md')
        # logger.debug('hash %s', hash_md_fetch)
        # attribute = fetch_data.get('attribute')


        # if the html is not in the FS, the markdown and its hash can't be
        # calculated, no matter if it's already in the store or not
        logger.debug('Getting hash from store.')
        store_data = get_store(STORE_LATEST_VIEW_URL % (url,), ['rows', 0, 'value'])
        logger.debug('Data from the store %s.', store_data)
        hash_html_store = get_value_from_key_index(store_data, ['value', 'sha256_html'])
        hash_md_store = get_value_from_key_index(store_data, ['value', 'sha256_md'])
        # NOTE: if hash_html is not still in the store, None will be different
        # to ''
        if hash_html_store != hash_html_fetch:
            html_filepath = join(FS_PATH, url2filenamedashes(url),
                                 hash_html_fetch + '.html')
            content_html = retrieve_content_store(html_filepath)
            if content_html:
                content_xpath = scraper_content(xpath, content_html)
                content_md = html2md(content_xpath)
                # logger.debug('Content md: %s', content_md)
                hash_md = generate_hash(content_md)
                logger.debug('Hash of the markdown in the store is %s',
                             hash_md)
                md_filepath = join(FS_PATH, url2filenamedashes(url),
                                   hash_md + '.md')
                hash_md_fs = retrieve_hash_store(md_filepath)
                logger.debug('Hash of the markdown in the FS is %s',
                             hash_md_fs)
                # if hash_md_fs is None, store it in the FS

                # if the md with same hash is already in the FS,
                # it's not needed to
                # store it in the FS, but it's still needed to check that
                # it's in  the store
                if not hash_md_store or (hash_md_store != hash_md):
                    logger.debug('Generating payload.')
                    logger.debug('Payload without processing: %s', fetch_data)
                    analyse_data = generate_urls_data(fetch_data, content_md,
                                                      hash_md, AGENT_TYPE)

                    logger.debug('Payload to store %s', analyse_data)
                    doc_id = generate_doc_id(AGENT_TYPE, url, hash_md)
                    logger.debug('Id of the document to store %s', doc_id)
                    store_url = STORE_UPDATE_DOC_URL % doc_id
                    logger.debug('Storing content in the store.')
                    post_store_hash(store_url, analyse_data)

                if not hash_md_fs:
                    logger.info('Hash is not in the file system.')
                    save_content_store(md_filepath, content_md)
            else:
                logger.error('The hash of the page html is not in the '
                             'store but it can not be calculated because the '
                             'the page html is not in the filesystem either.'
                             'Something went wrong.')
                sys.exit()
        return Response(status=200)
# TODO: add main
