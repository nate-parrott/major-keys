#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from PIL import Image, ImageDraw, ImageFont
import StringIO
import json
import os
import random
from sayings import sayings
import base64
import urllib

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('index.html').read())

class XHandler(webapp2.RequestHandler):
    def get(self, payload):
        data = open('x.html').read()
        image_url = '/image?payload=' + payload
        data = data.replace('IMAGE_URL', image_url)
        self.response.write(data)

def image_names():
    return [name for name in os.listdir('images/final') if name.split('.')[-1] in ['png', 'jpg', 'gif']]

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        payload = json.loads(base64.b64decode(self.request.get('payload')))
        text = payload[1]
        seed = payload[0]
        random.seed(seed)
        
        image_name = random.choice(image_names())
        template = random.choice(sayings)
        text = template.replace('***', text)
        
        image = Image.open('images/final/' + image_name)
        width, height = image.size
        data = json.load(open('images/final/' + image_name.split('.')[0] + '.json'))
        
        draw = ImageDraw.Draw(image)
        font_size = height * 0.03
        # print image_name
        # print 'y:', y, 'image_name split:', image_name.split('.')[1], 'height:', height,'text:', text_height
        font = ImageFont.truetype("Roboto-Regular.ttf", int(round(font_size)))
        text_w, text_h = font.getsize(text)
        y = data['y'] * height - text_h/2
        x = (width - text_w)/2
        draw.text((int(x), int(y)), text, font=font)
        
        output = StringIO.StringIO()
        image.save(output, format='JPEG')
        data = output.getvalue()
        
        self.response.write(data)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/image', ImageHandler),
    ('/_(.+)', XHandler),
], debug=True)
