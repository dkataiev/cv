import json

from datetime import date
from os import name
from mako.template import Template

CV_JSON = 'src/data/cv.json'

CV_HTML = 'src/html/cv.html'
HTML_TEMPLATE = 'src/html/template.html'

if __name__ == '__main__':
    with open(CV_JSON) as cv_json:
        cv_template = Template(filename=HTML_TEMPLATE)
        cv_data = json.load(cv_json)
        content = cv_template.render(cv=cv_data)
        print('Writing to {}'.format(CV_HTML))
        f = open(CV_HTML, 'w')
        f.write(content)
        f.close()
        print('Done')
