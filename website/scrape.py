import os.path
import re

from bs4 import BeautifulSoup
import requests

illegal_chars_pattern = r'[<>:"/\\|?*]'
class ScrapedArticle:
    def __init__(self, weblink):
        self.link = weblink
        self.webpage = BeautifulSoup(requests.get(self.link).text, 'html.parser')

    def title(self):
        t = self.webpage.findAll("h1", attrs={"class":"post-title"})[0].text.strip()
        if len(t) < 2:
            t = self.link

        t = re.sub(illegal_chars_pattern, '_', t)
        return t
    
    def image(self):
        image_wrapper = self.webpage.find("div", attrs={"class":"post-image-wrapper"})
        if image_wrapper:
            img = image_wrapper.find('img')
            if img:
                return img.get('src')
            else:
                pass
        else:
            pass

        return ''
    
    def author(self):
        author_div = self.webpage.find("div", attrs={"class":"post-author"})
        if author_div:
            a = author_div.find('a')
            if a:
                return a.text
            else:
                pass
        else:
            pass

        return ''


    def content(self):
        post_content = self.webpage.find_all('div', class_='post-content')[0]
        paragraphs = post_content.find_all("p")
        all_paragraphs = ""
        return paragraphs[1].get_text()

        # for some reason punch p tags are messed up when parsing
        for paragraph in paragraphs:
            txt = paragraph.get_text();
            r = txt.replace("READ_MORE", "")
            s = r.strip()
            all_paragraphs += s + '\n'

        return all_paragraphs

    def print(self, directory):
        with open(os.path.join(directory, f'{self.title()}.txt'), 'w', encoding='utf-8') as file:
            file.write(self.content())


class ScrapedArticleLink:
    def __init__(self, article):
        a = article.findAll('a')[0]
        imgs = article.findAll('img')

        self.link = a.get('href')
        self.linkTag = a.text
        self.linkImg = ""
        if len(imgs) > 0:
            img = imgs[0]
            self.linkImg = img.get('src')
        else:
            pass

    def hasImage(self):
        return len(self.linkImg) > 0
    
    def hasTag(self):
        return len(self.linkTag) > 0
        

def retrieve():
    homeLink = "https://punchng.com/"
    homepageHTML = requests.get(homeLink);
    homepage = BeautifulSoup(homepageHTML.text, 'html.parser')

    articles = homepage.find_all('article')
    articleLinks = []

    for article in articles:
        a_link = ScrapedArticleLink(article)
        articleLinks.append(a_link)
    
    return articleLinks