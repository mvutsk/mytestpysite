from aprj import dbm
from datetime import datetime


class LogStat(dbm.DynamicDocument):
    viewer = dbm.StringField(max_length=30, required=True)
    post_slug = dbm.StringField(max_length=255, required=True)
    view_time = dbm.DateTimeField(default=datetime.now(), required=True)
    remote_addr = dbm.StringField(max_length=255, required=True)

    meta = {
        'indexes': ['-view_time', 'post_slug', 'viewer'],
        'ordering': ['-view_time']
    }
