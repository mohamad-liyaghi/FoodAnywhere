from django.db import models


class LoginDeviceType(models.TextChoices):
    ANDROID = "a", "Android"
    IOS = "i", "iOS"
    WINDOWS = "w", "Windows"
    MACOS = "m", "macOS"
    LINUX = "l", "Linux"
    UNKNOWN = "u", "Unknown"


class LoginBrowserType(models.TextChoices):
    CHROME = "c", "Chrome"
    FIREFOX = "f", "Firefox"
    SAFARI = "s", "Safari"
    EDGE = "e", "Edge"
    OPERA = "o", "Opera"
    UNKNOWN = "u", "Unknown"
