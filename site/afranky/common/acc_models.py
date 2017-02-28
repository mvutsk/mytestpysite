from aprj import dbm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class BaseDocument(dbm.DynamicDocument):
    created_at = dbm.DateTimeField(verbose_name='Created at', required=True)
    updated_at = dbm.DateTimeField(verbose_name='Updated at', required=True)

    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(BaseDocument, self).save(*args, **kwargs)


class friend_list():
    username = ""
    name = ""
    status = ""
    added_at = ""


class Friend(dbm.EmbeddedDocument):
    added_at = dbm.DateTimeField(default=datetime.now(), required=True)
    friend_user_id = dbm.ObjectIdField(unique=False, required=True)
    status = dbm.StringField(verbose_name="status", max_length=30, required=True)


class User(BaseDocument):
    username = dbm.StringField(verbose_name='login', max_length=30, required=True, unique=True)
    name = dbm.StringField(verbose_name='name', max_length=100, required=True)
    email = dbm.EmailField(verbose_name='e-mail', max_length=100, required=True, unique=True)
    pw_hash = dbm.StringField(verbose_name='pwhash', max_length=100, required=True)
    is_active = dbm.BooleanField(verbose_name='is active', default=True, required=True)
    is_superuser = dbm.BooleanField(verbose_name='is admin', default=False, required=True)
    last_login = dbm.DateTimeField(verbose_name='last login date', default=datetime.now(), required=False)
    friends = dbm.ListField(dbm.EmbeddedDocumentField(Friend))
    viewed_posts = dbm.ListField(field=dbm.StringField(required=False), required=False)
    visit_count = dbm.IntField(min_value=0, default=0, required=True)

    meta = {
        'indexes': ['username', 'email']
    }

    # def __unicode__(self):
    #    return self.username

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password', None)
        super(User, self).__init__(*args, **kwargs)
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(
            password, method=current_app.config['PROJECT_PASSWORD_HASH_METHOD']
        )

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def refresh_last_login(self):
        self.last_login = datetime.now()
        self.visit_count += 1
        self.save()
