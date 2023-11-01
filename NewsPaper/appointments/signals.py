
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import PostCategory, Category
from django.conf import settings


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'new_post.html',
        {
            'title': title,
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новая статья уже на сайте',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@receiver(m2m_changed, sender=Category)
def weekly_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.post_category.all()
        subscribers_emails = []
        for category in categories:
            subscribers_emails += category.subscribers.all()

            subscribers_emails = [s.email for s in subscribers_emails]

        send_notifications(instance.preview(), instance.pk, instance.headline, subscribers_emails)