from django.urls import path, re_path
from caseManage.views import fileviews,testcaseviews,userviews

urlpatterns = [
    path('upload/', fileviews.upload),
    # path('download/', fileviews.download),
    path('index/', testcaseviews.getAllCases),
    path('uploadcase/', testcaseviews.uploadCase),
    path('updatecase/', testcaseviews.updateCase),
    path('delcase/', testcaseviews.delCase),
    path('delfilecase/', fileviews.delfileCase, name='delfileCase'),
    path('downfile/', fileviews.downFile, name='downFile'),
    path('downcase/', testcaseviews.downcases, name='downcases'),
    re_path('fileall/(\d+)/', fileviews.getAllFiles),
    re_path('students/(\d+)/', testcaseviews.students),
    re_path('teachers/(\d+)/', testcaseviews.teachers),
    re_path('learns/(\d+)/', testcaseviews.learns),
    re_path('questions/(\d+)/', testcaseviews.questions),
    re_path('princpals/(\d+)/', testcaseviews.princpals),
    re_path('others/(\d+)/', testcaseviews.others),
    re_path('search/(\d+)/', testcaseviews.searchcase)
]