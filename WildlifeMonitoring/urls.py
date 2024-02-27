from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include

app_name = 'single'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',include('single.urls',namespace='single'))
]

