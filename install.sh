sudo apt-get install python3 python3-pip qt5-default libqt5webkit5-dev\
     build-essential xvfb libxml2-dev libxslt1-dev
python3 -m venv ../price_checker
source bin/activate
pip install -r requirements.txt
