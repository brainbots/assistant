from .abstract_bot import AbstractBot
from bots.action import Action
import sendgrid
from sendgrid.helpers.mail import *
import settings

class MailBot(AbstractBot):
    def __init__(self, id):
        actions = ['mail.send']
        super().__init__(id, actions)
        # REQUIRED
        self.mail_from = None
        self.mail_to = None
        self.subject = None
        self.body = None

    def extract_attr(self, intent):
        if not self.mail_from :
            if intent.parameters['mail_from']:
                self.mail_from = intent.parameters['mail_from']
        if not self.mail_to :
            if intent.parameters['mail_to']:
                self.mail_to = intent.parameters['mail_to']
        if not self.subject :
            if intent.parameters['subject']:
                self.mail_to = intent.parameters['subject']
        if not self.body :
            if intent.parameters['body']:
                self.mail_to = intent.parameters['body']

    def execute(self):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_ACCESS_TOKEN)
        from_email = Email(self.from_email)
        to_email = Email(self.to_email)
        subject = self.subject
        content = Content(self.body)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)

    def is_long_running(self):
        return False

    def has_missing_attr(self):
        return (self.mail_from == None or self.mail_to == None or self.subject == None or self.body == None)

    def request_missing_attr(self):
        if not self.mail_from:
            return Action(
                action_type='inquiry',
                body='Please specify the sender email address',
                bot=self.id,
                keep_context=True)

        if not self.mail_to:
            return Action(
                action_type='inquiry',
                body='Please specify the recipient email address',
                bot=self.id,
                keep_context=True)

        if not self.subject:
            return Action(
                action_type='inquiry',
                body='What is the mail subject?',
                bot=self.id,
                keep_context=True)

        if not self.body:
            return Action(
                action_type='inquiry',
                body='What is the mail body ?',
                bot=self.id,
                keep_context=True)
