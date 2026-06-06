from django.apps import AppConfig


class StackusersConfig(AppConfig):
    name = 'stackusers'

    def ready(self):
        print('StackusersConfig.ready() executed')
        import stackusers.signals