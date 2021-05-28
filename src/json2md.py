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


def head_block(cv):
    return PARAGRAPH_SEPARATOR.join([
        h2(cv['name']),
        h3(cv['title']),
    ])


def generate_md(cv):
    return BLOCK_SEPARATOR.join([
        head_block(cv)
    ])


if __name__ == '__main__':
    with open(CV_JSON) as cv_json:
        content = generate_md(json.load(cv_json))
        print('Writing to {}'.format(README_MD_FILE))
        f = open(README_MD_FILE, 'w')
        f.write(content)
        f.close()
        print('Done')
