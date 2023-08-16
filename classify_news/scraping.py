from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from .models import FinancialNews

my_url = 'https://www.ft.com/markets'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

# print(page_soup)
news_headline = []
images2 = []
news_sources = []
news_headline_link = []
containers = page_soup.findAll("li", {"class": "o-teaser-collection__item o-grid-row"})
for container in containers:
    # print(container.div.div)
    articles = container.findAll("div", {"data-o-grid-colspan": "12 L9"})
    for article in articles:
        images = article.div.div.findAll("div", {"class": "o-teaser__image-container js-teaser-image-container"})
        for image in images:
            images2.append(image.a.div.img["data-src"])
            # print(image.a.div.img["data-src"])
        contents = article.div.div.findAll("div", {"class": "o-teaser__content"})
        for content in contents:
            sources = article.div.div.findAll("div", {"class": "o-teaser__meta"})
            for source in sources:
                try:
                    news_sources.append(source.a.text)
                except AttributeError:
                    news_sources.append("None")
            headlines = content.findAll("div", {"class": "o-teaser__heading"})
            for headline in headlines:
                link = "https://www.ft.com/" + headline.a["href"]
                news_headline_link.append(link)
                news_headline.append(headline.a.text)


# for link, news in zip(news_headline_link, news_headline):
#     print(link)
#     print(news)
# obj = {
#     'headlines': news_headline,
#     'headlines_links': news_headline_link,
#     'sources': news_sources,
#     'images': images2
# }
# print(obj)
def save_news():
    for text, link, image, source in zip(news_headline, news_headline_link, images2, news_sources):
        FinancialNews.objects.get_or_create(text=text, link=link, image=image, source=source)