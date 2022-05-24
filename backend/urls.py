from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('backend.core.urls', namespace='core')),
    path('', include('backend.bookstore.urls', namespace='bookstore')),
    path('', include('backend.crm.urls', namespace='crm')),
    path('', include('backend.persona.urls', namespace='persona')),
    path('', include('backend.example.urls', namespace='example')),
    path('', include('backend.expense.urls', namespace='expense')),
    path('', include('backend.hotel.urls', namespace='hotel')),
    path('', include('backend.movie.urls', namespace='movie')),
    path('', include('backend.school.urls', namespace='school')),
    path('', include('backend.todo.urls', namespace='todo')),
    path('', include('backend.video.urls', namespace='video')),
    path('admin/', admin.site.urls),
]

# djoser
urlpatterns += [
    path('api/v1/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
]

# swagger
urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa E501
]
