"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:03
INSTRUCTIONS:   文章序列化
"""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Article, Category, Tags, ArticleDraft


class CategorySerializer(serializers.ModelSerializer):
    """文章分类"""
    category = serializers.CharField(max_length=10, min_length=2, required=True,
                                     validators=[UniqueValidator(queryset=Category.objects.all())])
    num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    """文章标签"""
    tag = serializers.CharField(max_length=10, min_length=2, required=True,
                                validators=[UniqueValidator(queryset=Tags.objects.all())])
    num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tags
        fields = '__all__'


class AddArticleSerializer(serializers.ModelSerializer):
    """新增文章"""
    cover = serializers.CharField(min_length=20, max_length=500, required=True)
    title = serializers.CharField(min_length=2, max_length=50, required=True)
    summary = serializers.CharField(min_length=20, max_length=300, required=True)
    str_num = serializers.IntegerField(required=True)

    class Meta:
        model = Article
        fields = ['summary', 'cover', 'title', 'category', 'tag', 'str_num', 'markdown']


class ArticleContentSerializer(serializers.ModelSerializer):
    """获取文章内容"""
    class Meta:
        model = Article
        fields = ['summary', 'cover', 'title', 'category', 'tag', 'markdown', 'str_num']
        depth = 1


class ArticleOverViewSerializer(serializers.ModelSerializer):
    reading_time = serializers.IntegerField()
    """文章概览"""
    class Meta:
        model = Article
        exclude = ['markdown', 'create']


class SaveArticleDraftSerializer(serializers.ModelSerializer):
    """草稿箱"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ArticleDraft
        fields = ['summary', 'cover', 'title', 'markdown', 'user', 'id', 'category', 'tag']


class ArchiveSerializer(serializers.ModelSerializer):
    """归档相关"""
    class Meta:
        model = Article
        fields = ['title', 'created', 'id', 'category']
        depth = 1


class ArticleCategoryTagsSerializer(serializers.ModelSerializer):
    """获取指定文章的标签与分类"""

    class Meta:
        model = Article
        fields = ['id', 'category', 'tag']
        depth = 1


class ArticleTagSerializer(serializers.ModelSerializer):
    """用户为文章添加标签"""

    class Meta:
        model = Article
        fields = ['tag']