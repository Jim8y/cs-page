"""
Generate this website.

Usage:
  main.py [options]

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  -m                        Keep running to monitor changes.
  -o                        Open the output in a webbrowser.
"""

import datetime
import errno
import logging
import os
import shutil
from operator import itemgetter
from os.path import join

import bibtexparser
import markdown
import yaml
from dateutil import parser as dtparser
from pyquery import PyQuery as pq

from base import Engine
import bibmanager


def index(engine: Engine) -> None:
    with open('content/bio.md') as bio_md:
        bio = markdown.markdown(bio_md.read())

    parsed_bib = bibmanager.parse_bib('content/Zhang_0022:Fan.bib')

    # generate update panel
    with open('content/updates.yaml', 'r') as updates_yaml:
        def parse_md_and_strip(md):
            if not md:
                return None
            # parse markdown and rip off the outer <p>
            text = markdown.markdown(md)
            return pq(text)('p').html()


        try:
            updates = yaml.full_load(updates_yaml)
            for u in updates:
                if not isinstance(u['date'], datetime.date):
                    u['date'] = dtparser.parse(u.get('date')).date()
                u['date_str'] = u['date'].strftime('%b. %Y')

                u['content'] = parse_md_and_strip(u['content'])
        except yaml.YAMLError as exc:
            print(exc)
            raise

    # sort updates by date
    updates = sorted(updates, key=itemgetter('date'), reverse=True)

    # ignore old stuff before 2018
    updates = list(filter(lambda u: u['date'].year >= 2018, updates))

    # invited talks
    with open('content/talks.md') as talks_md:
        talks = markdown.markdown(talks_md.read())

    # media coverage
    with open('content/media.yaml', 'r') as media_yaml:
        media = yaml.full_load(media_yaml)

    current_time = datetime.date.today()
    upcoming_news = [n for n in updates if n['date'] >= current_time]
    past_news = [n for n in updates if n['date'] < current_time]

    engine.render_with_context('index.html', 'index.html', dict(publication=parsed_bib,
                                                                upcoming_news=upcoming_news,
                                                                past_news=past_news,
                                                                bio=bio,
                                                                talks=talks,
                                                                media=media,
                                                                ))


def page_not_found(engine: Engine) -> None:
    with open('./content/404.html', 'r') as c:
        content = c.read()

    engine.render_with_context('base.html', '404.html', dict(
        title='Woops',
        content=content))


def static(engine: Engine) -> None:
    try:
        shutil.copytree('static', join(engine.output_dir, 'static'))
        shutil.copytree('files', join(engine.output_dir, 'files'))
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise


if __name__ == '__main__':
    from docopt import docopt

    args = docopt(__doc__)

    CWD = os.path.dirname(os.path.realpath(__file__))
    OUTPUT_DIR = os.path.join(CWD, 'output')
    CONTENT_DIR = os.path.join(CWD, 'content')

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    engine = Engine(output_dir=OUTPUT_DIR, content_dir=CONTENT_DIR)

    engine.register(index)
    engine.register(page_not_found)
    engine.register(static)

    if args['-m']:
        engine.watch(open_output=args['-o'])
    else:
        engine.build(open_output=args['-o'])
