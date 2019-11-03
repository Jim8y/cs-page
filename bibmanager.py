"""
a lib handling bibliography
"""

from typing import List

from pybtex.database import parse_file
from pybtex.plugin import find_plugin
from pybtex.style.formatting import BaseStyle, toplevel
from pybtex.style.template import (
    field, join, optional, sentence, words, node, FieldIsMissing, tag, optional_field, href
)


@node
def format_names(children, context, role, **kwargs):
    """
    Returns formatted names as an APA compliant reference list citation.
    TODO: this function looks superfluous. But I don't know how to reduce it.
    """
    assert not children

    try:
        persons = context['entry'].persons[role]
    except KeyError:
        raise FieldIsMissing(role, context['entry'])

    style = context['style']

    formatted_names = [style.format_name(
        person, style.abbreviate_names) for person in persons]
    return join(sep=', ', sep2=', ', last_sep=', and ')[formatted_names].format_data(context)


class Minimalism(BaseStyle):
    # shorthand for the template sentence that extracts year
    date = words[field('year'), optional[", ", field('month')]]

    def __init__(self, abbreviate_names=False):
        super(Minimalism, self).__init__(abbreviate_names=abbreviate_names)

    def format_names(self, role, as_sentence=True):
        formatted_names = format_names(role)
        if as_sentence:
            return sentence(capfirst=False)[formatted_names]
        else:
            return formatted_names

    def format_title(self, e, which_field, as_sentence=True):
        formatted_title = href[
            field('url', raw=True),
            field(which_field),
        ]
        if as_sentence:
            return sentence[formatted_title]
        else:
            return formatted_title

    def format_btitle(self, e, which_field, as_sentence=True):
        formatted_title = tag('em')[field(which_field)]
        if as_sentence:
            return sentence["In", formatted_title, self.date]
        else:
            return words(sep=', ')[formatted_title, self.date]

    def format_authors(self, e):
        return self.format_names('author')

    def format_article(self, entry):
        template = toplevel[
            self.format_names('author'),
            self.format_title(entry, 'title'),
            sentence["In submission"]
        ]
        return template.format_data(entry)

    def get_inproceedings_template(self, e):
        # Required fields: author, title, booktitle, year
        # Optional fields: editor, pages, organization, publisher, address,
        #                  month, note, key
        return toplevel[
            self.format_authors(e),
            self.format_title(e, 'title'),
            sentence(sep=' ')[
                "In",
                self.format_btitle(e, 'booktitle', as_sentence=False),
            ],
            sentence[optional_field('note')],
        ]


class BiblioEntry:
    def __init__(self, formatted_string, media):
        self.formatted_string = formatted_string
        self.media = media


def parse_bib(filename, exclude_fields=None) -> List[BiblioEntry]:
    """

    :param filename:
    :param exclude_fields:
    :return: a list of BiblioEntry
    """
    STYLE = Minimalism(abbreviate_names=True)
    HTML = find_plugin('pybtex.backends', 'html')()

    bibliography = parse_file(filename)
    exclude_fields = exclude_fields or []

    if exclude_fields:
        for entry in bibliography.entries.values():
            for ef in exclude_fields:
                if ef in entry.fields.__dict__['_dict']:
                    del entry.fields.__dict__['_dict'][ef]

    formattedBib = STYLE.format_bibliography(bibliography)

    # crossref media coverage
    import yaml
    with open('content/media.yaml', 'r') as media_yaml:
        media = yaml.full_load(media_yaml)

    from collections import defaultdict
    media_indexed = defaultdict(list)
    for m in media:
        media_key = m['project'].lower()
        media_indexed[media_key].append({
            'venue': m['venue'],
            'url': m['url']
        })

    output = []
    for idx, entry in enumerate(bibliography.entries.values()):

        media = None
        if 'mediakey' in entry.fields:
            mk = entry.fields['mediakey']
            media = media_indexed[mk.lower()]

        formatted_string = formattedBib.entries[idx].text.render(HTML)
        output.append(BiblioEntry(formatted_string, media))

    return output
