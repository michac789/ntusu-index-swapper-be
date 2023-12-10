from rest_framework.test import APITestCase
import os
from modsoptimizer.models import CourseCode, CourseIndex
from modsoptimizer.utils.course_scraper import get_raw_data, process_data, save_course_data
from modsoptimizer.utils.exam_scraper import get_soup_from_html_file


class TestCourseScraper(APITestCase):
    '''
    Given soup of courses page, test these functions from `test_course_scraper`:
    - get_raw_data
    - process_data
    - save_course_data
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FILE_PATH = os.path.join('modsoptimizer', 'utils', 'scraping_files', 'course_schedule.html')
        self.soup = get_soup_from_html_file(FILE_PATH)
    
    def get_schedule_str(self, *args):
        # return a string of 'O' of length 192 (32 * 6) with 'X' on the given args (1 index)
        schedule_list = ['O'] * 192
        for arg in args:
            schedule_list[arg - 1] = 'X'
        return ''.join(schedule_list)
    
    def test_soup_1(self):
        raw_data = get_raw_data(self.soup, 0, 0)
        self.assertEqual(raw_data,
        [
            (
                {
                    "course_code": "AAA08B",
                    "course_name": "FASHION & DESIGN: WEARABLE ART AS A SECOND SKIN",
                    "academic_units": 3,
                },
                [
                    {
                        "index": "39619",
                        "info": [
                            {
                                "type": "LEC/STUDIO",
                                "group": "LE",
                                "day": "THU",
                                "time": "1330-1620",
                                "venue": "NIE7-02-07",
                                "remark": "",
                            }
                        ],
                    }
                ],
            )
        ])
        processed_data = process_data(raw_data)
        self.assertEqual(processed_data,
        [
            {
                "course_code": "AAA08B",
                "course_name": "FASHION & DESIGN: WEARABLE ART AS A SECOND SKIN",
                "academic_units": 3,
                "indexes": [
                    {
                        "index": "39619",
                        "schedule": self.get_schedule_str(108, 109, 110, 111, 112, 113),
                        "information": "LEC/STUDIO^LE^THU^1330-1620^NIE7-02-07^",
                    }
                ],
                "common_schedule": self.get_schedule_str(108, 109, 110, 111, 112, 113),
            }
        ])
        save_course_data(processed_data)
        course_code = CourseCode.objects.get(code='AAA08B')
        self.assertEqual(course_code.name, 'FASHION & DESIGN: WEARABLE ART AS A SECOND SKIN')
        self.assertEqual(course_code.academic_units, 3)
        self.assertEqual(course_code.common_schedule, self.get_schedule_str(108, 109, 110, 111, 112, 113))
        course_index = CourseIndex.objects.get(index='39619')
        self.assertEqual(course_index.course, course_code)
        self.assertEqual(course_index.schedule, self.get_schedule_str(108, 109, 110, 111, 112, 113))
        self.assertEqual(course_index.information, "LEC/STUDIO^LE^THU^1330-1620^NIE7-02-07^")
        self.assertEqual(course_index.get_information, [
            {
                "type": "LEC/STUDIO",
                "group": "LE",
                "day": "THU",
                "time": "1330-1620",
                "venue": "NIE7-02-07",
                "remark": "",
            }
        ])
