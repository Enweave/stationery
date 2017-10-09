from django.conf.urls import url

from pages import views as views_pages


urlpatterns = [
    url(r'^каталог/$',
        views_pages.CatalogView.as_view(), name='catalog'),
    url(r'^каталог/(?P<pk>[0-9a-f-]+)/$',
        views_pages.CategoryView.as_view(), name='category'),
    url(r'^товар/(?P<pk>[0-9a-f-]+)/$',
        views_pages.ProductView.as_view(), name='product'),
    url(r'^(?P<slug>[-\w]+)/$',
        views_pages.PageView.as_view(), name='static'),
]
