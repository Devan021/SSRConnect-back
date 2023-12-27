from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError, APIException


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="user/profile_pictures",
        null=True,
        blank=True,
        verbose_name="Profile Picture",
    )
    avatarID = models.CharField(max_length=50, null=True, blank=True)
    team = models.ForeignKey("user.Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    name = models.CharField(max_length=255, null=True, blank=True)

    @property
    def type(self):
        if self.is_superuser:
            return "ADMIN"
        elif self.is_staff:
            return "MENTOR"
        else:
            return "STUDENT"

    def update_password(self, newPassword: str) -> None:
        if len(newPassword) < 8:
            raise ValidationError("Password is too short", code="PASSWORD_TOO_SHORT")

        self.set_password(raw_password=newPassword)

    def change_password(self, old_password, new_password):
        if not self.check_password(raw_password=old_password):
            raise APIException(detail="Current password is incorrect", code="INVALID_OLD_PASSWORD")
        self.update_password(new_password)
        self.save()

    def confirm_password_reset(self, newPassword, otp):
        # from user.utils.email import notify_user_on_password_change
        #
        # if not self.compare_otp(otp=otp):
        #     raise APIError("Invalid OTP provided", code="INVALID_OTP")
        #
        self.update_password(newPassword)

        self.save()
        from user.models.email_otp import EmailOTP

        EmailOTP.objects.filter(email=self.email).delete()
        # @TODO: Setup email otp ratelimiting and mailing
        # notify_user_on_password_change(user=self)
        return True

    def clean(self):
        if self.pk is None and self.avatarID is None:
            from random import randint
            self.avatarID = str(randint(1, 10))

        if self.email.endswith("@am.amrita.edu"):
            self.is_staff = True

        self.username = self.email

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]