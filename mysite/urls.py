from django.conf.urls import include, url
from django.contrib import admin
from blog import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^transactions/', views.latesttransaction),
    url(r'^blocks/', views.lastblocks),
    url(r'^transactions1/', views.latesttransaction_tablesorter),
    url(r'^blocks1/', views.lastblocks_tablesorter),
    url(r'^test/', views.test),
    url(r'^test2/', views.test2),
    url(r'^json/', views.jsonreturn),

]
