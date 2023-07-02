from indexswapper.models import SwapRequest


def perform_pairing(swap_request_id: int):
    '''
    ### IMPORTANT WARNING !!! ###
    TODO - lock db using transaction to prevent clashes
    TLDR; this function should only be called one at a time,
    even if db accept multiple connection & server has multiple threads / instances
    If this function is called multiple times at the same time,
    it may cause the same swap request to be paired with multiple swap requests

    This function is to be called:
    - when a new swap request is created
        (call with that swap request id)
    - when a pair has been matched, but one side cancel it
        (call with the swap request id of the other side)
    - when a pair has been matched, swap unsuccessful after cooldown,
        and one side reinitiate the search
        (call with this user's swap request id, no need to do for the other side)

    Pseudocode:
    - Make this SwapRequest status to SEARCHING (it may be 'WAITING')
    - Filter all swap request that has status of waiting, has the same course code,
        and exclude this swap request
    - For each instance of the filtered swap request:
        - If this swap request's current index is in the instance's wanted indexes,
            and the instance's current index is in this swap request's wanted indexes,
            then:
            - Fill in the 'pair' column and 'index_gained' column for both swap requests
            - Set both swap requests' status to WAITING
            - Return True
    - Otherwise return False
    '''
    swap_request = SwapRequest.objects.get(id=swap_request_id)
    swap_request.status = SwapRequest.Status.SEARCHING
    instances = SwapRequest.objects.filter(
        status=SwapRequest.Status.SEARCHING,
        current_index__code=swap_request.current_index.code)\
        .exclude(id=swap_request_id)
    for instance in instances:
        if instance.current_index.index in swap_request.get_wanted_indexes and\
                swap_request.current_index.index in instance.get_wanted_indexes:
            swap_request.status = SwapRequest.Status.WAITING
            instance.status = SwapRequest.Status.WAITING
            swap_request.pair = instance
            instance.pair = swap_request
            swap_request.index_gained = instance.current_index.index
            instance.index_gained = swap_request.current_index.index
            instance.save()
            swap_request.save()
            return True
    swap_request.save()
    return False
