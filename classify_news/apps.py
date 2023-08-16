from django.apps import AppConfig
import os


class ClassifyNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classify_news'

    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
        from . import updater
        updater.news_start()


