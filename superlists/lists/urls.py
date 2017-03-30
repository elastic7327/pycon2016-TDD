from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # url(r'lists/(\d+)/$', 'lists.views.view_list', name='view_list'),
    # url(r'lists/(\d+)/add_item/$', 'lists.views.add_item', name='add_item'),
    # url(r'lists/(\d+)/add_item/$', 'lists.views.add_item', name='add_item'),
    url(r'(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'(\d+)/add_item/$', 'lists.views.add_item', name='add_item'),
    url(r'new$', 'lists.views.new_list', name='new_list'),
]
