import os
import datetime

README_MD_FILE = 'README.md'

if __name__ == '__main__':
    content = '# Hello from Python!\n ## Time is {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('Writing to {}'.format(README_MD_FILE))
    f = open(README_MD_FILE, 'w')
    f.write(content)
    f.close()
    print('Done')