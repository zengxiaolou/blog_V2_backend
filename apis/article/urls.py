"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:20
INSTRUCTIONS:   文件简介
"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ArticleDocumentView, AddArticleViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()

router.register('search', ArticleDocumentView, basename='search')
router.register('category', CategoryViewSet, basename='category')
router.register('tag', TagViewSet, basename='tag')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^add/$', AddArticleViewSet.as_view()),
]