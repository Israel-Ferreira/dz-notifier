import requests
from xml.etree import ElementTree

from pynotifier import Notification, NotificationClient
from pynotifier.backends import platform


def send_notification(articles: list) -> None:
    c = NotificationClient()
    c.register_backend(platform.Backend())

    for artcl in articles:
        notification = Notification(title=artcl["title"], message=artcl["description"])
        c.notify_all(notification)


if __name__ == "__main__":
    url = "https://feeds.dzone.com/home"  # Feed do Dzone.com

    print("Obtendo os artigos mais recentes do Dzone.com")

    dzone_articles = requests.get(url, timeout=5)

    parsed_content = ElementTree.fromstring(dzone_articles.content).iter("item")

    articles = []

    for elem in parsed_content:
        article_title = elem.find("title").text
        article_link = elem.find("link").text
        description = elem.find("description").text

        article = {
            "title": article_title,
            "link": article_link,
            "description": description
        }

        articles.append(article)

    send_notification(articles)
