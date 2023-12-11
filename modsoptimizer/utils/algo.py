from collections import OrderedDict
from modsoptimizer.models import CourseCode


def optimize_index(optimizer_input_data: OrderedDict):
    # TODO - simple backtracking algorithm
    return [
        {
            "code": "MH1101",
            "index": "10405",
        },
        {
            "code": "MH1201",
            "index": "10406",
        }
    ]
