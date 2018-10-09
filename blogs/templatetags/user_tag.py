from blogs.models import *
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django import template

register =template.Library()

@register.inclusion_tag('classification.html')
def get_param(username):
    username = UserInfo.objects.filter(username=username).first()
    if username:
        article_list = Article.objects.filter(user=username)
        # 子查询
        blog = username.blog
        kind_query = Kind.objects.filter(blog=blog).values('title').annotate(c=Count('id'))
        tag_query = Tag.objects.filter(blog=blog).values('title').annotate(c=Count('id'))

        date_list=Article.objects.filter(user=username).annotate(month=TruncMonth("create_time")).values("month").\
            annotate(c=Count("id")).values_list("month","c")
    return locals()