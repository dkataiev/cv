import base64
import json


from datetime import date
from mako.template import Template
from pdfkit import from_string

from json2md import generate_md

README_MD_FILE = 'README.md'
CV_JSON = 'src/data/cv.json'
CV_PDF = 'src/html/cv.pdf'

PHOTO_PATH = 'src/html/img/dkataiev.png'

HTML_TEMPLATE = 'src/html/template.html'


PDF_OPTIONS = {
    'page-size': 'Letter',
    'margin-top': '0.25in',
    'margin-right': '0.25in',
    'margin-bottom': '0.25in',
    'margin-left': '0.25in',
    'enable-local-file-access': None
}


def base64img(path):
    with open(path, 'rb') as image_file:
        return 'data:image/png;base64, {}'.format(base64.b64encode(image_file.read()).decode("UTF-8"))


def generate_markdown(cv_json):
    content = generate_md(cv_json)
    print('Writing to {}'.format(README_MD_FILE))
    f = open(README_MD_FILE, 'w')
    f.write(content)
    f.close()
    print('Done')


def generate_pdf(cv_json):
    cv_template = Template(filename=HTML_TEMPLATE)
    html_content = cv_template.render(
        cv=cv_json,
        photo_data=base64img(PHOTO_PATH)
    )
    from_string(html_content, CV_PDF, PDF_OPTIONS)


if __name__ == '__main__':
    with open(CV_JSON) as cv_json:
        data = json.load(cv_json)
        generate_markdown(data)
        generate_pdf(data)
