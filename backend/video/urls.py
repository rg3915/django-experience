from django.urls import include, path

from backend.video import views as v

app_name = 'video'

v1_urlpatterns = [
    path('videos/', v.videos, name='videos'),
    path('videos/<int:pk>/', v.video, name='video'),
]

urlpatterns = [
    path('api/v1/', include(v1_urlpatterns)),
]
