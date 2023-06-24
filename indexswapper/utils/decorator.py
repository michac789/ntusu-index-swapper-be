from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from indexswapper.models import SwapRequest


def get_swap_request_with_id_verify(*allowed_status):
    '''
        Custom decorator that gets SwapRequest object by its id (given in url).
        Takes in allowed status args, which are the status allowed for the object.
        Return 401 if user is not authenticated.
        Return 404 if object is not found.
        Return 403 if requesting user is not owner of object.
        Return 400 if object status is not in allowed status.
        You can access the retrieved object from `kwargs['instance']`.
    '''
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(request, *args, **kwargs):
            kwargs['instance'] = get_object_or_404(
                SwapRequest, id=kwargs['id'])
            if kwargs['instance'].owner != request.user:
                return Response({
                    'error': 'you are not the owner of this request'
                }, status=status.HTTP_403_FORBIDDEN)
            if kwargs['instance'].status not in allowed_status:
                return Response({
                    'error': f'only allow status of {allowed_status}'
                }, status=status.HTTP_400_BAD_REQUEST)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def verify_cooldown(COOLDOWN_HOURS=24):
    '''
        Custom decorator that verify SwapRequest object cooldown.
        It access the object from kwargs['instance'].
        Return 400 if object status is not in allowed COOLDOWN_HOURS has not passed.
        Else execute the main decorated function.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            dt_found = kwargs['instance'].datetime_found
            if tz.now() < dt_found + COOLDOWN_HOURS:
                return Response({
                    'error': 'waiting for cooldown',
                    'time_left': -tz.now() + dt_found + COOLDOWN_HOURS
                }, status=status.HTTP_400_BAD_REQUEST)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
