from django.urls import path
from . import views

app_name = 'classify_news'

urlpatterns = [
    path('', views.index, name='index'),
    path('sentiment/<int:sentiment_id>/', views.sentiment, name='sentiment'),
    path('chart/', views.chart, name='chart'),
    path('sentiment_visualization/', views.sentiment_visualization, name='sentiment_visualization')
]