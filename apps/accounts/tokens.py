# apps/accounts/tokens.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            force_str(user.pk) + str(timestamp) +
            str(user.is_active)
        )

    def make_token(self, user):
        return self._make_token_with_timestamp(user, self._num_seconds(self._now()))

account_activation_token = AccountActivationTokenGenerator()
