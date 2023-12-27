from django.utils.timezone import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class EmailOTP(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, null=True, blank=True
    )
    code = models.CharField(max_length=8)
    timestamp = models.DateTimeField(default=timezone.now)

    @property
    def isValid(self):
        return self.timestamp > timezone.now() - timedelta(minutes=30)

    def _generate_code(self):
        from django.utils.crypto import get_random_string

        self.code = get_random_string(length=6)

    def renew(self):
        if self.timestamp > timezone.now() - timedelta(minutes=1):
            raise ValidationError(
                "Please wait 1 minute before requesting a new code",
                code="WAIT_REQUIRED",
            )
        self._generate_code()
        self.timestamp = timezone.now()
        self.save()

    def clean(self):
        if self.user is not None:
            if self.user.email != self.email:
                raise ValidationError("Email does not match user", code="EMAIL_MISMATCH")
        if self.code is None or self.code == "":
            self._generate_code()
        if self.pk is None:
            # from ..utils.ratelimit import clear_email_otp_attempt_cache_for_email
            #
            # clear_email_otp_attempt_cache_for_email(email=self.email)
            # @TODO: Setup email otp ratelimiting and mailing
            pass


    def delete(self, *args, **kwargs):
        # from ..utils.ratelimit import clear_email_otp_attempt_cache_for_email
        # @TODO: Setup email otp ratelimiting and mailing
        # clear_email_otp_attempt_cache_for_email(email=self.email)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "email_otp"
        verbose_name_plural = "Email OTPs"
        verbose_name = "Email OTP"


__all__ = ["EmailOTP"]
