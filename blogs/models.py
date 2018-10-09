from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.db.models import Count,Min

# Create your models here.


# 用户信息表
class UserInfo(AbstractUser):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    telephone = models.CharField(max_length=18,null=True)
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.jpg')
    blog = models.OneToOneField(to='Blog', to_field='id', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


# 博客表

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=32)
    # 站点名字唯一
    site_name = models.CharField(verbose_name='站点名称', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=20,null=True)

    def __str__(self):
        return self.title



# 标签表
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 分类表
class Kind(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 文章表

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=32)
    desc = models.CharField(verbose_name='文章描述', max_length=150)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    content = models.TextField()
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='id', on_delete=models.CASCADE)
    kind = models.ForeignKey(verbose_name='分类', to='Kind', to_field='id', null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(verbose_name='标签', to='Tag', through='Article2Tag',
                                 through_fields=('article', 'tag'), )

    def __str__(self):
        return self.title

# 文章-标签表
class Article2Tag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='id', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'), ]

    def __str__(self):
        bind = self.article.title + "---" + self.tag.title
        return bind


# 评论表
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='id', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

# 点赞，点踩表
class ArticleUpDown(models.Model):
    id = models.AutoField(primary_key=True)
    is_up = models.BooleanField(default=True)
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


