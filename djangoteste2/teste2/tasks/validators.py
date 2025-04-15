from django.core.exceptions import ValidationError

class MaximumLengthValidator:
    def __init__(self, max_length = None):
        self.max_length = max_length

    def validate(self, password, user=None):
        if self.max_length is not None and len(password) > self.max_length:
            raise ValidationError(
                f"This password must be at most {self.max_length} characters long.",
                code='password_max_length',
                params={'max_length': self.max_length},
            )
    
    def get_help_text(self):
        return f"Your password must be at most {self.max_length} characters long."