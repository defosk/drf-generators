
from django.core.management.base import AppCommand, CommandError
from drf_generators.generators import *
from optparse import make_option
import django


class Command(AppCommand):
    help = 'Generates DRF API Views and Serializers for a Django app'

    args = "[appname ...]"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '-f', '--format', dest='format', default='viewset',
            help='view format (default: viewset)'
        )
        parser.add_argument('-d', '--depth', dest='depth', default=0,
                    help='serialization depth'),

        parser.add_argument('--force', dest='force', action='store_true',
                    help='force overwrite files'),

        parser.add_argument('--serializers', dest='serializers', action='store_true',
                    help='generate serializers only'),

        parser.add_argument('--views', dest='views', action='store_true',
                    help='generate views only'),

        parser.add_argument('--urls', dest='urls', action='store_true',
                    help='generate urls only'),


    def handle_app_config(self, app_config, **options):
        if app_config.models_module is None:
            raise CommandError('You must provide an app to generate an API')

        force = options['force']
        format = options['format']
        depth = options['depth']
        serializers = options['serializers']
        views = options['views']
        urls = options['urls']

        if format == 'viewset':
            generator = ViewSetGenerator(app_config, force)
        elif format == 'apiview':
            generator = APIViewGenerator(app_config, force)
        elif format == 'function':
            generator = FunctionViewGenerator(app_config, force)
        elif format == 'modelviewset':
            generator = ModelViewSetGenerator(app_config, force)
        else:
            message = '\'%s\' is not a valid format. ' % options['format']
            message += '(viewset, modelviewset, apiview, function)'
            raise CommandError(message)

        if serializers:
            result = generator.generate_serializers(depth)
        elif views:
            result = generator.generate_views()
        elif urls:
            result = generator.generate_urls()
        else:
            result = generator.generate_serializers(depth) + '\n'
            result += generator.generate_views() + '\n'
            result += generator.generate_urls()

        print(result)
