from django.shortcuts import render
from .models import ClassifiedNews, FinancialNews, NamedEntityRecognition, Sentiment
import pickle
import spacy
import math
from .ner import get_ner_df
# from .scraping import save_news
# Loading spacy
nlp = spacy.load("en_core_web_sm")

# Loading model for predicting financial news sentiment (from an investor point of view)
with open('model/financial_model.pkl', 'rb') as f:
    model = pickle.load(f)


# save_news()
def index(request):
    # Get all Financial News
    sentiments = Sentiment.objects.all()
    headlines = FinancialNews.objects.order_by('-date_added')
    for headline in headlines:
        # Get a specific Financial News headline
        financial_news = FinancialNews.objects.get(id=headline.id)
        # Predicting sentiment of the Financial News from an Investor point of view
        sentiment_integer = model.predict([f"{headline.text}"])
        proba = model.predict_proba([f"{headline.text}"])
        if sentiment_integer[0] == 0:
            sentiment_text = Sentiment.objects.get(sentiment='Negative')
        elif sentiment_integer[0] == 1:
            sentiment_text = Sentiment.objects.get(sentiment='Positive')
        elif sentiment_integer[0] == 2:
            sentiment_text = Sentiment.objects.get(sentiment='Neutral')
        else:
            sentiment_text = 'Error!'

        for prob in proba:
            accuracy_probability = math.floor(max(prob) * 100)

        # Saving classified financial news headlines into the database
        ClassifiedNews.objects.get_or_create(news=financial_news, sentiment_text=sentiment_text,
                                             sentiment_integer=sentiment_integer[0], accuracy_percentage=accuracy_probability)
        # Detecting entities from a specific financial news headline and saving it into the database
        doc = nlp(headline.text)
        for ent in doc.ents:
            NamedEntityRecognition.objects.get_or_create(news=financial_news, entity=ent.text, label=ent.label_,
                                                         explanation=spacy.explain(ent.label_))
    classified_news = ClassifiedNews.objects.order_by('-date_added')[3:]
    cn1 = ClassifiedNews.objects.order_by('-date_added')[0]
    cn2 = ClassifiedNews.objects.order_by('-date_added')[1]
    cn3 = ClassifiedNews.objects.order_by('-date_added')[2]
    named_entity_recognition = NamedEntityRecognition.objects.all()
    context = {'classified_news': classified_news, 'named_entity_recognition': named_entity_recognition,
               'sentiments': sentiments, 'cn1': cn1, 'cn2': cn2, 'cn3': cn3}
    return render(request, 'classify_news/index.html', context)


def sentiment(request, sentiment_id):
    sentiment = Sentiment.objects.get(id=sentiment_id)
    classified_news = sentiment.classify_sentiment.order_by('date_added')
    named_entity_recognition = NamedEntityRecognition.objects.all()
    context = {'sentiment': sentiment, 'classified_news': classified_news, 'named_entity_recognition': named_entity_recognition}
    return render(request, 'classify_news/sentiment.html', context)


def chart(request):
    df = get_ner_df()
    country_names = df.groupby('label').entity.value_counts()['GPE'].index.values[:10]
    country_values = df.groupby('label').entity.value_counts()['GPE'].values[:10]
    context = {'country_names': country_names, 'country_values': country_values}
    return render(request, 'classify_news/chart.html', context)


def  sentiment_visualization(request):
    positive = Sentiment.objects.get(sentiment='Positive')
    positive_news = positive.classify_sentiment.all()
    negative = Sentiment.objects.get(sentiment='Negative')
    negative_news = negative.classify_sentiment.all()
    neutral = Sentiment.objects.get(sentiment='Neutral')
    neutral_news = neutral.classify_sentiment.all()
    sentiment_names = ['Neutral', 'Positive', 'Negative']
    sentiment_values = [neutral_news.count(), positive_news.count(), negative_news.count()]
    context = {'sentiment_names': sentiment_names, 'sentiment_values': sentiment_values}
    return render(request, 'classify_news/sentiment_visualization.html', context)
