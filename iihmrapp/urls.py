from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('web_login',views.web_login,name = 'web_login'),
    path('admin_raw_data_download',views.admin_raw_data_download,name = 'admin_raw_data_download'),
    path('admin_IIHMR_mobile_apk_upload',views.admin_IIHMR_mobile_apk_upload,name = 'admin_IIHMR_mobile_apk_upload'),
    
]