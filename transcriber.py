
"""
1. Using requests, get the webage structure.
2. Parse the info based on HTML classes and ids.
3. Serialize as JSON and pass to Pandas DataFrame for formatting.
"""
import bs4
import re

# Moving past the authentication problem to the actual scraping of the website.

with open('transcript.html') as p:
    soup = bs4.BeautifulSoup(p, 'html.parser')

# The transcript itself is made of <div>s with the class of of 'xcript_grades'
# Actually, the transcript is all in tables held within <div>s, so I'm going
# to find all the tables and iterate over them.


def transcribe(soup):
    """Function doing all of the work."""
    transcript_tables = soup.find_all('table')

    # First we're going to turn everything into dictionaries, which we'll
    # then turn into JSON.
    transcript = {}
    for table in transcript_tables:
        previous_sibling = table.find_previous_sibling()
        if table.get('id') == 'phead':
            td_labels_html = table.find_all(
                'td',
                class_='label'
            )
            td_labels = [label.text.strip() for label in td_labels_html]
            td_data_html = table.find_all(
                'td',
                class_='data'
            )
            td_data = [data.text.strip() for data in td_data_html]
            personal_information = {
                labels: data for labels, data in zip(td_labels, td_data)
            }
            table_heading = table.find_previous_sibling('h2').text.strip()
            transcript[table_heading] = personal_information
        elif previous_sibling and \
                previous_sibling.text == 'Grade/Hour Totals':
            th_html = table.find_all('th')
            th = [info.text.strip() for info in th_html]
            td_html = table.find_all('td')
            td = [info.text.strip() for info in td_html]
            summary = {
                header: data for header, data in zip(th, td)
            }
            table_heading = table.find_previous_sibling('h2').text
            transcript[table_heading] = summary
        elif previous_sibling \
                and \
                previous_sibling.text == 'College Level Academic Skills Test':
            academic_skills = [skill for skill in table.stripped_strings]
            table_heading = table.find_previous_sibling('h2').text
            transcript[table_heading] = academic_skills
        else:
            semester = []
            table_headers = [header.text.strip() for header in table.find_all('th')]
            table_rows = table.find_all('tr')[1:]  # Excluding the header row
            for course in table_rows:
                course_text = [data.text.strip() for data in course.children]
                course_dict = dict(zip(table_headers, course_text))
                semester.append(course_dict)
            if table.find_previous_sibling().get('class') == 'xcript_credit':
                header = table.find_previous_sibling().text.script()
            else:
                header = table.find_previous_sibling('h3').text.strip()
            table.parent
            transcript[header] = semester

    return transcript

# TODO: Gather text at the tail end of <div>s and append them to the course
# list or make another dictionary.
# TODO: Figure out how I want to display this information via pdf, doc, or whatever.

if __name__ == '__main__':
    transcribe(soup)
