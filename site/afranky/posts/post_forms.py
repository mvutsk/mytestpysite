from flask import render_template, current_app
from wtforms import *
from flask_wtf import FlaskForm
from common.post_models import Post, Comment, BlogPost, Video, Image, Quote


class PostForm(FlaskForm):
    post_type_class = None

    # def __init__(self, posttype='post'):
    #    self.post_type_class = posttype

    post_title = StringField(
        label='Title',
        validators=[
            validators.required(),
            validators.length(max=300)
        ]
    )
    if post_type_class == 'post' or post_type_class is None:
        post_data = TextAreaField(
            label='Data',
            validators=[
                validators.required()
            ]
        )

    next = HiddenField()

    def validate_post_title(form, field):
        post_title = field.data
        if Post.objects.filter(title=post_title):
            raise ValidationError('Post with such title already exists.')

    def validate_post_data(form, field):
        post_data = field.data
        if post_data is None:
            raise ValidationError('Type something into your post.')

    def save(self, author):
        title = self.post_title.data
        data = self.post_data.data
        author = author

        post = Post(title=title, body=data, author=author)
        post.save()
        return post


class PostComment(FlaskForm):

    comment_data = TextAreaField(
            label='Comment',
            validators=[
                validators.length(max=300)
            ]
        )

    next = HiddenField()

    def validate_comment_data(self, field):
        comment_data = field.data
        if comment_data is None:
            raise ValidationError('Empty comments are not allowed.')

    def save(self, post, author):
        body = self.comment_data.data
        author = author
        post.comments.append(Comment(body=body, author=author))
        post.save()
