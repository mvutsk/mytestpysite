from flask import Blueprint, render_template, session, g, flash, request, redirect, \
    url_for, current_app, abort, send_file
from common.post_models import Post, BlogPost, Video, Image, Quote
from common.acc_models import User
from common.stat_model import LogStat
from posts.post_forms import PostForm, PostComment

import csv
from datetime import datetime

posts_prj = Blueprint('posts_prj', __name__)


@posts_prj.route('/')
def index():
    posts = Post.objects.all()
    return render_template('posts/index.html', posts=posts, slug=None)


@posts_prj.route('/about/')
def about():
    return render_template('posts/about.html')


@posts_prj.route('/addpost/', methods=['GET', 'POST'])
def addpost():
    next = request.values.get('next', '/')
    form = PostForm()
    form.next.data = next

    if form.validate_on_submit():
        user = User.objects.get(pk=session['user_id'])
        form.save(author=user)
        flash('Post added successfully.', 'success')
        return redirect(next)
    return render_template('posts/add_post_form.html', form=form)

def logstat(post, user, ip_addr):
    if user == 'anonym':
        viewer = 'anonym noid'
    else:
        viewer = user.username
    post_slug = post.slug
    logs = LogStat(viewer=viewer, post_slug=post_slug, remote_addr=ip_addr)
    logs.save()


@posts_prj.route('/postview/<slug>/', methods=['GET', 'POST'])
def postview(slug):
    post = Post.objects.get_or_404(slug=slug)
    user = None
    try:
        author = User.objects.get(pk=post.author.id)
    except:
        author = None

    post_author = None
    if not author:
        post_author = 'Author is not with us anymore.'

    if session.get('user_id', None):
        post.views_count += 1
        user = User.objects.get(pk=session.get('user_id', None))
        if not Post.objects(id=post.id, viewers__in=[user]):
            Post.objects(id=post.id).update_one(push__viewers=user)
        if post.slug not in user.viewed_posts:
            user.viewed_posts.append(post.slug)
            user.save()

        logstat(post=post, user=user, ip_addr=request.remote_addr)

        cform = PostComment()
        if cform.validate_on_submit():
            cform.save(post=post, author=user)
            return redirect("postview/" + post.slug)

    else:
        post.anon_views_count += 1
        cform = None
        logstat(post=post, user='anonym', ip_addr=request.remote_addr)

    post.save()
    return render_template('posts/view_detail.html', post=post, post_author=post_author,
                           commform=cform)


# /statistics/?reptype=csv|xml|json
@posts_prj.route('/statistics/', methods=['GET', 'POST'])
def statistics():
    # TODO: template for csv, xml, json
    if session.get('user_id', None):
        user = User.objects.get_or_404(pk=session.get('user_id', None))
        if user.is_superuser:
            reptype = request.args.get('reptype', None)
            if reptype == 'xml':
                pass
            elif reptype == 'json':
                pass
            else:  # all others are csv
                frepname = str(current_app.config.root_path) + "/reports/report_" + str(datetime.now().strftime("%Y-%m-%d-%I%M%S")) + ".csv"
                with open(frepname, 'w') as csvfile:
                    fieldnames = ['user_name', 'user_username', 'user_email', 'post_slug', 'date_view', 'from_ip']
                    writecsv = csv.DictWriter(csvfile, fieldnames)
                    writecsv.writeheader()
                    stats = LogStat.objects.all()
                    for stt in stats:
                        if stt.viewer == 'anonym noid':
                            ruser = {
                                'name': 'anonymous user',
                                'username': stt.viewer,
                                'email': 'anonymous user'
                            }
                        else:
                            try:
                                ruser = User.objects.get(username=stt.viewer)
                            except:
                                ruser = {
                                    'name': 'removed user',
                                    'username': stt.viewer,
                                    'email': 'removed user'
                                }

                        writecsv.writerow({'user_name': ruser['name'], 'user_username': ruser['username'],
                                           'user_email': ruser['email'], 'post_slug': stt.post_slug,
                                           'date_view': stt.view_time, 'from_ip': stt.remote_addr})

                return send_file(frepname)

        else:
            abort(404)
    else:
        abort(404)

@posts_prj.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist in this Universe', 404