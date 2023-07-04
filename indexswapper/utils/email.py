from indexswapper.models import SwapRequest
from NTUSU_BE.utils import DO_NOT_REPLY_MESSAGE, send_email
from sso.models import User


def send_swap_request_creation(user: User, swap_request_data: dict):
    SUBJECT = 'Index Swapper - Swap Request Creation Confirmation'
    CONTENT = f'''
Hi, {user.username}!<br>
<br>
This is a confirmation email that your swap request has been created.
Here is the information of your swap request:<br>
ID: {swap_request_data['id']}<br>
Your Contact Information: {swap_request_data['contact_info']}<br>
Course: {swap_request_data['course_name']} ({swap_request_data['course_code']})<br>
Current Index: {swap_request_data['current_index']}<br>
Wanted Indexes: {', '.join(swap_request_data['wanted_indexes'])}<br>
<br>
An algorithm is currently searching for a pair for you.
You will be contacted shortly through this email if a pair is found.
If a pair is not found, you will be placed under waiting list.<br>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [user.email])


def send_swap_search_another(user, swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Search Another Pair Confirmation'
    CONTENT = f'''
Hi, {user.username}!<br>
<br>
This is a confirmation email that you are currently finding a new pair.
We apologize for the inconvenience that the previous pair does not work out.
We will take necessary action to prevent irresponsible users from abusing this system.<br>
Here is the information of your swap request:<br>
ID: {swap_request.id}<br>
Your Contact Information: {swap_request.contact_info}<br>
Course: {swap_request.current_index.name} ({swap_request.current_index.code})<br>
Current Index: {swap_request.current_index}<br>
Wanted Indexes: {', '.join(swap_request.wanted_indexes)}<br>
<br>
An algorithm is currently searching for a pair for you.
You will be contacted shortly through this email if a pair is found.
If a pair is not found, you will be placed under waiting list.<br>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [user.email])


def send_swap_completed(user, swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Completed'
    CONTENT = f'''
Hi, {user.username}!<br>
<br>
Thank you for using Index Swapper!<br>
    '''
    return send_email(SUBJECT, CONTENT, [user.email])


def send_swap_cancel_self(user: User, swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Cancel Search Confirmation'
    CONTENT = f'''
Hi, {user.username}!<br>
<br>
This is a confirmation email that you have cancelled this swap request:<br>
ID: {swap_request.id}<br>
Your Contact Information: {swap_request.contact_info}<br>
Course: {swap_request.current_index.name} ({swap_request.current_index.index})<br>
Current Index: {swap_request.current_index}<br>
Wanted Indexes: {', '.join(swap_request.wanted_indexes)}<br>
<br>
We apologize if you cancel this due to long waiting time, or no pair is found.<br>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [user.email])  # TODO - change this to pair email


def send_swap_cancel_pair(user: User, swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Pair Cancelled Swap Request'
    CONTENT = f'''
Hi, {user.username}!<br>
<br>
This is a confirmation email that you have cancelled this swap request:<br>
ID: {swap_request.id}<br>
Your Contact Information: {swap_request.contact_info}<br>
Course: {swap_request.current_index.index} ({swap_request.current_index.code})<br>
Current Index: {swap_request.current_index}<br>
Wanted Indexes: {', '.join(swap_request.wanted_indexes)}<br>
<br>
We apologize if you cancel this due to long waiting time, or no pair is found.<br>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [user.email])
