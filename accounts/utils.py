from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailActivateTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, new_request, timestamp):
        return six.text_type(new_request.id)+six.text_type(timestamp)+six.text_type(new_request.is_email_verified)

generateToken = EmailActivateTokenGenerator()


