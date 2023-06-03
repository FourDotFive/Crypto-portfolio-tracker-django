from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('user/', include('users.urls'))
]


handler404 = 'portfolio.views.error_404_view'
