from django.db import models
from django.contrib.auth.models import AbstractUser


class Github(models.Model):
    """github用户信息"""
    id = models.AutoField(primary_key=True)
    github_id = models.IntegerField(unique=True, verbose_name="githubID")
    avatar = models.CharField(max_length=300, null=True, verbose_name="头像")
    nickname = models.CharField(max_length=50, null=True, verbose_name="昵称")
    homepage = models.URLField(verbose_name='github主页')
    name = models.CharField(max_length=50, null=True, verbose_name='用户昵称')
    company = models.CharField(max_length=50,  null=True, verbose_name='所属公司')
    blog = models.CharField(max_length=100,  null=True, verbose_name='用户blog')
    local = models.CharField(max_length=50,  null=True, verbose_name='地址')
    email = models.EmailField(null=True, verbose_name='邮箱')
    followers = models.IntegerField(verbose_name='关注', default=0, null=True)
    following = models.IntegerField(verbose_name='被关注', default=0, null=True)
    created = models.CharField(max_length=50, null=True, verbose_name='创建时间')
    updated = models.CharField(max_length=50,  null=True, verbose_name='最后更新时间')


class UserProfile(AbstractUser):
    """
    用户信息
    """
    id = models.AutoField(primary_key=True)
    avatar = models.CharField(max_length=300, default='https://avatars1.githubusercontent.com/u/71955670?s=40&v=4',
                              verbose_name="头像")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号")
    github = models.CharField(max_length=50, default="未绑定", verbose_name="github账号")
    github_info = models.ForeignKey(Github, on_delete=models.CASCADE, null=True, verbose_name='github信息')
    is_black = models.BooleanField(default=False, verbose_name='拉黑用户')
    nickname = models.CharField(max_length=10, default='', verbose_name="昵称")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.username



