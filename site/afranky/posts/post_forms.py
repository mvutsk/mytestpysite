from flask import render_template, current_app
from wtforms import *
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed, FileRequired
from common.post_models import Post, Comment, Video, Image, ImageURL
import re

class PostForm(FlaskForm):
    # post_type_class = None
    # posttype = None

    # def __init__(self, posttype='post'):
    #    self.post_type_class = posttype

    post_title = StringField(
        label='Title',
        validators=[
            validators.required(),
            validators.length(max=300)
        ]
    )
    # if post_type_class == 'post' or post_type_class is None:
    post_data = TextAreaField(
        label='Data',
        validators=[
            validators.required()
        ]
    )

    next = HiddenField()

    def validate_post_title(form, field):
        if Post.objects.filter(title=field.data):
            raise ValidationError('Post with such title already exists.')

    def validate_post_data(form, field):
        if field.data is None:
            raise ValidationError('Type something into your post.')

    def save(self, author):
        title = self.post_title.data
        data = self.post_data.data
        author = author
        post = Post(title=title, body=data, author=author)
        post.save()
        return post


class ImageForm(FlaskForm):

    post_title = StringField(
        label='Title',
        validators=[
            validators.required(),
            validators.length(max=300)
        ]
    )

    post_data = TextAreaField(
        label='Description',
        validators=[
            validators.required()
        ]
    )

    images = UploadSet('images', IMAGES)
    image = FileField(
        label='Image File',
        validators=[
            FileRequired(),
            FileAllowed(images, 'Images only!')
            # validators.required(),
            # validators.regexp('^[^/\\]\.jpg$')
            # validators.regexp('^(.*)\.jpg$')
        ]
    )

    next = HiddenField()

    def validate_post_title(form, field):
        if Post.objects.filter(title=field.data):
            raise ValidationError('Post with such title already exists.')

    def validate_post_data(form, field):
        if field.data is None:
            raise ValidationError('Please add a description for the picture.')

    def save(self, author, image_file, img_fname):
        title = self.post_title.data
        data = self.post_data.data
        author = author
        # image_data = request.FILES[self.image.name].read()
        post = Image(title=title, body=data, author=author, image_file_name=img_fname)
        post.image.put(image_file, content_type='image/jpeg')
        post.save()
        return post


class ImageURLForm(FlaskForm):

    post_title = StringField(
        label='Title',
        validators=[
            validators.required(),
            validators.length(max=300)
        ]
    )

    post_data = TextAreaField(
        label='Description',
        validators=[
            validators.required()
        ]
    )

    post_image_url = StringField(
        label='Image URL',
        validators=[
            validators.required()
        ]
    )

    next = HiddenField()

    def validate_post_title(form, field):
        if Post.objects.filter(title=field.data):
            raise ValidationError('Post with such title already exists.')

    def validate_post_data(form, field):
        if field.data is None:
            raise ValidationError('Please add a description for the picture.')

    def validate_post_image_url(form, field):
        if field.data is None:
            raise ValidationError('Provide an URL of picture.')

    def save(self, author):
        title = self.post_title.data
        data = self.post_data.data
        imageurl = self.post_image_url.data
        author = author
        post = ImageURL(title=title, body=data, author=author, image_url=imageurl)
        post.save()
        return post


class VideoForm(FlaskForm):

    post_title = StringField(
        label='Title',
        validators=[
            validators.required(),
            validators.length(max=300)
        ]
    )

    post_data = TextAreaField(
        label='Description',
        validators=[
            validators.required()
        ]
    )

    post_video_url = StringField(
        label='Video URL',
        validators=[
            validators.required()
        ]
    )

    next = HiddenField()

    def validate_post_title(form, field):
        if Post.objects.filter(title=field.data):
            raise ValidationError('Post with such title already exists.')

    def validate_post_data(form, field):
        if field.data is None:
            raise ValidationError('Please add a description for the picture.')

    def validate_post_video_url(form, field):
        if field.data is None:
            raise ValidationError('Provide an URL of video.')

    def save(self, author):
        title = self.post_title.data
        data = self.post_data.data
        embed_code = self.post_video_url.data
        author = author
        post = Video(title=title, body=data, author=author, embed_code=embed_code)
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
        if field.data is None:
            raise ValidationError('Empty comments are not allowed.')

    def save(self, post, author):
        body = self.comment_data.data
        author = author
        post.comments.append(Comment(body=body, author=author))
        post.save()
