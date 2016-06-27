"""analyse_url."""
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from werkzeug import exceptions
from os.path import join
import json
import yaml
import logging
import logging.config
# from logger import LoggingDependency
from config import CONFIG, FS_PATH, MD_URL, AGENT_TYPE
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
 store, put_md_url

logging.basicConfig(level=logging.DEBUG)
with open(CONFIG) as fle:
    config = yaml.load(fle)
if "LOGGING" in config:
    logging.config.dictConfig(config['LOGGING'])
logger = logging.getLogger(__name__)


class AnalyseURLService(object):
    name = "analyseurl"


    # @http('GET', '/analyseurl/<string:url>/<string:hash_html>')
    # def get_method(self, request, url, hash_html):
    #     # return json.dumps({'hash': hash})
    #     logger.debug('url: %s', url)
    #     logger.debug('hash_html: %s', hash_html)
    #     return json.dumps({'url': url, 'hash_html': hash_html})


    # FIXME: temporally getting the values as POST data cause string:url
    # causes 409
    @http('POST', '/analyseurl')
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
        url = json_data.get('url')
        logger.debug('url: %s', url)
        hash_html = json_data.get('hash_html')
        etag = json_data.get('etag')
        last_modified = json_data.get('last_modified')
        html_filepath = join(FS_PATH, url2filenamedashes(url) + hash_html + '.html')
        content_html = retrieve_content_store(html_filepath)
        content_md = html2md(content_html)
        hash_md = generate_hash(content_md)
        md_filepath = join(FS_PATH, url2filenamedashes(url) + hash_md + '.md')
        md_hash_in_store = retrieve_hash_store(md_filepath)
        if not md_hash_in_store:
            logger.info('hash is not in the file system')
            store(md_filepath, content_md)
            put_md_url(MD_URL, url, hash_md, content_md, etag, last_modified,
                       AGENT_TYPE)
        return Response(json.dumps({'url': url}))
