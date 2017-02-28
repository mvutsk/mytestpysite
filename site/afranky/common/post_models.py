from aprj import dbm
from datetime import datetime
from flask import url_for, current_app, session
from common.acc_models import User, BaseDocument
from slugify import slugify


class Comment(dbm.EmbeddedDocument):
    created_at = dbm.DateTimeField(default=datetime.now(), required=True)
    body = dbm.StringField(verbose_name="Comment", required=True)
    author = dbm.ReferenceField(User, required=True)


class Post(BaseDocument):
    created_at = dbm.DateTimeField(default=datetime.now(), required=True)
    title = dbm.StringField(verbose_name="Title", max_length=255, required=True)
    author = dbm.ReferenceField(User, required=True)
    body = dbm.StringField(verbose_name="Data", required=True)
    slug = dbm.StringField(max_length=255, required=True)
    comments = dbm.ListField(dbm.EmbeddedDocumentField('Comment'))
    views_count = dbm.IntField(min_value=0, default=0, required=True)
    anon_views_count = dbm.IntField(min_value=0, default=0, required=True)
    viewers = dbm.ListField(dbm.ReferenceField(User), default=None, unique=False, required=False)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }


class BlogPost(Post):
    body = dbm.StringField(verbose_name="Text", required=True)


class Video(Post):
    embed_code = dbm.StringField(verbose_name="Code for blog", required=True)


class Image(Post):
    image_url = dbm.StringField(verbose_name="URL of picture", required=True, max_length=255)


class Quote(Post):
    body = dbm.StringField(verbose_name="Quote", required=True)
    author = dbm.StringField(verbose_name="Author", required=True, max_length=255)
