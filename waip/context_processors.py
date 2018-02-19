from django.conf import settings  # import the settings file


def google_analytics_key(request):
    return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}
