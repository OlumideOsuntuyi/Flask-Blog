from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'flask_app_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Post, Note, Article, Comment, Like, Bookmark

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    #retrieve_articles(app)

    return app


def retrieve_articles(app):
    from .scrape import ScrapedArticle
    from .scrape import retrieve as rtv
    from .models import Article

    articles = rtv()
    articleIndex = 0
    print(f'Retrieved articles: {len(articles)}')
    
    for article in articles:
        a = ScrapedArticle(article.link)
        name = a.title()
        link = a.link
        content = " "
        author = a.author()
        image = a.image()


        with app.app_context():
            r = Article.query.filter_by(name=name).first()
            if r:
                pass
            else:
                new_article = Article(name=name, link=link, author=author, image=image, content=content)
                db.session.add(new_article)
                db.session.commit()
                articleIndex += 1
                print(f'stored in database count this instance: {articleIndex}')
    
    return len(articles)


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("created database")