from django.db.models import Count
from django_elasticsearch_dsl_drf.filter_backends import *
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import mixins, viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.utils.pagination import MyPageNumberPagination
from .documents import ArticleDocument, ArticleDraftDocument
from .serialzers import ArticleDocumentSerializer, AddArticleSerializer, CategorySerializer, TagsSerializer, \
    SaveArticleDraftSerializer, ArticleDraftDocumentSerializer, ArchiveSerializer, ArticleInfoSerializer, \
    ArticleOverViewSerializer
from .models import Article, Category, Tags, ArticleDraft, ArticleInfo
import logging

logger = logging.getLogger('mdjango')


class ArticleDocumentView(BaseDocumentViewSet):
    """已发表文章查询视图集"""
    document = ArticleDocument
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArticleDocumentSerializer
    pagination_class = MyPageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend,
    ]
    ordering_fields = {
        'created': 'created'
    }
    ordering = ('-created',)
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        article = Article.objects.get(id=instance.id)
        article.views_num += 1
        article.save()
        try:
            article_info = ArticleInfo.objects.get(id=1)
            article_info.view_num += 1
            article_info.save()
        except Exception as e:
            article_info = ArticleInfo(article_num=0, view_num=1, like_num=0)
            article_info.save()
        return Response(serializer.data)


class ArchiveViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章归档"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArchiveSerializer
    queryset = Article.objects.all()


class HeatMapViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章数量与日期"""
    serializer_class = ArchiveSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('created',)

    def get_queryset(self):
        return Article.objects.values('created').annotate(test=sum('created')).all()


class ArticleOverViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章概览数据"""
    serializer_class = ArticleOverViewSerializer
    permission_classes = ()
    authentication_classes = ()
    queryset = Article.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res = self.get_paginated_response(serializer.data)
            for i in res.data['results']:
                i['like_user'] = len(i['like_user'])
            return res
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddArticleViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """新增文章相关"""
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AddArticleSerializer
    queryset = Article.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        category = serializer.validated_data["category"]
        category.num += 1
        category.save()
        try:
            article_info = ArticleInfo.objects.get(id=1)
            article_info.article_num += 1
            article_info.save()
        except Exception as e:
            article_info = ArticleInfo(article_num=1, view_num=0, like_num=0)
            article_info.save()


class SaveArticleDraftViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """文章草稿箱相关"""
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SaveArticleDraftSerializer
    queryset = ArticleDraft.objects.all()


class ArticleDraftViewSet(BaseDocumentViewSet):
    """草稿查询"""
    document = ArticleDraftDocument
    serializer_class = ArticleDraftDocumentSerializer
    pagination_class = MyPageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        SearchFilterBackend
    ]
    search_fields = ('title', 'content', 'summary', 'category.category', 'tag.tag')


class GetCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """分类管理"""

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GetTagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class TagViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """标签管理"""

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class GetViewAndLikeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取文章总数、浏览总数、点赞总数"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArticleInfoSerializer
    queryset = ArticleInfo.objects.all()


class GetLastYearDataView(APIView):
    """获取最近一年文章数据"""
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        article = Article.objects.count()
        queryset = Article.objects.dates('create', 'day').values('create').annotate(count=Count('id'))
        data = {
            "results": {
                'article': article,
                'date': queryset
            }
        }
        return Response(data, status=status.HTTP_200_OK)
