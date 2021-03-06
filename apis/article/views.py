import logging
from datetime import date

from django.db.models import Count
from rest_framework import mixins, viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apis.utils.pagination import MyPageNumberPagination
from .serialzers import AddArticleSerializer, CategorySerializer, TagsSerializer, \
    ArticleContentSerializer, ArticleCategoryTagsSerializer, ArticleTagSerializer
from .models import Article, Category, Tags, ArticleDraft
from apis.utils.utils.other import redis_handle
from main.settings import REDIS_PREFIX, COUNT_PREFIX
from .tasks import send_mails
from ..operations.models import Subscribe

logger = logging.getLogger('django_log')

like_view_parm = [openapi.Parameter(name='user_id', in_=openapi.IN_QUERY, description='用户ID', type=openapi.TYPE_NUMBER),
                  openapi.Parameter(name='article_id', in_=openapi.IN_QUERY, description="文章ID", type=openapi.TYPE_NUMBER)]

tag_param = [openapi.Parameter(name='tag', in_=openapi.IN_QUERY, description="标签名称", type=openapi.TYPE_STRING)]





class AddArticleViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """新增文章相关"""
    permission_classes = (permissions.IsAdminUser,)
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            return ArticleContentSerializer
        return AddArticleSerializer

    def perform_create(self, serializer):
        serializer.save()
        send_mails.delay(theme='订阅通知', title=serializer.instance.title, url='http://blog.messstack.com/detail/' +
                         str(serializer.instance.id) + '/')
        category = serializer.validated_data["category"]
        category.num += 1
        category.save()
        redis_handle.incr(REDIS_PREFIX + "total_article", amount=1)
        tag = serializer.validated_data['tag']
        for i in tag:
            redis_handle.hincrby(COUNT_PREFIX + 'tag', i.tag, amount=1)

    def perform_update(self, serializer):
        serializer.save()
        tag = serializer.validated_data.get('tag', '')
        if tag:
            for i in tag:
                redis_handle.hincrby(COUNT_PREFIX + 'tag', i.tag, amount=1)

class GetCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """获取分类"""
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
    """获取标签"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class TagViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """标签管理"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        redis_handle.hset(COUNT_PREFIX + 'tag', serializer.validated_data['tag'], 0)


class GetViewAndLikeView(APIView):
    """获取文章总数、浏览总数、点赞总数"""
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            total_like = redis_handle.get(REDIS_PREFIX + "total_like")
            total_article = redis_handle.get(REDIS_PREFIX + "total_article")
            total_view = redis_handle.get(REDIS_PREFIX + "total_view")
            data = {'total_like': total_like, "total_article": total_article, "total_view": total_view}
        except Exception as e:
            return Response({"data": str(e.args)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


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


class LikeView(APIView):
    """文章点赞相关"""
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(operation_description='获取文章点赞数', manual_parameters=like_view_parm)
    def get(self, request, *args, **kwargs):
        """获取所有点赞数或指定文章的点赞数"""
        article_id = request.query_params.get('article_id', '')
        user_id = request.query_params.get('user_id', '')
        article_name = "article_like:" + str(article_id)
        view_name = "view:" + str(article_id)
        try:
            if article_id and user_id:
                article_like = redis_handle.zcard(REDIS_PREFIX + article_name)
                comment = redis_handle.get(REDIS_PREFIX + 'article_comment:' + str(article_id))
                comment = comment if comment else 0
                view = redis_handle.get(REDIS_PREFIX + view_name)
                view = view if view else 0
                flag = redis_handle.zrank(REDIS_PREFIX + article_name, user_id)
                data = {"total": article_like, 'view': view, "flag": flag, 'comment': comment}
            elif article_id:
                article_like = redis_handle.zcard(REDIS_PREFIX + article_name)
                view = redis_handle.get(REDIS_PREFIX + view_name)
                comment = redis_handle.get(REDIS_PREFIX + 'article_comment:' + str(article_id))
                comment = comment if comment else 0
                data = {"total": article_like, 'view': view,  'comment': comment}
            else:
                total_like = redis_handle.get(REDIS_PREFIX + "total_like")
                data = {"total": total_like}
        except Exception as e:
            return Response({'data': '数据查询失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


class ArticleCategoryTagViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """获取指定文章的分类和标签"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArticleCategoryTagsSerializer
    queryset = Article.objects.all()


class ArticleUpdateTagViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """更新文章的标签"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ArticleTagSerializer
    queryset = Article.objects.all()

    def perform_update(self, serializer):
        serializer.save()
        tag = serializer.validated_data.get('tag', '')
        if tag:
            redis_handle.hincrby(COUNT_PREFIX + 'tag', tag[-1].tag, amount=1)


class CheckTagExistView(APIView):
    """判断标签是否已经存在"""
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(operation_description='查询标签是否存在', manual_parameters=tag_param)
    def get(self, request, *args, **kwargs):
        tag_name = request.query_params.get('tag', '')
        if tag_name:
            tag = Tags.objects.filter(tag=tag_name).first()
            if not tag:
                tag = Tags(tag=tag_name)
                tag.save()
                redis_handle.hset(COUNT_PREFIX + 'tag', tag_name, 0)
            return Response({'results': tag.id}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_400_BAD_REQUEST)