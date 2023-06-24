from drf_yasg import openapi


API_DESCRIPTIONS = {
    'swaprequest_create': '''
        What this endpoint does:
        - Create new SwapRequest instance
        - Email the user for confirmation that SwapRequest instance has been created
        - Perform pairing algorithm for every SwapRequest instance created
        - If any pair is found, email both users that pair has been found

        Expected input data:
        - **contact_info**: _string (max 100 characters)_
            expected contact information preferred by user such as telegram username, phone number, or email
            currently it is free text (no specific format validation)
        - **current_index**: _string (max 5 characters)_
            course index that the user currently has and wants to be swapped,
            must be a valid course index, all course indexes are unique
        - **wanted_indexes**: _list of strings (max 5 characters each, min 1 item in list)_
            list of course indexes that the user wants to swap to,
            each of those index should be valid, should not be the same as current index,
            and should be the same course code as current_index

        Return output:
        - Return 401 if user is not logged in
        - Return 400 bad request if any of the expected input is not present, or
            if it has wrong data type, or if it exceeds max character
        - Return 404 if CourseIndex instance with index 'current_index' does not exist
        - Return 400 if any of the index in wanted_indexes is invalid, or if it is the same as current index,
            or if any of the index in wanted_indexes is not the same course code as current index
        - Return 201 with created instance if SwapRequest instance is created successfully
    ''',
    'swaprequest_list': '''
        What this endpoint does:
        - Gets all SwapRequest instances that are created by the user

        Optional query parameters:
        - **status**: _either 'W' or 'S' or 'C'_
            filter SwapRequest instances with this status only
            'W': waiting
            'S': searching
            'C': completed
        
        Return output:
        - Return 401 if user is not logged in
        - Return 400 if query parameter format is invalid
        - Return 200 with list of SwapRequest instances if successful

        Sample output:
        ```
        [
            {
                "id": 10,
                "datetime_added": "2023-06-24 11:01:59",
                "datetime_found": null,
                "wanted_indexes": [
                    "70183",
                    "70184"
                ],
                "current_index": "70181",
                "contact_info": "contact telegram @sampletelegram",
                "status": "S",
                "user": 1
            },
            ...
        ]
        ```
    '''
}

swaprequest_qp = openapi.Parameter(
    'status', openapi.IN_QUERY,
    description="filter status with 'S' (searching),'W' (waiting), 'C' (completed))",
    type=openapi.TYPE_STRING)
