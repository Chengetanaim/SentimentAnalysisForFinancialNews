from django.db import models


class Sentiment(models.Model):
    sentiment = models.CharField(max_length=100)

    def __str__(self):
        return self.sentiment


class FinancialNews(models.Model):
    text = models.TextField()
    link = models.URLField()
    image = models.URLField()
    source = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Financial News'


class ClassifiedNews(models.Model):
    news = models.ForeignKey(FinancialNews, related_name='classify_news', on_delete=models.CASCADE)
    # sentiment_text = models.CharField(max_length=100)
    sentiment_text = models.ForeignKey(Sentiment, related_name='classify_sentiment', on_delete=models.CASCADE)
    sentiment_integer = models.IntegerField()
    accuracy_percentage = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news.text

    class Meta:
        verbose_name_plural = 'Classified News'


class NamedEntityRecognition(models.Model):
    news = models.ForeignKey(FinancialNews, related_name='named_entity_recognition', on_delete=models.CASCADE)
    entity = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    explanation = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news.text
