from django.urls import path
from . import views
from .views import upload_csv
from .views import upload_json


urlpatterns = [
    path('test', views.test),
    path('run', views.run),
    path('run-explain', views.run_explain),
    path('upload_csv', upload_csv, name='upload_csv'),
    path('upload-json', views.upload_json, name='upload_json'),
    path('list-question', views.list_question),
    path('add-question', views.add_question),
    path('modify-question', views.modify_question),
    path('del-question', views.del_question),
    path('list-set', views.list_set),
    path("TestSuiteCreate", views.test_suit_create),
    path("TestSuiteShow", views.test_suit_show),
    path("TestCreate", views.test_create),
    path("TestShow", views.test_show),
    path("config", views.config),
    # path("TaskCreate", views.task_create),
    # path("TaskShow", views.task_show),
    # path("TaskInfo", views.task_info),
    # path("TaskExec", views.task_exec),
    # path("TaskResult", views.task_res),
    # path("TaskDele", views.task_dele),
    
    # path("TestSuiteDele", views.test_suite_dele),
    path("TestDele", views.test_dele),

    
    path("TestExec", views.test_exec),
    path("TestResult", views.test_res),

    path("SetShow1", views.set_show1),
    path("SetShow2", views.set_show2),
    path("SetCreate", views.set_create, name="set_create"),
    path('SetUpdate', views.set_update, name='set_update'),
    path('SetDelete', views.set_delete, name='set_delete'),
    path('UploadSetFile', views.upload_set_file, name='upload_set_file'),

    path("RecentTests", views.recent_tests),
    path("DatasetList", views.dataset_list),
    path("SuiteList", views.suite_list),
    path("TestDetails", views.test_details),
    path("TestStatus", views.test_status),

    path("DownloadTestResult", views.download_test_result, name="download_test_result"),
    path("RandomDataset", views.random_dataset),
    
    path('run-test/', views.run_test, name='run_test'),
    path('download-log/', views.download_log, name='download_log'),
]