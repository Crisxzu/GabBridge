from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password, make_password
from bridge.models import Client
import logging

logger = logging.getLogger(__name__)


class AccountNumberBackend(ModelBackend):
    def authenticate(self, request, card_number=None, pin=None, **kwargs):
        if not card_number or not pin:
            return None

        try:
            user = Client.objects.get(card_number=card_number)
            if check_password(pin, user.pin):
                return user
            else:
                return None

        except Client.DoesNotExist:
            logger.warning(f"Login attempt with non-existent account: {card_number}")
            return None
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None