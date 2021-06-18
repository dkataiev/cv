import json
import os

from datetime import date

README_MD_FILE = 'README.md'
CV_JSON = 'src/cv.json'

BLOCK_SEPARATOR = '\n\n___\n\n'
PARAGRAPH_SEPARATOR = '\n'

HR = '---'


def h2(text):
    return '## {}'.format(text)


def h3(text):
    return '### {}'.format(text)


def h4(text):
    return '#### {}'.format(text)


def h6(text):
    return '###### {}'.format(text)


def strong(text):
    return '__{}__'.format(text)


def italic(text):
    return '*{}*'.format(text)


def li(text):
    return '* {}'.format(text)


def ul(items):
    list = [li(i) for i in items]
    return PARAGRAPH_SEPARATOR.join(list)


def titled_ul(title, items):
    list = [li(i) for i in items]
    list[0:0] = [h3(title)]
    return PARAGRAPH_SEPARATOR.join(list)


def sub_ul(title, items):
    list = ['\t{}'.format(li(i)) for i in items]
    list[0:0] = [li(strong(title))]
    return PARAGRAPH_SEPARATOR.join(list)


def link(title, body):
    return '[{}]({})'.format(title, body)


def meta():
    repo = os.getenv('GITHUB_REPOSITORY')
    server = os.getenv('GITHUB_SERVER_URL')
    sha = os.getenv('GITHUB_SHA')
    commit_url = '{}/{}/commit/{}'.format(server, repo, sha)

    return h6('Updated on {} [{}]'.format(date.today(), link(sha[:7], commit_url)))


def contact_text(contact):
    contact_type = strong('{}:'.format(contact['type']))
    contact_link = link(contact['title'], contact['link'])
    return ' '.join([contact_type, contact_link])


def head_block(name, title):
    return PARAGRAPH_SEPARATOR.join([
        h2(name),
        h3(title)
    ])


def contacts_block(data):
    return titled_ul('Contacts:', [contact_text(c) for c in data])


def career_summary_block(data):
    return PARAGRAPH_SEPARATOR.join([h3('Career Summary:'), data])


def titled_item(title, text):
    return "{} {}".format(strong(title), text)

# def career_progression_item(data):
#     period = '{} - {}'.format(data['start'], data['end'])
#     title = "'{}' {}".format(data['title'], italic(period))

#     items = project_item(data)
#     items[0:0] = [titled_item("Company Description:",
#                               data['companyDescription'])]
#     progresssion_item = ul(title, items)
#     technologies = sub_ul('Technologies:', data['technologies'])
#     responsibilities = sub_ul('Responsibilities:', data['responsibilities'])
#     return PARAGRAPH_SEPARATOR.join([progresssion_item, responsibilities, technologies])


# def project_item(data):
#     return [
#         titled_item("Project description:", data['projectDescription']),
#         titled_item("Project role:", data['role']),
#     ]

def project_item(data):
    return titled_item("Project description:", data['projectDescription'])


def career_progression_item(data):
    period = '{} - {}'.format(data['start'], data['end'])
    title = "'{}' {}".format(data['title'], italic(period))

    items = [
        titled_item("Company Description:", data['companyDescription']),
        titled_item("Employment type:", data['employmentType']),
        titled_item("Team size:", data['teamSize']),
    ]

    progresssion_item = titled_ul(title, items)
    project_items = [project_item(p) for p in data["projects"]]

    return PARAGRAPH_SEPARATOR.join([progresssion_item, ul(project_items)])


def career_progression_block(data):
    progression = [career_progression_item(c) for c in data]
    progression_block = BLOCK_SEPARATOR.join(progression)
    return PARAGRAPH_SEPARATOR.join([h2('Career Progression:'), progression_block])


def language_skills_block(data):
    return titled_ul('Language Skills:', data)


def online_education_item_title(ed):
    if ed['start'] == ed['end']:
        title = title = "{} ({})".format(ed['title'], ed['start'])
        return strong(title)

    title = title = "{} ({} - {})".format(ed['title'], ed['start'], ed['end'])
    return strong(title)


def online_education_item(ed):
    return '[{}] {} {} '.format(ed['platform'], online_education_item_title(ed), link('Certificate', ed['certificate']))


def online_education_block(data):
    return titled_ul('Online education:', [online_education_item(ed) for ed in data])


def classic_education_item(ed):
    title = '{} ({} - {})'.format(ed['institution'], ed['start'], ed['end'])
    achivements = PARAGRAPH_SEPARATOR.join(
        ['\t{}'.format(li(a)) for a in ed['achivements']])
    return PARAGRAPH_SEPARATOR.join([strong(title), achivements])


def classic_education_block(data):
    return titled_ul('Education:', [classic_education_item(ed) for ed in data])


def further_interests_block(data):
    return titled_ul('Further Interests:', [link(d['title'], d['url']) for d in data])


def generate_md(cv):
    return BLOCK_SEPARATOR.join([
        head_block(cv['name'], cv['title']),
        contacts_block(cv['contacts']),
        career_summary_block(cv['careerSummary']),
        career_progression_block(cv['careerProgression']),
        language_skills_block(cv['languageSkills']),
        online_education_block(cv['onlineEducation']),
        classic_education_block(cv['classicEducation']),
        further_interests_block(cv['furtherInterests']),
        meta()
    ])


if __name__ == '__main__':
    with open(CV_JSON) as cv_json:
        content = generate_md(json.load(cv_json))
        print('Writing to {}'.format(README_MD_FILE))
        f = open(README_MD_FILE, 'w')
        f.write(content)
        f.close()
        print('Done')
