import yaml
import re
from jinja2 import FileSystemLoader, Environment
import os
import codecs
import markdown

import copy

from os.path import exists
import shutil

import time

CWD = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(CWD, 'output')


def date_format(value, format='%b %d, %Y'):
    return value.strftime(format)


class Engine(object):
    env = Environment(loader=FileSystemLoader('templates'))
    output_dir = OUTPUT_DIR

    def __init__(self):
        self.def_cntx = dict(SITE_ROOT=OUTPUT_DIR, now=time.strftime("%d/%m/%Y"))
        if exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

        self.env.filters['dateformat'] = date_format

    def render(self, temp, cntx):
        x = copy.copy(cntx)
        x.update(self.def_cntx)
        return temp.render(x)

    def render_and_write(self, template, cntx, path):
        with open(path, 'w') as f:
            f.write(self.render(template, cntx))

    def get_def_cntx(self):
        return copy.copy(self.def_cntx)

    def get_root_fn(self, fn):
        return os.path.join(self.output_dir, fn)

    def fn_sanitize(self, fn):
        s = re.sub('\s', '-', fn)
        return re.sub('[^0-9a-zA-Z-]', '', s)
