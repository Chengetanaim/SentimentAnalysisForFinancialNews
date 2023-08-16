from .models import Sentiment


def sentiments(request):
    sentiments = Sentiment.objects.all()
    return {'sentiments': sentiments}