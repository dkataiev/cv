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


def h4(text):
    return '#### {}'.format(text)


def strong(text):
    return '__{}__'.format(text)


def italic(text):
    return '*{}*'.format(text)


def li(text):
    return '* {}'.format(text)


def ul(title, items):
    list = [li(i) for i in items]
    list[0:0] = [h3(title)]
    return PARAGRAPH_SEPARATOR.join(list)


def sub_ul(title, items):
    list = ['\t{}'.format(li(i)) for i in items]
    list[0:0] = [li(strong(title))]
    return PARAGRAPH_SEPARATOR.join(list)


def link(title, body):
    return '[{}]({})'.format(title, body)


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
    return ul('Contacts:', [contact_text(c) for c in data])


def career_summary_block(data):
    return PARAGRAPH_SEPARATOR.join([h3('Career Summary:'), data])


def titled_item(title, text):
    return "{} {}".format(strong(title), text)


def project_item(data):
    return [
        titled_item("Project description:", data['projectDescription']),
        titled_item("Project role:", data['role']),
        titled_item("Employment type:", data['employmentType']),
        titled_item("Team size:", data['teamSize'])
    ]


def career_progression_item(data):
    period = '{} - {}'.format(data['start'], data['end'])
    title = "'{}' {}".format(data['title'], italic(period))

    items = project_item(data)
    items[0:0] = [titled_item("Company Description:",
                              data['companyDescription'])]
    progresssion_item = ul(title, items)
    technologies = sub_ul('Technologies:', data['technologies'])
    responsibilities = sub_ul('Responsibilities:', data['responsibilities'])
    return PARAGRAPH_SEPARATOR.join([progresssion_item, responsibilities, technologies])


def career_progression_block(data):
    progression = [career_progression_item(c) for c in data]
    progression[0:0] = [h2('Career Progression:')]
    return PARAGRAPH_SEPARATOR.join(progression)


def language_skills_block(data):
    return ul('Language Skills:', data)


def online_education_item_title(ed):
    if ed['start'] == ed['end']:
        title = title = "{} ({})".format(ed['title'], ed['start'])
        return strong(title)

    title = title = "{} ({} - {})".format(ed['title'], ed['start'], ed['end'])
    return strong(title)


def online_education_item(ed):
    return '[{}] {} {} '.format(ed['platform'], online_education_item_title(ed), link('Certificate', ed['certificate']))


def online_education_block(data):
    return ul('Online education:', [online_education_item(ed) for ed in data])


def classic_education_item(ed):
    title = '{} ({} - {})'.format(ed['institution'], ed['start'], ed['end'])
    achivements = PARAGRAPH_SEPARATOR.join(
        ['\t{}'.format(li(a)) for a in ed['achivements']])
    return PARAGRAPH_SEPARATOR.join([strong(title), achivements])


def classic_education_block(data):
    return ul('Education:', [classic_education_item(ed) for ed in data])


def further_interests_block(data):
    return ul('Further Interests:', [link(d['title'], d['url']) for d in data])


def generate_md(cv):
    return BLOCK_SEPARATOR.join([
        head_block(cv['name'], cv['title']),
        contacts_block(cv['contacts']),
        career_summary_block(cv['careerSummary']),
        career_progression_block(cv['careerProgression']),
        language_skills_block(cv['languageSkills']),
        online_education_block(cv['onlineEducation']),
        classic_education_block(cv['classicEducation']),
        further_interests_block(cv['furtherInterests'])
    ])


if __name__ == '__main__':
    with open(CV_JSON) as cv_json:
        content = generate_md(json.load(cv_json))
        print('Writing to {}'.format(README_MD_FILE))
        f = open(README_MD_FILE, 'w')
        f.write(content)
        f.close()
        print('Done')
