from django.contrib import admin
from .models import FinancialNews, ClassifiedNews, NamedEntityRecognition, Sentiment


admin.site.register(FinancialNews)
admin.site.register(ClassifiedNews)
admin.site.register(NamedEntityRecognition)
admin.site.register(Sentiment)