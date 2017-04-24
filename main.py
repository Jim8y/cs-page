# encoding: utf-8

import yaml
from jinja2 import FileSystemLoader, Environment
import os
import codecs
import markdown
from os.path import join, exists
from base import Engine

from optparse import OptionParser
import bibtexparser

parser = OptionParser()
parser.add_option("-d", "--deploy", action="store_true", dest="deploy", default=False)
parser.add_option("-f", "--fetchall", action="store_true", dest="fetchall", default=False)
(options, args) = parser.parse_args()

CWD = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(CWD, 'output')

e = Engine(deploy=options.deploy)

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *

def customizations(record):
    authors = record['author']
    count = authors.count('and') - 1
    authors = authors.replace(' and', ',', count)
    record['author'] = authors

    record['title'] = record['title'].replace('{','').replace('}','')
    return record

def index():
    temp = e.env.get_template('index.html')
    output_fn = e.get_root_fn('index.html')

    with open('content/publications.yaml', 'r') as c:
        pubs = yaml.load_all(c)
        pubs = list(pubs)

    with open('content/fan.bib') as bfile:
        bib = bfile.read()

    bibparser = BibTexParser()
    bibparser.customization = customizations
    bib = bibtexparser.loads(bib, parser=bibparser)

    updates = [
        dict(
            year=2017,
            month='Apr',
            header="Solidus Paper is Online",
            content="Solidus: Confidential Distributed Ledger Transactions via PVORM is now available on <a href=\"http://ia.cr/2017/317\">ePrint</a>.",
            ),
        dict(
            year=2016,
            month='Oct',
            header="Paper Accepted to EuroS&P '17",
            content="Sealed-Glass Proofs: Using Transparent Enclaves to Prove and Sell Knowledge is accepted to EuroS&P '17.",
            ),
        dict(
            year=2016,
            month='Jul',
            header="Paper Accepted to CCS'16",
            content="Town Crier: An Authenticated Data Feed for Smart Contracts is accepted to ACM CCS'16."
            ),
        dict(
            year=2016,
            month='Apr',
            header="Paper Accepted to Security'16",
            content="Stealing Machine Learning Models via Prediction APIs is accepted to USENIX Security'16.",
            )
        ]

    e.render_and_write(temp,
            dict(publications=bib.entries, updates=updates),
            output_fn)


def page_not_found():
    output = e.get_root_fn('404.html')
    temp = e.env.get_template('base.html')

    with open('./content/404.html', 'r') as c:
        content = c.read()

    e.render_and_write(temp, dict(
        title='Woops',
        content=content),
        output)


import os
import shutil
import errno
import sys

if __name__ == '__main__':
    index()
    page_not_found()

    try:
        shutil.copytree('static', join(OUTPUT_DIR, 'static'))
        shutil.copytree('files', join(OUTPUT_DIR, 'files'))
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
