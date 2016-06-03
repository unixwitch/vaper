# vim:set sw=4 ts=4 et:

from fabric.api import *

env.roledefs = {
    'production': [ 'vaper@willow.uk.le-fay.org' ],
}

@roles('production')
def deploy():
    with cd('/var/uwsgi/vaper/app'):
        run('git pull')
        run('/var/uwsgi/vaper/venv/bin/pip install -r requirements.txt')
        run('/var/uwsgi/vaper/venv/bin/python ./manage.py migrate --settings=vaper.settings.production')
        run('/var/uwsgi/vaper/venv/bin/python ./manage.py collectstatic --noinput --settings=vaper.settings.production')
        run('touch -h /usr/local/etc/uwsgi/conf.d/vaper.ini')
