from django.contrib import admin

# 超级管理员账户：admin 123456
from  blogs import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Kind)
admin.site.register(models.Tag)
admin.site.register(models.Blog)
admin.site.register(models.Comment)
