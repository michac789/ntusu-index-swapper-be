'''
    This file is used to scrape exam schedule from NTU website.
    For now, it is to be run manually, save link as html file, then run this script.
    *Why not from website directly?
    - We have to enter some information first before getting access to the page itself,
    a bit difficult and we may have problems when the web is down

    TODO - find a better way to automate this, would be painful to do in prod environment
'''
from bs4 import BeautifulSoup
from datetime import datetime as dt
import os
from typing import Dict, List
from modsoptimizer.models import CourseCode


def get_soup_from_html_file(file_path: str) -> BeautifulSoup:
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return BeautifulSoup(html_content, "lxml")


def get_raw_data(soup: BeautifulSoup) -> List[Dict[str, str]]:
    raw_data = []
    exam_table = soup.find_all('table')[1] # exam schedule is the 2nd table
    rows = exam_table.find_all('tr')[2:] # data starts from 3rd row
    for row in rows:
        cells = row.find_all('td')
        if not cells: break
        raw_data.append({
            'date': cells[0].text.strip(),
            'day': cells[1].text.strip(),
            'time': cells[2].text.strip(),
            'course_code': cells[3].text.strip(),
            'course_title': cells[4].text.strip(),
            'duration': cells[5].text.strip(),
        })
    return raw_data


def process_data(raw_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    data = []
    for exam in raw_data:
        # extract date in DDMMYY format for first 6 characters
        date = exam['date']
        date_object = dt.strptime(date, "%d %B %Y")
        date_str = date_object.strftime("%d%m%y")

        # extract exam time, 'X' for occupied, 'O' for unoccupied
        exam_time_list = ['O'] * 32 # 8am to 12am, 16 hours in total, every 30 mins interval
        hour, am_pm = exam['time'].split(' ')
        start_index = (int(hour.split('.')[0]) - 8) * 2 + (1 if hour.split('.')[1] == '30' else 0)\
            if am_pm == 'am' else \
            (int(hour.split('.')[0])) * 2 + (1 if hour.split('.')[1] == '30' else 0) + 8
        duration_list = exam['duration'].split(' ')
        end_index = start_index + int(duration_list[0]) * 2 + \
            (1 if len(duration_list) > 2 and duration_list[2] == '30' else 0)
        exam_time_list[start_index:end_index] = ['X'] * (end_index - start_index)
        exam_time_str = ''.join(exam_time_list)

        data.append({
            'course_code': exam['course_code'],
            'exam_schedule_str': date_str + exam_time_str,
        })
    return data


def save_exam_schedule(data: List[Dict]) -> None:
    # assume that all course codes are already in database
    for exam_data in data:
        course = CourseCode.objects.get(code=exam_data['course_code'])
        course.exam_schedule = exam_data['exam_schedule_str']
        course.save()


def perform_exam_schedule_scraping():
    try:
        FILE_PATH = os.path.join('modsoptimizer', 'utils', 'scraping_files', 'examtimetable.html')
        soup = get_soup_from_html_file(FILE_PATH)
        raw_data = get_raw_data(soup)
        data = process_data(raw_data)
        save_exam_schedule(data)
    except Exception as e:
        print(f'Error: {e}')
