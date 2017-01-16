from django.core.management.base import BaseCommand
import json
from constance import config
import logging
from constance import settings

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = u'Dump settings from DB to a JSON file (usage ./manage.py dump_settings)'

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str)

    def handle(self, *args, **options):
        output_file = options['output_file']
        log.debug('Begin')
        log.debug('Output file is: %s' % output_file)

        data = {}

        for name, options in settings.CONFIG.items():
            data[name] = getattr(config, name)

        with open(output_file, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4))

        log.debug('Done')
