# fetch-url

Work in progress...

## Installation in Debian/Ubuntu

### System dependencies

    sudo apt-get install python-dev

### With virtualenv

#### Obtain virtualenv

Check https://virtualenv.pypa.io/en/latest/installation.html or if Debian equal/newer than jessie (virtualenv version equal or greater than 1.9)

    sudo apt-get install python-virtualenv

#### Create a virtualen

    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/oiienv
    source ~/.virtualenvs/oiienv/bin/activate

#### Install dependencies in virtualenv
    git clone https://lab.openintegrity.org/agents/analyse-url.git
    cd analyse-url
    pip install -r requirements.txt

## Configuration

TBD

## Running

    cd analyse-url/analyse_url
    nameko run analyse_url --config config.yaml
