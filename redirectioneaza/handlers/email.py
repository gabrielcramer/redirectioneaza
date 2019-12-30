# -*- coding: utf-8 -*-
"""
This file contains the Emailing logic. Emails will be logged as message in the console for DEV-like environments.
"""

import os
from logging import info, warning

import boto3
from botocore.exceptions import ClientError
import sendgrid
from flask_mail import Message
from sendgrid.helpers.mail import *

from redirectioneaza import app
from redirectioneaza.config import DEV
from redirectioneaza.contact_data import CONTACT_EMAIL_ADDRESS


class EmailManager:
    default_sender = {
        "name": "redirectioneaza",
        "email": CONTACT_EMAIL_ADDRESS
    }

    @staticmethod
    def send_email(**kwargs):
        """
        kwargs:
            receiver        dict
            sender          dict
            subject         String

            text_template
            html_template
        """

        try:

            # in development do not send emails, just log the content
            if DEV:
                text_template = kwargs.get("text_template")
                info(text_template)
                return True

            # send with amazon ses
            response = EmailManager.send_ses_email(**kwargs)

            # if False then the send failed
            if response is False:
                warning('Could not send email with SES')
                return False

            return True

        except Exception as e:

            warning(e)
            return False

    @staticmethod
    def send_ses_email(**kwargs):
        receiver = kwargs.get("receiver")
        sender = kwargs.get("sender", EmailManager.default_sender)
        subject = kwargs.get("subject")

        # create receiver and sender addresses
        receiver = '{} <{}>'.format(receiver['name'], receiver['email'])
        sender = '{} <{}>'.format(sender['name'], sender['email'])

        # email content
        text_template = kwargs.get("text_template")
        html_template = kwargs.get("html_template", "")

        try:
            client = boto3.client(
                'ses',
                region_name=app.config['AWS_REGION'],
                aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
            )

            body = {
                'Text': {
                    'Charset': 'utf-8',
                    'Data': text_template,
                }
            }

            if html_template:
                body['Html'] = {
                    'Charset': 'utf-8',
                    'Data': html_template,
                }

            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        receiver,
                    ],
                },
                Message={
                    'Body': body,
                    'Subject': {
                        'Charset': 'utf-8',
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            return True
