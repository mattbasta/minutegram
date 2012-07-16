#!/usr/bin/env python

import base64
import webapp2
from webapp2_extras import jinja2

from google.appengine.api import images
from google.appengine.ext import db

from models.submission import Submission

SANDBOXED = True


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template, **context):
        rv = self.jinja2.render_template(template, **context)
        self.response.write(rv)


class MainHandler(BaseHandler):
    def get(self):
        ctx = {}
        self.render_template("homepage.html", **ctx)


class PostHandler(BaseHandler):
    def post(self):
        data = self.request.get("url")
        if not data.startswith("data:"):
            self.error(400)
            return
        data = data[5:]
        try:
            metadata, body = data.split(",")
            if not metadata.startswith("image/png"):
                raise ValueError("Image of wrong MIME type.")

            imagedata = base64.standard_b64decode(body)
            if len(imagedata) > 500000:
                raise ValueError("Image too big.")

            image = images.Image(imagedata)
            image.resize(300, 300 / image.width * 300)

            sub = Submission(submitter=str(self.request.remote_addr) or "")
            sub.image = db.Blob(image.execute_transforms())
            sub.put()

        except ValueError:
            self.error(400)
            return

        self.response.write("{error:false}")


class HITHandler(BaseHandler):
    def get(self):
        url = ("https://%s.mturk.com/mturk/externalSubmit" %
                   "workersandbox" if SANDBOXED else "www")
        ctx = {"image_url": self.request.get("url"),
               "assignmentId": self.request.get("assignmentId"),
               "postback_url": url}
        self.render_template("hit_template.html", **ctx)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/post_pic', PostHandler),
                               ('/hit', HITHandler),],
                              debug=True)
