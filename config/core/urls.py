from django.urls import path
from . import views

urlpatterns=[

    path("",views.CityView.as_view(),name="index"),
    path("allComsFilter/",views.allComsFilter,name="allComsFilter"),
    path("amlakFilter/",views.handleAmlakFilter,name="amlakFilter"),
    path("handleAmlakFilterSecondLevel/",views.handleAmlakFilterSecondLevel,name="handleAmlakFilterSecondLevel"),
    path("handleAmlakFilterSecondLevel/forThird",views.handleAmlakFilterSecondLevel,name="handleAmlakFilterSecondLevel"),
    path("handleFilterThirdLevel/",views.handleFilterThirdLevel,name="handleFilterThirdLevel"),
    path("createThread/<str:comId>/",views.createThread,name="createThread"),


    path("MakeCommerical/",views.MakeCommerical.as_view(),name="MakeCommerical"),
    path("NewCommericalForm/<str:id>/",views.NewCommericalForm.as_view(),name="NewCommericalForm"),
    path("NewCommericalForm/<str:id>/<str:parent_id>/",views.NewCommericalForm.as_view(),name="NewCommericalForm"),

    path("inbox/",views.inbox,name="inbox"),

    path("loadMore/",views.load_more,name="loadMore"),
    path("first/",views.first,name="first"),
    path("second/",views.second,name="second"),
   path("allSearch/",views.search_handle_all,name="allSearch"),
    path("<str:name>/",views.CityDetail.as_view(),name="city"),
    path("eachCategory/<str:categoryId>/",views.eachCategory,name="eachCategory"),
    path("eachCategorySecondlevel/<str:categoryId>/",views.eachCategorySecondlevel,name="eachCategorySecondlevel"),
    path("eachCategoryThirdLevel/<str:categoryId>/",views.eachCategoryThirdLevel,name="eachCategoryThirdLevel"),
    path("CommericalDetail/<str:comId>/",views.CommericalDetail.as_view(),name="CommericalDetail"),

    path("delete_message/<str:threadId>/<str:messageId>/",views.deleteMessage,name="delete_message"),
    path("createThread/<str:comId>/",views.createThread,name="createThread"),
    path("threadView/<str:threadId>/",views.threadView,name="threadView"),
   

    
]