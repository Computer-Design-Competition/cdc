import sys
import site

site.addsitedir('/var/www/covid_server/covid/lib/python3.7/site-packages')

sys.path.insert(0, '/var/www/covid_server/covid')

from server import app as application