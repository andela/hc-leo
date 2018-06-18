from django.conf.urls import include, url

from hc.help import views

urlpatterns = [
    url(r'^$', views.index, name="hc-faq"),
]
