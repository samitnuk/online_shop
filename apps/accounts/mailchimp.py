from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash

from django.conf import settings


def get_client():
    return MailChimp(settings.MAILCHIMP_USERNAME,
                     settings.MAILCHIMP_API_KEY, )


def subscribe_user(email_address,
                   list_id=settings.MAILCHIMP_LIST_ID, ):

    client = get_client()
    client.lists.members.create_or_update(
        list_id=list_id,
        subscriber_hash=get_subscriber_hash(email_address),
        data={
            'email_address': email_address,
            'status_if_new': 'subscribed',
        })

    return


def unsubscribe_user(email_address,
                     list_id=settings.MAILCHIMP_LIST_ID, ):

    client = get_client()
    client.lists.members.delete(
        list_id=list_id,
        subscriber_hash=get_subscriber_hash(email_address)
    )

    return


def get_emails_list(list_id=settings.MAILCHIMP_LIST_ID):
    client = get_client()
    members = client.lists.members.all(
        list_id=list_id,
        fields="members.email_address"
    )['members']
    return [member['email_address'] for member in members]
