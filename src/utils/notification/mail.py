from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from src.config import settings
from src.utils.notification.mail_content import event_notification_content


class Mail:

    @staticmethod
    def _send_mail(subject: str, content: str, recipient: str) -> None:
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as session:
            session.login(settings.mail.mail, settings.mail.password)

            msg = MIMEMultipart()
            msg["From"] = settings.mail.mail
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(content, "html"))

            try:
                session.send_message(msg)

            except smtplib.SMTPRecipientsRefused:
                raise ValueError('invalid mail')

            finally:
                session.quit()

    @staticmethod
    def send_event(title: str, description: str, date: datetime, email):
        content = event_notification_content.format(title=title, description=description, date=date)
        try:
            Mail._send_mail('Уведомление', content, email)
        except Exception as e:
            print(f"mail error: {e}")