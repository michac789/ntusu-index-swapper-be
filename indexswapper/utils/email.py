from indexswapper.models import SwapRequest
from NTUSU_BE.constants import FE_URL
from NTUSU_BE.utils import DO_NOT_REPLY_MESSAGE, send_email


def get_contact_type_label(contact_type: str):
    mapping = dict(SwapRequest.ContactType.choices)
    return mapping.get(contact_type, 'Invalid contact type')


def send_swap_request_creation(swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Swap Request Creation Confirmation'
    CONTENT = f'''
<p>Hi, <b>{swap_request.user.display_name}!</b> (username: <b>{swap_request.user.username}</b>)</p>
<p><span><br></span></p>
<p>
    This is a confirmation email that your swap request has been created:
</p>
<ul>
    <li>ID: <b>#{swap_request.id}</b></li>
    <li>Course: <b>{swap_request.current_index.name} ({swap_request.current_index.code})</b></li>
    <li>Current Index: <b>{swap_request.current_index.index}</b></li>
    <li>Wanted Indexes: <b>{', '.join(swap_request.wanted_indexes)}</b></li>
    <li>Your Contact: <b>{swap_request.contact_info}
    ({get_contact_type_label(swap_request.contact_type)})</b></li>
</ul>
<p>
    An algorithm is currently searching a pair for you.
    You will be contacted shortly if a match is found.
    If a match is not found, you will be placed under waiting list, and will be contacted once a pair is found.
</p>
<p><br></p>
<p>Thank you for your attention.</p>
<hr>
<p>Important Links:</p>
<p>- Check your SwapRequest status <a href="{FE_URL['indexswapper-myswaprequests']}">here</a>.</p>
<p>- Check how many people want your current index <a href="{FE_URL['indexswapper-allmodules']}">here</a>.
You can click on the pending request number to see the details.</p>
<p>- Send your feedbacks, criticism and suggestions for our service <a href="{FE_URL['portal-feedback']}">here</a>.</p>
<hr>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [swap_request.user.email])


def send_swap_search_another(swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Search Another Pair Confirmation'
    CONTENT = f'''
<p>Hi, <b>{swap_request.user.display_name}!</b> (username: <b>{swap_request.user.username}</b>)</p>
<p><span><br></span></p>
<p>
    This is a confirmation email that you are searching for another pair.
    We apologize for the inconvenience that your previous pair is not working out.
    We will take necessary action to prevent irresponsible users from abusing this system.
    Here is the information of your current swap request:
</p>
<ul>
    <li>ID: <b>#{swap_request.id}</b></li>
    <li>Course: <b>{swap_request.current_index.name} ({swap_request.current_index.code})</b></li>
    <li>Current Index: <b>{swap_request.current_index.index}</b></li>
    <li>Wanted Indexes: <b>{', '.join(swap_request.get_wanted_indexes)}</b></li>
    <li>Your Contact: <b>{swap_request.contact_info}
    ({get_contact_type_label(swap_request.contact_type)})</b></li>
</ul>
<p>
    An algorithm is currently searching a pair for you.
    You will be contacted shortly if a match is found.
    If a match is not found, you will be placed under waiting list, and will be contacted once a pair is found.
</p>
<p><br></p>
<p>Thank you for your attention.</p>
<hr>
<p>Important Links:</p>
<p>- Check your SwapRequest status <a href="{FE_URL['indexswapper-myswaprequests']}">here</a>.</p>
<p>- Check how many people want your current index <a href="{FE_URL['indexswapper-allmodules']}">here</a>.
You can click on the pending request number to see the details.</p>
<p>- Send your feedbacks, criticism and suggestions for our service <a href="{FE_URL['portal-feedback']}">here</a>.</p>
<hr>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [swap_request.user.email])


def send_swap_cancel_self(swap_request: SwapRequest, is_waiting: bool = True):
    SUBJECT = 'Index Swapper - Cancel Swap Confirmation'
    CONTENT = f'''
<p>Hi, <b>{swap_request.user.display_name}!</b> (username: <b>{swap_request.user.username}</b>)</p>
<p><span><br></span></p>
<p>
    This is a confirmation email that you have <u>cancelled</u> this swap request:
</p>
<ul>
    <li>ID: <b>#{swap_request.id}</b></li>
    <li>Course: <b>{swap_request.current_index.name} ({swap_request.current_index.code})</b></li>
    <li>Current Index: <b>{swap_request.current_index.index}</b></li>
    <li>Wanted Indexes: <b>{', '.join(swap_request.get_wanted_indexes)}</b></li>
    <li>Your Contact: <b>{swap_request.contact_info}({get_contact_type_label(swap_request.contact_type)})</b></li>
    <li>Status: <b>{is_waiting and 'Waiting' or 'Searching'}</b></li>
</ul>
<p>
    {is_waiting and 
     """
     <p style="color: orange;">
Please note that you are cancelling a swap request that has been paired.
This action might cause inconvenience to the other pair, so please refrain on cancelling a paired swap request.
If you repeat such action many times, you will be banned from using this service.
     </p>
     """
     or 
     'We apologize if you cancel the swap request due to long waiting time, or if you have found another pair outside of this platform.'}
</p>
<p><br></p>
<p>Thank you for your attention.</p>
<hr>
<p>Important Links:</p>
<p>- Check your SwapRequest status <a href="{FE_URL['indexswapper-myswaprequests']}">here</a>.</p>
<p>- Check how many people want your current index <a href="{FE_URL['indexswapper-allmodules']}">here</a>.
You can click on the pending request number to see the details.</p>
<p>- Send your feedbacks, criticism and suggestions for our service <a href="{FE_URL['portal-feedback']}">here</a>.</p>
<hr>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [swap_request.user.email])


def send_swap_cancel_pair(swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Pair Cancelled Swap Request'
    CONTENT = f'''
<p>Hi, <b>{swap_request.user.display_name}!</b> (username: <b>{swap_request.user.username}</b>)</p>
<p><span><br></span></p>
<p>
    We are sorry to say that your pair has decided to cancel the swap request:
</p>
<ul>
    <li>ID: <b>#{swap_request.id}</b></li>
    <li>Course: <b>{swap_request.current_index.name} ({swap_request.current_index.code})</b></li>
    <li>Current Index: <b>{swap_request.current_index.index}</b></li>
    <li>Wanted Indexes: <b>{', '.join(swap_request.get_wanted_indexes)}</b></li>
    <li>Your Contact: <b>{swap_request.contact_info}
    ({get_contact_type_label(swap_request.contact_type)})</b></li>
</ul>
<p>
    We will take necessary action to prevent irresponsible users from abusing this system.
    As a result, your swap request is placed back under 'SEARCHING' status.
    An algorithm is currently searching a pair for you.
    You will be contacted shortly if a match is found.
    If a match is not found, you will be placed under waiting list, and will be contacted once a pair is found.
</p>
<p><br></p>
<p>Thank you for your attention.</p>
<hr>
<p>Important Links:</p>
<p>- Check your SwapRequest status <a href="{FE_URL['indexswapper-myswaprequests']}">here</a>.</p>
<p>- Check how many people want your current index <a href="{FE_URL['indexswapper-allmodules']}">here</a>.
You can click on the pending request number to see the details.</p>
<p>- Send your feedbacks, criticism and suggestions for our service <a href="{FE_URL['portal-feedback']}">here</a>.</p>
<hr>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [swap_request.user.email])


def send_swap_completed(swap_request: SwapRequest):
    pass  # TODO need this?


def send_swap_pair_found(swap_request: SwapRequest):
    SUBJECT = 'Index Swapper - Pair Found!'
    CONTENT = f'''
<p>Hi, <b>{swap_request.user.display_name}!</b> (username: <b>{swap_request.user.username}</b>)</p>
<p><span><br></span></p>
<p>
    A pair is found. Here are the details:
</p>
<ul>
    <li>ID: <b>#{swap_request.id}</b></li>
    <li>Course: <b>{swap_request.current_index.name} ({swap_request.current_index.code})</b></li>
    <li>Current Index: <b>{swap_request.current_index.index}</b></li>
    <li>Wanted Indexes: <b>{', '.join(swap_request.get_wanted_indexes)}</b></li>
    <li>Your Contact: <b>{swap_request.contact_info}
    ({get_contact_type_label(swap_request.contact_type)})</b></li>
    <li style="color: blue;">Pair's Contact: <b>{swap_request.pair.contact_info}
    ({get_contact_type_label(swap_request.pair.contact_type)})</b></li>
    <li style="color: blue;">Index gained: <b>{swap_request.index_gained}</b></li>
</ul>
<p style="color: blue;">
    We will take necessary action to prevent irresponsible users from abusing this system.
    As a result, your swap request is placed back under 'SEARCHING' status.
    An algorithm is currently searching a pair for you.
    You will be contacted shortly if a match is found.
    If a match is not found, you will be placed under waiting list, and will be contacted once a pair is found.
</p>
<p><br></p>
<p>Thank you for your attention.</p>
<hr>
<p>Important Links:</p>
<p>- Check your SwapRequest status <a href="{FE_URL['indexswapper-myswaprequests']}">here</a>.</p>
<p>- Check how many people want your current index <a href="{FE_URL['indexswapper-allmodules']}">here</a>.
You can click on the pending request number to see the details.</p>
<p>- Send your feedbacks, criticism and suggestions for our service <a href="{FE_URL['portal-feedback']}">here</a>.</p>
<hr>
{DO_NOT_REPLY_MESSAGE}
    '''
    return send_email(SUBJECT, CONTENT, [swap_request.user.email])
