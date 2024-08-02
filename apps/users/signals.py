from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from core.tasks import send_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_welcome_email_after_registration(sender, instance, created, **kwargs) -> None:
    """Send welcome email to user after registration."""
    if created:
        send_email.delay(
            template_path="emails/welcome.html",
            subject="Welcome to FoodAnywhere!",
            context={
                "first_name": instance.first_name,
            },
            to_email=instance.email,
        )
