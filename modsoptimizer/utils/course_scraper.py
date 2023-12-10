from bs4 import BeautifulSoup, element
from urllib import request
from typing import Dict, List, Tuple
import re
from modsoptimizer.models import CourseCode, CourseIndex
from NTUSU_BE.settings import logger


def get_soup_from_url(acadyear: str, acadsem: str) -> BeautifulSoup:
    get_url = lambda acadyear, acadsem: f"https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1?acadsem={acadyear};{acadsem}&staff_access=true&r_search_type=F&boption=Search&r_subj_code="
    url = get_url(acadyear, acadsem)
    with request.urlopen(url) as fp:
        soup = BeautifulSoup(fp, "lxml")
        return soup


def get_raw_data(soup: BeautifulSoup, start: int=0, end: int=99999):
    # Return a list of length (end-start+1) containing 2-sized tuples,
    # where the tuple contain the header table and the schedule table
    # It contains the data for the courses from index `start` to `end` inclusive
    def get_courses_soup() -> List[Tuple[element.Tag, element.Tag]]:
        hr_tags = soup.find_all('hr')
        courses_soup = []
        for i, hr_tag in enumerate(hr_tags):
            if i < start: continue
            if i > end: break
            course_header_table = hr_tag.find_next_sibling()
            course_schedule_table = course_header_table.find_next_sibling()
            courses_soup.append((course_header_table, course_schedule_table))
        return courses_soup

    # Given header table, extract the course code, course name, and academic units
    def extract_header_info(element: element.Tag) -> Dict:
        td_tags = element.find_all('td')
        raw_course_code = td_tags[0].get_text()
        raw_course_name = td_tags[1].get_text()
        raw_academic_units = td_tags[2].get_text()
        course_code = raw_course_code
        course_name = re.sub(r'[*~^#]', '', raw_course_name) # remove unwanted characters
        academic_units = int(float(raw_academic_units.split('AU')[0].strip()))
        return {
            'course_code': course_code,
            'course_name': course_name,
            'academic_units': academic_units
        }
    
    # Given schedule table, extract necessary information and return list of indexes info
    def extract_schedule_info(element: element.Tag) -> List[Dict]:
        rows = element.find_all('tr')[1:] # exclude header row
        # `indexes_list` is list of dict with key `index` and `info`
        # `info` value is a list containing row_info dict below
        indexes_list = []
        temp_info_list = []
        curr_index = ''
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            new_index = cells[0].get_text()
            if i == 0: curr_index = new_index # first index
            
            # if this is a new index, append previous and reset temp_info_list
            if new_index != '' and len(temp_info_list) > 0:
                indexes_list.append({
                    'index': curr_index,
                    'info': temp_info_list[:]
                })
                temp_info_list = []
                curr_index = new_index
            row_info = {
                'type': cells[1].get_text(),
                'group': cells[2].get_text(),
                'day': cells[3].get_text(),
                'time': cells[4].get_text(),
                'venue': cells[5].get_text(),
                'remark': cells[6].get_text()
            }
            temp_info_list.append(row_info)
        indexes_list.append({
            'index': curr_index,
            'info': temp_info_list[:]
        })
        return indexes_list
    
    courses_soup = get_courses_soup()
    raw_data = []
    for header_table, schedule_table in courses_soup:
        header_info = extract_header_info(header_table)
        schedule_info = extract_schedule_info(schedule_table)
        raw_data.append((header_info, schedule_info))
    return raw_data


def process_data(raw_data: List[Tuple[dict, List]]) -> List[Dict]:
    processed_data = []
    # loop through each course
    for data in raw_data:
        clean_data = {}
        
        # common course info
        clean_data['course_code'] = data[0]['course_code']
        clean_data['course_name'] = data[0]['course_name']
        clean_data['academic_units'] = data[0]['academic_units']
        
        # get required data for all indexes of this course
        indexes_data = []
        for index_data in data[1]:
            index_info = {}
            index_info['index'] = index_data['index']
            
            # get schedule list for each index
            schedule_list = ['O'] * 32 * 6 # 32 chars for 16 hours, 6 days a week, per 30mins interval
            for row_info in index_data['info']:
                day, time = row_info['day'], row_info['time']
                days_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
                if day not in days_list:
                    raise ValueError(f'Invalid day: `{day}` (should be one of {days_list})')
                day_index = 32 * days_list.index(day)
                start_time, end_time = time.split('-')
                start_index = (int(start_time[0:2]) - 8) * 2 + \
                    (1 if start_time[2:] == '30' else 0)
                end_index = (int(end_time[0:2]) - 8) * 2 + \
                    (1 if end_time[2:] == '20' else 0)
                schedule_list[day_index + start_index: day_index + end_index] = ['X'] * (end_index - start_index)
            index_info['schedule'] = schedule_list
            
            # get information string for each index
            information_list = []
            for row_info in index_data['info']:
                information = '^'.join([
                    row_info['type'],
                    row_info['group'],
                    row_info['day'],
                    row_info['time'],
                    row_info['venue'],
                    row_info['remark']
                ])
                information_list.append(information)
            index_info['information'] = ';'.join(information_list)
            
            indexes_data.append(index_info)
        clean_data['indexes'] = indexes_data
        
        # get common schedule (that time slot is occupied in all indexes)
        def get_common_schedule_str(*args):
            common_schedule_list = []
            for values in zip(*args):
                if all(val == 'X' for val in values):
                    common_schedule_list.append('X')
                else:
                    common_schedule_list.append('O')
            return ''.join(common_schedule_list)
        schedules_list = [index['schedule'] for index in indexes_data]
        common_schedule = get_common_schedule_str(*schedules_list)
        clean_data['common_schedule'] = common_schedule
        
        # convert schedule list to string for all indexes
        for index in indexes_data:
            index['schedule'] = ''.join(index['schedule'])

        processed_data.append(clean_data)
    return processed_data


def save_course_data(data: List[Dict]) -> None:
    for course in data:
        course_code = CourseCode.objects.create(
            code=course['course_code'],
            name=course['course_name'],
            academic_units=course['academic_units'],
            common_schedule=course['common_schedule'],
        )
        for index in course['indexes']:
            CourseIndex.objects.create(
                course=course_code,
                index=index['index'],
                information=index['information'],
                schedule=index['schedule'],
            )


def perform_course_scraping():
    # constants
    ACADEMIC_YEAR = '2023'
    ACADEMIC_SEMESTER = '2'
    START_INDEX = 3
    END_INDEX = 3
    try:
        soup = get_soup_from_url(ACADEMIC_YEAR, ACADEMIC_SEMESTER)
        raw_data = get_raw_data(soup, START_INDEX, END_INDEX)
        processed_data = process_data(raw_data)
        save_course_data(processed_data)
    except Exception as e:
        logger.error(f'Course Schedule Scraper Error: {e}')
