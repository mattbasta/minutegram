#!/usr/bin/env python

import webapp2
from webapp2_extras import jinja2

SANDBOXED = True


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template, **context):
        rv = self.jinja2.render_template(template, **context)
        self.response.write(rv)


class HITHandler(BaseHandler):
    def get(self):
        url = ("https://%s.mturk.com/mturk/externalSubmit" %
                   "workersandbox" if SANDBOXED else "www")
        ctx = {"image_url": self.request.get("url"),
               "assignmentId": self.request.get("assignmentId"),
               "postback_url": url}
        self.render_template("hit_template.html", **ctx)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/hit', HITHandler),],
                              debug=True)
