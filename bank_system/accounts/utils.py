"""
Telegram login authentication functionality.
"""
from functools import wraps
import hashlib
import hmac
import time
from django.shortcuts import redirect
from django.views.generic.edit import View
from django.contrib.auth.mixins import AccessMixin



ONE_DAY_IN_SECONDS = 86400


def verify_telegram_authentication(bot_token, request_data) -> bool:
    """
    Check if received data from Telegram is real.

    Based on SHA and HMAC algothims.
    Instructions - https://core.telegram.org/widgets/login#checking-authorization
    """
    request_data = request_data.copy()

    received_hash = request_data['hash']
    auth_date = request_data['auth_date']

    request_data.pop('hash', None)
    request_data_alphabetical_order = sorted(request_data.items(), key=lambda x: x[0])

    data_check_string = []

    for data_pair in request_data_alphabetical_order:
        key, value = data_pair[0], data_pair[1]
        data_check_string.append(key + '=' + value)

    data_check_string = '\n'.join(data_check_string)

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    _hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)

    if unix_time_now - unix_time_auth_date > ONE_DAY_IN_SECONDS:
        return False

    if _hash != received_hash:
        return False

    return True

           
class LoginConfirmedRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated, telegram is connected and ."""

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.user.telegram_id != 0:
                if request.user.confirmed:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    self.redirect_field_name = "await_confirm"
            else:
                self.redirect_field_name = "register_telegram"
        else:
            self.redirect_field_name = "login"
        
        return self.handle_no_permission()