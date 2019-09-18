import copy
import os
import re
import shutil
import time
from os.path import exists, join, splitext
from typing import Dict

import logging
from jinja2 import FileSystemLoader, Environment, Template
import frontmatter
import markdown
from pyquery import PyQuery as pq
import docutils.core

from typing import Callable
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer


# Jinja filters
def date_format(value, format='%b %d, %Y'):
    return value.strftime(format)


class WatchBuilder(RegexMatchingEventHandler):
    def __init__(self, builder, *args, **kwargs):
        super().__init__(args, kwargs)
        self.builder = builder

    def on_any_event(self, event):
        logging.info(event)
        self.builder()


class Engine(object):
    env = Environment(loader=FileSystemLoader('templates'))

    def __init__(self, output_dir, content_dir):
        self.output_dir = output_dir
        self.content_dir = content_dir

        self.def_cntx = dict(SITE_ROOT=self.output_dir,
                             now=time.strftime("%x"))
        if exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.mkdir(self.output_dir)

        self.env.filters['dateformat'] = date_format

        # array to hold build task
        self.build_task = []

    def _render_and_write(self, template: Template, context: Dict, output_fullpath):
        with open(output_fullpath, 'w') as f:
            # merge context with the default context
            dft_context = self.get_copy_of_default_context()
            dft_context.update(context)
            f.write(template.render(dft_context))

    def _get_root_fn(self, fn):
        return os.path.join(self.output_dir, fn)

    def get_copy_of_default_context(self):
        return copy.copy(self.def_cntx)

    def render_with_context(self, template_filename, output_filename, context: Dict):
        if not isinstance(context, Dict):
            raise Exception('invalid context. Must be a dictionary')

        temp = self.env.get_template(template_filename)
        output_fn = self._get_root_fn(output_filename)

        self._render_and_write(temp, context, output_fn)

    def render_without_context(self, template_filename, output_filename=None):
        temp = self.env.get_template(template_filename)
        output_fn = self._get_root_fn(
            template_filename if output_filename is None else output_filename)

        self._render_and_write(temp,
                               dict(),
                               output_fn)

    def render_markdown(self, md_filename, output_filename=None, template='article.html'):
        post = frontmatter.load(join(self.content_dir, md_filename))
        meta = post.metadata
        content = markdown.markdown(post.content)

        article = dict(body=content)
        article.update(meta)

        if output_filename is None:
            output_filename = '{}.html'.format(splitext(md_filename)[0])

        self.render_with_context(template, output_filename, dict(article=article))

    def register(self, task: Callable[['Engine'], None]):
        self.build_task.append(task)

    def open_output(self):
        import webbrowser
        logging.info('opening')
        webbrowser.open(os.path.join(self.output_dir, 'index.html'))

    def build(self, open_output=False):
        logging.info('starting building')

        for task in self.build_task:
            task(self)

        logging.info('done building')
        if open_output:
            self.open_output()

    def watch(self, open_output=False):
        self.build(open_output)

        logging.info('monitoring changes in {}'.format(self.content_dir))
        handler = WatchBuilder(self.build, ignore_regexes=[r".*/output/.*"])
        observer = Observer()
        observer.schedule(handler, self.content_dir, recursive=True)

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()