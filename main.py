from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fozil.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<title %r>' % self.title


@app.route('/')
def hello():
    articles = Article.query.all()
    return render_template('kot.html', articles=articles)


@app.route('/about')
def about():
    return render_template('kot.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route("/post/<int:id>")
def post_deteil(id):
    article =Article.query.get_or_404(id)
    return render_template("post_deteil.html", article=article)

@app.route("/posts/<int:id>/del")
def del_post(id):
    article = Article.query.get_or_404(id)
    return render_template("del_post.html", article=article)


@app.route("/posts/<int:id>/confirm-del", methods=["POST"])
def confirm_del(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect("/")

@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def post_update(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        db.session.commit()
        return redirect("/")
    return render_template("post_update.html", article=article)




@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/")
        except:
            return "Ошибка при добавлении статьи"
    else:
        return render_template("create-article.html")


with app.app_context():
    db.create_all()
    print("Таблица создана!")

if __name__ == "__main__":
    app.run(debug=True)
