from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import *
import json
import random

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    f = feed()
    _a = Article.query.all()
    random.shuffle(_a)
    a = []
    for article in _a:
        if len(a) < 5:
            a.append(article)
        else:
            pass

    return render_template("home.html", user=current_user, feed=f ,link_articles=a)


def parse_news(news):
    parsed = []
    index = 0
    for item in news:
        i = {
            'index': index,
            'link': item.link,
            'name': item.name,
            'image': item.image
        }
        index += 1
        parsed.append(i)
    return parsed


def feed():
    from main import tweets
    posts = []
    users_query = Post.query.all()
    for index, tweet in tweets.iterrows():
        if len(posts) < 30:
            tweet_json = {
                'id': tweet['Tweet_ID'],
                'author_username': tweet['Username'],
                'author_id': tweet['Tweet_ID'],
                'author_avatar': f'images/avatar/vibrent_{(len(posts) % 10) + 1}.png',
                'date': tweet['Timestamp'],
                'content': tweet['Text'],
                'likes': tweet['Likes'],
                'comments': tweet['Retweets']
            }
            posts.append(tweet_json)

    for post in users_query:
        if len(posts) < 10:
            user = User.query.all(post.author_id)
            post_json = {
                'id': post.id,
                'author_username': user.first_name,
                'author_id': post.author_id,
                'author_avatar': '',
                'date': post.date.strftime('%Y-%m-%d %H:%M:%S'),
                'content': post.content,
                'likes': len(post.likes),
                'comments': len(post.comments)
            }
            posts.append(post_json)
    else:
        pass
    
    random.shuffle(posts)
    return posts;