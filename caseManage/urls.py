from django.urls import path
from caseManage.views import fileviews,testcaseviews,userviews

urlpatterns = [
    path('upload/', fileviews.upload),
    path('download/', fileviews.download),
    path('index/', testcaseviews.getAllCases),
    path('fileall/', fileviews.getAllFiles)
]