from django.urls import path
from . import views

urlpatterns=[

    path("",views.CityView.as_view(),name="index"),
    path("allComsFilter/",views.allComsFilter,name="allComsFilter"),
    path("amlakFilter/",views.handleAmlakFilter,name="amlakFilter"),
    path("handleAmlakFilterSecondLevel/",views.handleAmlakFilterSecondLevel,name="handleAmlakFilterSecondLevel"),
    path("handleAmlakFilterSecondLevel/forThird",views.handleAmlakFilterSecondLevel,name="handleAmlakFilterSecondLevel"),
    path("handleFilterThirdLevel/",views.handleFilterThirdLevel,name="handleFilterThirdLevel"),
    path("loadMore/",views.load_more,name="loadMore"),
    path("first/",views.first,name="first"),
    path("second/",views.second,name="second"),
  
    path("<str:name>/",views.CityDetail.as_view(),name="city"),
    path("eachCategory/<str:categoryId>/",views.eachCategory,name="eachCategory"),
    path("eachCategorySecondlevel/<str:categoryId>/",views.eachCategorySecondlevel,name="eachCategorySecondlevel"),
    path("eachCategoryThirdLevel/<str:categoryId>/",views.eachCategoryThirdLevel,name="eachCategoryThirdLevel"),
    path("CommericalDetail/<str:comId>/",views.CommericalDetail.as_view(),name="CommericalDetail"),
    path("createThread/<str:comId>/",views.createThread,name="createThread"),
    path("threadView/<str:threadId>/",views.threadView,name="threadView"),
    
]