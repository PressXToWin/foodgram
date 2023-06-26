from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
]
