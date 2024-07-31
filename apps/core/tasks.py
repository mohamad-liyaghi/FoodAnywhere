from celery import shared_task
from templated_mail.mail import BaseEmailMessage


@shared_task
def send_email(template_path: str, to_email: str, subject: str, context: dict) -> str:
    """
    Email the specified recipient using the provided template and context.
    """
    email_message = BaseEmailMessage(
        subject=subject,
        template_name=template_path,
        context={**context},
    )
    email_message.send(to=[to_email])
    return f"Email sent to {to_email} successfully."
