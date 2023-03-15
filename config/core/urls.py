from django.urls import path
from . import views

urlpatterns=[

    path("",views.CityView.as_view(),name="index"),
    path("amlakFilter/",views.handleAmlakFilter,name="amlakFilter"),
    path("handleAmlakFilterSecondLevel/",views.handleAmlakFilterSecondLevel,name="handleAmlakFilterSecondLevel"),
    path("loadMore/",views.load_more,name="loadMore"),
  
    path("<str:name>/",views.CityDetail.as_view(),name="city"),
    path("eachCategory/<str:categoryId>/",views.eachCategory,name="eachCategory"),
    path("eachCategorySecondlevel/<str:categoryId>/",views.eachCategorySecondlevel,name="eachCategorySecondlevel"),
    path("eachCategoryThirdLevel/<str:categoryId>/",views.eachCategoryThirdLevel,name="eachCategoryThirdLevel"),
    path("CommericalDetail/<str:comId>/",views.CommericalDetail.as_view(),name="CommericalDetail"),
    path("createThread/<str:comId>/",views.createThread,name="createThread"),
    path("threadView/<str:threadId>/",views.threadView,name="threadView"),
    
]