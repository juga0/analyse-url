# fetch-url

Work in progress...

## Installation in Debian/Ubuntu

### System dependencies

`sudo apt-get install python-dev`
For lxml package:
 `sudo apt-get install libxml2-dev libxslt1-dev`
For PyYAML package:
`sudo apt-get install libyaml-dev`
For cryptograpy package:
`sudo apt-get install libffi-dev`

### With virtualenv

#### Obtain virtualenv

Check https://virtualenv.pypa.io/en/latest/installation.html or if Debian equal/newer than jessie (virtualenv version equal or greater than 1.9)

    sudo apt-get install python-virtualenv

#### Create a virtualenv

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/oiienv
    source ~/.virtualenvs/oiienv/bin/activate

#### Install dependencies in virtualenv

    git clone https://meta.openintegrity.org/agents/analyse-url.git
    cd analyse-url
    pip install -r requirements.txt

## Configuration

To change the host/port in which this agent listen, modify `config.yml` or
create the environment variables:

    ANALYSE_PAGE_HOST='127.0.0.1' # 127.0.0.1 is the default
    ANALYSE_PAGE_PORT='8002' # 8002 is the default


Other variable that can be changed in `config.py` or via environment variables:
 * `STORE_CONFIG_DB` name of the DB where the agents will find their
   configuration. Default is `config`
 * `STORE_CONFIG_DOC` name of the document where this agent will find its
   configuration. For this agent the default is `pages-juga`
 * `STORE_DB` name of the database for this agent. Default is `pages-juga`
 * `STORE_URL` URL of the sotre. Default is `
   `https://staging-store.openintegrity.org`

## Running

    analyse_url/analyse_pages_tos_service.py

or

    cd analyse_url
    analyse_pages_tos_service.py

or

    cd analayse_url
    nameko run analyse_url --config config.yaml # if runned in this way,
    won't take the ANALYSE* environment variables
