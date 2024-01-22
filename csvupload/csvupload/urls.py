"""csvupload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


# csvapp/urls.py
from django.urls import path
from csvapp.views import get_data, data_table, file_list, file_detail, file_upload, file_edit, file_delete, \
    process_selected_files, clear_all_documents, DataTableView,get_data_json,datatable_example,datatable_example1, \
    get_data_json1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('file_list/', file_list, name='file_list'),
    path('file_detail/<int:pk>/', file_detail, name='file_detail'),
    path('file_upload/', file_upload, name='file_upload'),
    path('file_edit/<int:pk>/', file_edit, name='file_edit'),
    path('file_delete/<int:pk>/', file_delete, name='file_delete'),
    path('process_selected_files/', process_selected_files, name='process_selected_files'),
    path('clear_all_documents/', clear_all_documents, name='clear_all_documents'),
    path('get_data/', get_data, name='get_data'),
    path('data_table/', data_table, name='data_table'),
    path('data_table_view/', DataTableView.as_view(), name='data_table_view'),
    path('get_data_json/', get_data_json, name='get_data_json'),
    path('get_data_json1/', get_data_json1, name='get_data_json1'),
    path('datatable/', datatable_example, name='datatable_example'),
    path('datatable1/', datatable_example1, name='datatable_example'),
    # Add other URL patterns as needed
]
