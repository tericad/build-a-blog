from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date


@app.route('/blog', methods=['GET'])
def index():
    if request.args.get('id')==None:
        blogs = Blog.query.order_by(desc(pub_date)).all()
        return render_template('blog.html',title="My Blog", blogs = blogs)
    else:
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        return render_template('entry.html', blog=blog)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title= request.form['title']
        blog_body = request.form['blog']

        title_error=''
        body_error=''

        if len(blog_title) == 0:
            blog_title=''
            title_error='Blogs must have at least a 1 charachter in the title.'
        if len(blog_body) == 0:
            blog_body=''
            body_error='Blogs must have at least 1 charachter in the body.'
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body, pub_date)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id=' + str(new_blog.id))
        else:
            return render_template('newpost.html', blog_title=blog_title, title_error=title_error,
        blog_body=blog_body, body_error=body_error)
    else:
        return render_template('newpost.html')

@app.route('/entry', methods=['GET'])
def entries():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    return render_template('entry.html', blog=blog)


if __name__ == '__main__':
    app.run()