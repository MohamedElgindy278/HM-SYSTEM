import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config.settings import settings
from src.core.exceptions import ExceptionFactory

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """
        Send email using SMTP.
        """
        message = MIMEMultipart()
        message["From"] = settings.SMTP_FROM
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                timeout=10,
            ) as server:
                server.starttls()
                server.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD,
                )
                server.send_message(message)

        except (smtplib.SMTPException, OSError) as e:
            logger.error("Failed to send email to %s: %s", to_email, e)
            raise ExceptionFactory.server_error("Failed to send email")
