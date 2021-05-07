from django.urls import path, re_path
from caseManage.views import fileviews,testcaseviews,userviews

urlpatterns = [
    path('upload/', fileviews.upload),
    path('download/', fileviews.download),
    path('index/', testcaseviews.getAllCases),
    path('fileall/', fileviews.getAllFiles),
    re_path('students/(\d+)/', testcaseviews.students)
]