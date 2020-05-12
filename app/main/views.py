import os
from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User, Blog, Comment, Subscriber
from .forms import UpdateProfile, CreateBlog
from .. import db, photos
from datetime import datetime
from ..email import mail_message
from app.request import get_quotes

#views
@main.route('/', methods = ['GET', 'POST'])
def index():
    '''
    View function that returns the index page and it's data
    '''
    # intro = "Welcome to My Developer Journey"
    # quotes = requests.get("http://quotes.stormconsultancy.co.uk/random.json").json()
    quotes = get_quotes()
    page = request.args.get('page',1,type =int)
    blogs = Blog.query.order_by(Blog.posted.desc()).paginate(page = page,per_page = 3)
    return render_template('index.html', blogs=blogs, quotes=quotes)

@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    # user_id = current_user._get_current_object().id
    # posts = Pitch.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
    # ,posts=posts

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))

@main.route('/new_post',methods=['GET','POST'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = CreateBlog()
    if form.validate_on_submit():
        title = form.title.data
        user_id = current_user._get_current_object().id
        content = form.content.data
        blog = Blog(title = title, content = content,user_id=user_id)
        blog.save_blog()
        for subscriber in subscribers:
            mail_message('New blog post','email/new_blog',subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
    return render_template('newblog.html',form = form)

@main.route('/blog/<id>')
def blog(id):
    comments = Comment.query.filter_by(blog_id = id).all()
    blog = Blog.query.get(id)
    # blog = Blog.query.get_or_404(id)
    return render_template('blog.html',blog = blog ,comment= comments)

@main.route('/blog/<blog_id>/update',methods=['GET','POST'])
@login_required
def updateblog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(404)
    form = CreateBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash('You have updated your Blog')
        return redirect(url_for('main.index',id=blog_id))
    if request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('newblog.html',form = form)

@main.route('/comment/<blog_id>',methods=['GET','POST'])
def comment(blog_id):
    blog = Blog.query.get(blog_id)
    comment = request.form.get('newcomment')
    new_comment = Comment(comment = comment, blog_id=blog_id)
    new_comment.save_comment()
    return redirect(url_for('main.blog',id= blog.id))

@main.route('/subscribe',methods=['POST'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber =  Subscriber(email= email)
    new_subscriber.save_subscriber()
    db.session.add(new_subscriber)
    db.session.commit()
    mail_message("Subscribed to Tech-Blog","email/welcome_sub",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def del_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete_blog()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_post(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.filter_by(user=user).order_by(Blog.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('userpost.html',blogs=blogs,user = user)