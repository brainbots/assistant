from .abstract_bot import AbstractBot
from bots.action import Action
import sendgrid
from sendgrid.helpers.mail import *
import settings

class MailBot(AbstractBot):
    def __init__(self, id):
        actions = ['send']
        super().__init__(id, actions)
        # REQUIRED
        self.mail_from = None
        self.mail_to = None
        self.subject = None
        self.body = None

    def extract_attr(self, intent):
        if intent.parameters['from']:
            self.mail_from = intent.parameters['from']
        if intent.parameters['to']:
            self.mail_to = intent.parameters['to']
        if intent.parameters['subject']:
            self.subject = intent.parameters['subject']
        if intent.parameters['body']:
            self.body = intent.parameters['body']

    def execute(self):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_ACCESS_TOKEN)
        from_email = Email(self.mail_from)
        to_email = Email(self.mail_to)
        subject = self.subject
        content = Content("text/plain",self.body)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return Action(
            action_type='message',
            body='email sent successfully',
            bot=self.id,
            keep_context=False)

    def is_long_running(self):
        return False

    def has_missing_attr(self):
        return (self.mail_from == None or self.mail_to == None or self.subject == None or self.body == None)

    def request_missing_attr(self):
        if self.mail_from == None:
            return Action(
                action_type='inquiry',
                body='Please specify the sender email address',
                bot=self.id,
                keep_context=True)

        if self.mail_to == None:
            return Action(
                action_type='inquiry',
                body='Please specify the recipient email address',
                bot=self.id,
                keep_context=True)

        if self.subject == None:
            return Action(
                action_type='inquiry',
                body='What is the mail subject?',
                bot=self.id,
                keep_context=True)

        if self.body == None:
            return Action(
                action_type='inquiry',
                body='What is the mail body ?',
                bot=self.id,
                keep_context=True)
