from google.appengine.ext import db


class Submission(db.Model):
    submitter = db.StringProperty(required=True)
    image = db.BlobProperty()

