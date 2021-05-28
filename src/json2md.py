import datetime
import json

README_MD_FILE = 'README.md'
CV_JSON = 'src/cv.json'

BLOCK_SEPARATOR = '\n\n___\n\n'
PARAGRAPH_SEPARATOR = '\n'


def h2(text):
    return '## {}'.format(text)


def h3(text):
    return '### {}'.format(text)


def strong(text):
    return '__{}__'.format(text)


def li(text):
    return '* {}'.format(text)


def ul(title, items):
    list = [li(i) for i in items]
    list[0:0] = [h3(title)]
    return PARAGRAPH_SEPARATOR.join(list)

def link(title, body):
    return '[{}]({})'.format(title, body)

def contact_text(contact):
    contact_type = strong(contact['type'])
    contact_link = link(contact['title'], contact['link'])
    return ' '.join([contact_type, contact_link])

def head_block(cv):
    return PARAGRAPH_SEPARATOR.join([
        h2(cv['name']),
        h3(cv['title']),
    ])


def contacts_block(contacts):
    return ul('Contacts', [contact_text(c) for c in contacts])


def generate_md(cv):
    return BLOCK_SEPARATOR.join([
        head_block(cv),
        contacts_block(cv['contacts'])
    ])


if __name__ == '__main__':
    with open(CV_JSON) as cv_json:
        content = generate_md(json.load(cv_json))
        print('Writing to {}'.format(README_MD_FILE))
        f = open(README_MD_FILE, 'w')
        f.write(content)
        f.close()
        print('Done')
