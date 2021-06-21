import json

from datetime import date
from pdfkit import from_file


CV_HTML = 'src/html/cv.html'
CV_PDF = 'src/html/cv.pdf'

OPTIONS = {
    'page-size': 'Letter',
    'margin-top': '0.25in',
    'margin-right': '0.25in',
    'margin-bottom': '0.25in',
    'margin-left': '0.25in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ]
}


if __name__ == '__main__':
    from_file(CV_HTML, CV_PDF, OPTIONS)
