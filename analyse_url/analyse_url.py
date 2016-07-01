"""analyse_url."""
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from werkzeug import exceptions
from os.path import join
import json
import logging
import logging.config
# from logger import LoggingDependency
from config import FS_PATH, URLS_DOC_URL, AGENT_TYPE, SERVICE_NAME
try:
    from agents_common.html_utils import html2md
    from agents_common.policies_util import generate_hash
    from agents_common.scraper_utils import url2filenamedashes
except:
    from config import AGENTS_MODULE_PATH
    import sys
    sys.path.append(AGENTS_MODULE_PATH)
    from agents_common.html_utils import html2md
    from agents_common.policies_util import generate_hash
    from agents_common.scraper_utils import url2filenamedashes
from analyse_utils import retrieve_content_store, retrieve_hash_store, \
    save_content_store, put_store_hash, generate_urls_data, generate_doc_id, \
    scraper_content

logging.basicConfig(level=logging.DEBUG)
try:
    from config import LOGGING
    logging.config.dictConfig(LOGGING)
except:
    print 'No LOGGING configuration found.'
logger = logging.getLogger(__name__)


class AnalyseURLService(object):
    name = SERVICE_NAME

    # FIXME: temporally getting the values as POST data cause string:url
    # causes 409
    # TODO: handle errors
    # TODO: use nameko events
    # FIXME: instead of getting xpath from requests,
    # it should query again the store and get the xmpat
    # for the url in the request
    @http('POST', '/' + SERVICE_NAME)
    def analyse_url(self, request):
        """
        """
        if request.method != "POST":
            raise exceptions.MethodNotAllowed
        logger.debug('request: %s', request)
        # FIXME: is this the best way to obtain post payload?
        #        or should insted use .form or .vaules or .data?
        data = request.get_data()
        logger.debug('data %s', data)
        json_data = json.loads(data)
        logger.debug('json data %s', json_data)
        # url = json_data.get('url')
        # logger.debug('url: %s', url)
        # hash_html = json_data.get('hash_html')
        # etag = json_data.get('etag')
        # last_modified = json_data.get('last_modified')
        url = json_data.get('key')
        logger.debug('key: %s', url)
        header = json_data.get('header')
        if header:
            etag = header.get('etag')
            logger.debug('etag: %s', etag)
            last_modified = header.get('last_modified')
            logger.debug('last_modified: %s', last_modified)
        xpath = json_data.get('xpath')
        hash_html = json_data.get('sha256')

        html_filepath = join(FS_PATH, url2filenamedashes(url),
                             hash_html + '.html')
        content_html = retrieve_content_store(html_filepath)
        if content_html:
            content_xpath = scraper_content(xpath, content_html)
            content_md = html2md(content_xpath)
            hash_md = generate_hash(content_md)
            md_filepath = join(FS_PATH, url2filenamedashes(url), hash_md + '.md')
            md_hash_in_store = retrieve_hash_store(md_filepath)
            if not md_hash_in_store:
                logger.info('Hash is not in the file system.')
                save_content_store(md_filepath, content_md)
                data = generate_urls_data(AGENT_TYPE, url, etag, last_modified,
                                          content_md)
                doc_id = generate_doc_id(AGENT_TYPE, url, hash_md)
                store_url = URLS_DOC_URL % doc_id
                put_store_hash(store_url, data)
        return Response(status=200)
