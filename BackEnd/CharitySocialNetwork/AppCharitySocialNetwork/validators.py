import re

from django.core.exceptions import ValidationError
from django.utils.regex_helper import _lazy_re_compile


class PasswordValidator:
    list_message = {
        'ENG':
            'Password minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character',
        'VN':
            'Mật khẩu tối thiểu tám ký tự, ít nhất một ký tự hoa, một ký tự viết thường, một số và một ký tự đặc biệt',
    }
    message = list_message.get('ENG')
    code = 'invalid'
    user_regex = _lazy_re_compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",  # dot-atom

        re.IGNORECASE)
    language = 'ENG'

    def __init__(self, message=None, code=None, language=None):

        if language is not None:
            self.language = language
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def get_message(self):
        return self.list_message.get(self.language)

    def __call__(self, value):

        if not self.user_regex.match(value):
            raise ValidationError(self.get_message(), code=self.code, params={'value': value})

    def __eq__(self, other):
        return (
                isinstance(other, PasswordValidator) and
                (self.message == other.message) and
                (self.code == other.code)
        )
