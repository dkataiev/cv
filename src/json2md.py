import json
import os

from datetime import date

BLOCK_SEPARATOR = '\n\n___\n\n'
PARA_SEPARATOR = '\n'
HR = '---'


def h2(text):
    return '## {}'.format(text)


def h3(text):
    return '### {}'.format(text)


def h4(text):
    return '#### {}'.format(text)


def h5(text):
    return '##### {}'.format(text)


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
    return PARA_SEPARATOR.join(list)


def ul_title(text):
    return strong(text)


def titled_ul(title, items):
    list = [li(i) for i in items]
    list[0:0] = [title]
    return PARA_SEPARATOR.join(list)


def sub_ul(items, level):
    offset = '\t' * level
    list = ['{}{}'.format(offset, li(i)) for i in items]
    return PARA_SEPARATOR.join(list)


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
    return h3('{} - {}'.format(name, title))


def contacts_block(data):
    return titled_ul(h4('Contacts:'), [contact_text(c) for c in data])


def career_summary_block(data):
    return PARA_SEPARATOR.join([h4('Career Summary:'), data])


def skills_block(data):
    return titled_ul(h4('Skills:'), data)


def titled_item(title, text):
    return "{} {}".format(strong(title), text)


def project_item(data):
    title = titled_item("Project description:", data['projectDescription'])
    responsibilities = sub_ul(data['responsibilities'], 2)
    responsibilities_text = '{}{}'.format(PARA_SEPARATOR, responsibilities)
    technologies = sub_ul(data['technologies'], 2)
    technologies_text = '{}{}'.format(PARA_SEPARATOR, technologies)
    items = [
        titled_item("Project role:", data['role']),
        titled_item("Team size:", data['teamSize']),
        titled_item('Responsibilities:', responsibilities_text),
        titled_item('Technologies:', technologies_text)
    ]
    return PARA_SEPARATOR.join([title, sub_ul(items, 1)])


def career_progression_item(data):
    title = "'{}'".format(data['title'])
    period = '{} - {}'.format(data['start'], data['end'])
    item_title = '{} ({})'.format(strong(title), italic(period))

    items = [
        titled_item("Company Description:", data['companyDescription']),
        titled_item("Employment type:", data['employmentType']),
    ]

    progresssion_item = titled_ul(item_title, items)
    project_items = [project_item(p) for p in data["projects"]]

    return PARA_SEPARATOR.join([progresssion_item, ul(project_items)])


def career_progression_block(data):
    progression = [career_progression_item(c) for c in data]
    progression_block = BLOCK_SEPARATOR.join(progression)
    return PARA_SEPARATOR.join([h4('Career Progression:'), progression_block])


def language_skills_block(data):
    return titled_ul(h4('Language Skills:'), data)


def online_education_item_title(ed):
    if ed['start'] == ed['end']:
        title = title = "{} ({})".format(ed['title'], ed['start'])
        return strong(title)

    title = title = "{} ({} - {})".format(ed['title'], ed['start'], ed['end'])
    return strong(title)


def online_education_item(ed):
    return '[{}] {} {} '.format(ed['platform'], online_education_item_title(ed), link('Certificate', ed['certificate']))


def online_education_block(data):
    return titled_ul(h4('Online education:'), [online_education_item(ed) for ed in data])


def classic_education_item(ed):
    title = '{} ({} - {})'.format(ed['institution'], ed['start'], ed['end'])
    achivements = PARA_SEPARATOR.join(
        ['\t{}'.format(li(a)) for a in ed['achivements']])
    return PARA_SEPARATOR.join([strong(title), achivements])


def classic_education_block(data):
    return titled_ul(h4('Education:'), [classic_education_item(ed) for ed in data])


def further_interests_block(data):
    return titled_ul(h4('Further Interests:'), [link(d['title'], d['url']) for d in data])


def generate_md(cv):
    return BLOCK_SEPARATOR.join([
        head_block(cv['name'], cv['title']),
        contacts_block(cv['contacts']),
        career_summary_block(cv['careerSummary']),
        skills_block(cv['hardSkills']),
        career_progression_block(cv['careerProgression']),
        language_skills_block(cv['languageSkills']),
        online_education_block(cv['onlineEducation']),
        classic_education_block(cv['classicEducation']),
        further_interests_block(cv['furtherInterests']),
        meta()
    ])
