
import datetime

from celery import shared_task
from .models import Post, Category

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.shortcuts import render
from .models import *
from NewsPaper import settings

@shared_task
def daily_news_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(article_date__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscibers = Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True)
    html_content = render_to_string(
        'daily_news.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    message = EmailMultiAlternatives(
        subject='Новые публикации',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscibers
    )

    message.attach_alternative(html_content, 'text/html')
    message.send()

@shared_task
def new_post_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            subscribers_emails.append(subscriber.email)

    html_content = render_to_string(
        'new_post.html',
        {
            'username': subscriber.username,
            'preview': post.preview(),
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    message = EmailMultiAlternatives(
        subject='Новая публикация',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails
    )

    message.attach_alternative(html_content, 'text/html')
    message.send()