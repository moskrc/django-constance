from django.core.management.base import BaseCommand
import json
from constance import config
import logging

log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = u'Upload settings from JSON to django-constance (usage ./manage.py apply_settings)'

    def add_arguments(self, parser):
        parser.add_argument('settings_file', type=str)

    def handle(self, *args, **options):
        settings_file = options['settings_file']
        log.debug('Settings file: %s' % settings_file)

        log.debug('Begin')
        with open(settings_file) as f:
            settings = json.loads(f.read())
            for k,v in settings.items():
                log.debug('%s = %s' % (k,v))
                setattr(config, k, v)


        log.debug('Done')
