from django.db import models
from django.conf import settings
from active_sessions.enums import LoginDeviceType, LoginBrowserType


class ActiveSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="active_sessions",
    )
    device_type = models.CharField(max_length=1, choices=LoginDeviceType.choices, default=LoginDeviceType.UNKNOWN)
    browser_type = models.CharField(max_length=1, choices=LoginBrowserType.choices, default=LoginBrowserType.UNKNOWN)
    ip_address = models.GenericIPAddressField()
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ip_address} - {self.date}"

    class Meta:
        ordering = ["-date"]
        verbose_name = "Active Session"
        verbose_name_plural = "Active Sessions"
