"""
AUTHOR:         zeng_xiao_yu
GITHUB:         https://github.com/zengxiaolou
EMAIL:          zengevent@gmail.com
TIME:           2020/8/24-18:20
INSTRUCTIONS:   文件简介
"""

from django.conf.urls import url, include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import AddArticleViewSet, CategoryViewSet, TagViewSet, GetTagViewSet, GetCategoryViewSet,\
    GetViewAndLikeView, GetLastYearDataView, LikeView, ArticleCategoryTagViewSet, ArticleUpdateTagViewSet, \
    CheckTagExistView
app_name = "article"
router = DefaultRouter()

router.register('category', CategoryViewSet, basename='category')
router.register('get/category', GetCategoryViewSet, basename='/get/category')
router.register('get/tag', GetTagViewSet, basename='get/tag')
router.register('tag', TagViewSet, basename='tag')
router.register('article', AddArticleViewSet, basename='article')
router.register('category-tag', ArticleCategoryTagViewSet, basename='category-tag')
router.register('article/tag', ArticleUpdateTagViewSet, basename='article/tag')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^last-data/$', GetLastYearDataView.as_view()),
    url(r"^like/$", LikeView.as_view()),
    path("info/", GetViewAndLikeView.as_view(), name="info"),
    url(r"^check-tag/$", CheckTagExistView.as_view())
]
