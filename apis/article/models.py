import math

from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

user = get_user_model()


class Category(models.Model):
    """文章分类"""
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=10, null=False, unique=True, verbose_name="分类")
    num = models.IntegerField(default=0, verbose_name="文章数")

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['id']


class Tags(models.Model):
    """文章标签"""
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=5, unique=True, verbose_name="标签")
    num = models.IntegerField(default=0)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['id']


class Article(models.Model):
    """已发布文章"""
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="article", verbose_name="文章分类")
    tag = models.ManyToManyField("Tags", related_name="article",  verbose_name='文章标签')
    title = models.CharField(max_length=100, verbose_name='文章标题')
    cover = models.CharField(max_length=255, verbose_name='文章封面')
    summary = models.TextField(verbose_name="文章简介")
    markdown = models.TextField(verbose_name='markdown')
    created = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    create = models.DateField(default=datetime.now, verbose_name="创建日期")
    str_num = models.IntegerField(default=0, verbose_name="文章字数")
    comments_num = models.IntegerField(default=0, verbose_name="评论数量")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    @property
    def reading_time(self):
        return math.ceil(self.str_num/600)


class ArticleDraft(models.Model):
    """文章草稿箱"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True, related_name="draft", verbose_name='用户信息')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="draft",
                                 verbose_name="文章分类")
    tag = models.ManyToManyField("Tags", related_name="draft", blank=True, verbose_name='文章标签')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='文章标题')
    cover = models.CharField(max_length=255, null=True, blank=True, verbose_name='文章封面')
    summary = models.TextField(null=True, blank=True, verbose_name="文章简介")
    markdown = models.TextField(null=True,  blank=True, verbose_name='文章内容')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
