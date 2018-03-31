"""
Scrape trail data from the completion list on the PCTA site.
"""
from load_mongo import load_mongo_db
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select

import time


def main():
    """
    Instantiate a selenium browser. Retrieve url. Pull data from tabel.
    """
    windows_driver = '/mnt/c/Users/kurtrm/Documents/bin/chromedriver.exe'
    browser = Chrome(executable_path=windows_driver)

    url = 'https://www.pcta.org/discover-the-trail/' \
          'thru-hiking-long-distance-hiking/2600-miler-list/'

    browser.get(url)
    year_range = range(1952, 2018)  # Range of years of recorded thru-hikes

    for year in year_range:
        select = Select(browser.find_element_by_id('year'))
        select.select_by_value(str(year))
        time.sleep(1.5)
        miler_list = browser.find_elements_by_css_selector('td')
        if miler_list[0].text != 'No records found for the selected year.':
            people = extract_names(miler_list, year)
            load_mongo_db('pct', 'completions', people)


def extract_names(elements, year):
    """
    Extract the name from the web element and assign them keywords
    in a dictionary.

    Parameters
    ----------
    element: selenium web element

    Returns
    -------
    dict
    """
    milers = []
    groupings = _miler_grouper(elements)
    # import pdb; pdb.set_trace()
    for miler in groupings:
        person = {'last_name': miler[0],
                  'first_name': miler[1],
                  'trail_name': miler[2],
                  'year': year}
        milers.append(person)

    return milers


def _miler_grouper(iterable):
    """
    Group miler names into threes.
    Yields a generator.
    """
    length = len(iterable) + 1
    if length == 3:
        yield [each.text for each in iterable]
    for i in range(3, length, 3):
        previous = i - 3
        group = iterable[previous: i]
        yield [each.text for each in group]


if __name__ == '__main__':
    main()
