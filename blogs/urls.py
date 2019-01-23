from blogs import views
from django.conf.urls import url


urlpatterns = [url(r"^$", views.blog, name="blog")]
