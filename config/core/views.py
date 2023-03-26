from django.shortcuts import render,get_object_or_404,redirect
from .models import (Commerical,SavedCommerical,
                    SmallCity,City,Thread,Message,
                    Feature,Tag,Location
                    )
from django.contrib import messages
from django.views import View
from django.views.generic import ListView,UpdateView,DetailView
from django.db.models import Q,F
from django.db.models.functions import Length
from datetime import datetime
from jalali_date import datetime2jalali
from django.utils import timezone


from .utilty import    (findTimeDiffrence,title_not_to_be,
three_level_parent,
two_level_parent,
two_and_three_parent,
apartemanForosh,
immadate_location_image,
price_Title,
moavezeh,GroupHasYearOfConstruction,
GroupHasPrice,GroupHasMeter,GroupHasExchangePossibale,
GroupHasCommericalSituation_like_new_or_old,Group_Employments,
typeOneForSecondLevelFilter_Amlak_Frosh,amlakEjareh,vasayelNaghliehMotor_va_Car,
vasayelNaghlieh_Both_and_supplies,digitals,kitchen,personal,digitalOrKitchenOrPersonalOrEntertaimentOrSupllies,
services,foroshJustForSanadEdari,ejarehAll,cars,tablet_and_mobile,
themSelf,male_or_female,social,employment
                     )

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core import serializers

from .utils2 import (
    groupHas_Parking_And_Anbari_And_Floor,groupHas_sanadEdari,
    cloths_accessory

)


def lcoationIdsssss():
    return [i.id for i in Location.objects.all()]
    





class CityView(View):
    
    
    def get(self,request,*args,**kwargs):

        all_citites=City.objects.all()
        
        # if self.request.session.get("city_name2",None):
        #     del self.request.session["city_name2"]
        ls=self.request.GET.getlist("items")
        big=self.request.GET.getlist("bigCity")
        self.request.session["bb"]=big
        self.request.session["min"]=ls
        print("BEFFOORREEE")
        print("BEFFOORREEE")
        print("BEFFOORREEE")
        print(self.request.GET)
        print("AFTTTERRRR")
        print("AFTTTERRRR")
        bigInJson=[int(i) for i in big]

        ci=City.objects.filter(id__in=bigInJson)

        
    

        filtred_coms=None
        if big and ls:

            filtred_coms=Commerical.objects.filter(
            Q(city__in=bigInJson) | Q(smallCity__in=ls)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
            print("OONNNEEe")
        else:
            filtred_coms=Commerical.objects.filter(
                Q(city__in=bigInJson) 
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).distinct()
            print("TWOOWOOWOWOOWOW")
         
        all_cats=Commerical.objects.filter(
            parent=None
        )

        print(filtred_coms,"FFFIILLFLFLFLLFLFL")

        cits=City.objects.filter(
            id__in=[int(i) for i in big]
        )


        contex={

            'cities':ci,
            'coms':filtred_coms,
            'all_cats':all_cats,
            'cits':cits
            
        }
      
        
        return render(request,"core/after_search_city.html",contex)

    def post(self,request,*args,**kwargs):

        ls=self.request.POST.getlist("items")
        big=self.request.POST.getlist("bigCity")
        self.request.session["bb"]=big
        self.request.session["min"]=ls
        
       
        bigInJson=[int(i) for i in big]

        ci=City.objects.filter(id__in=bigInJson)

        
    

        filtred_coms=None
        if big and ls:

            filtred_coms=Commerical.objects.filter(
            Q(city__in=bigInJson) | Q(smallCity__in=ls)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()[:4]
            print("OONNNEEe")
        else:
            filtred_coms=Commerical.objects.filter(
                Q(city__in=bigInJson) 
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).distinct()[:4]
            print("TWOOWOOWOWOOWOW")
         
        all_cats=Commerical.objects.filter(
            parent=None
        )

        contex={

            'cities':ci,
            'coms':filtred_coms,
            'all_cats':all_cats,
            
        }
      
        
        return render(request,"core/after_search_city.html",contex)
    


def allComsFilter(request):

    province=request.session.get("bb")
    smallCities=request.session.get("min")

    defaultLocalIds=[]

    cities=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    for c in cities:
        for loc in c.location_set.all():
            defaultLocalIds.append(loc.id)
    all_cats=Commerical.objects.filter(
            parent=None
        )

    locationIds=request.GET.get("ids")
    justImg=request.GET.get("justImg",False)
    instatnceComs=request.GET.get("instatnceComs","عادی")


    

    least_price=request.GET.get("least_price",0)
    max_price=request.GET.get("max_price",400000000)

    locas_to_go=list(map(

            lambda x:int(x),locationIds.split(",")
            if len(locationIds)>=1 else defaultLocalIds
        ))
  

    coms_to_show=None

    if province and smallCities:
            print("A")
            if bool(justImg):


                coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                ).filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities]) 
                            

                    ).filter(
                        # Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(int(least_price),int(max_price))) |
                        Q(vadieh__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        img_length__gte=1
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()
            else:
                print("ELELLELELLSSSSSEEe")
                coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities])         
                    ).filter(
                        # Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(least_price,max_price))|
                        Q(vadieh__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()


    elif province and not smallCities:

            print("B")

            if bool(justImg):
                coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                ).filter(
                    Q(city__in=[int(i) for i in province]) &
                    # Q(parent__parent__parent__title="املاک") &
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(least_price,max_price))|
                    Q(vadieh__range=(int(least_price),int(max_price)))
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).filter(
                        img_length__gte=1
                ).filter(
                        com_status=instatnceComs
                    ).distinct()
            else:
                coms_to_show=Commerical.objects.filter(
                    Q(city__in=[int(i) for i in province]) &
                    Q(parent__parent__parent__title="املاک") &
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(least_price,max_price))|
                    Q(vadieh__range=(int(least_price),int(max_price)))
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).filter(
                        com_status=instatnceComs
                    ).distinct()


    elif not province and smallCities:
            print("C")

            if bool(justImg):
                coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                ).filter(
                    Q(smallCity__in=[int(i) for i in smallCities])&
                    # Q(parent__parent__parent__title="املاک") &
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(least_price,max_price))|
                    Q(vadieh__range=(int(least_price),int(max_price)))
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).filter(
                        img_length__gte=1
                ).filter(
                        com_status=instatnceComs
                    ).distinct()
            else:
                coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        # Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(least_price,max_price))|
                        Q(vadieh__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()

    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    for i in cits:
        for l in i.location_set.all():
            if l.id in locas_to_go :
                print("yese","********************************")
            else:
                print("NONONONOONONON")
    

 
    contex={
       
        'coms':coms_to_show,
        'cits':cits,
        'justImg':bool(justImg),
        'instatnceComs':instatnceComs,
        'least_price':int(least_price),
        'max_price':int(max_price),
        'all_cats':all_cats,
        'locas_to_go':locas_to_go
        
    }
    return render(request,"core/allComsFilter.html",contex)



def eachCategory(request,categoryId):

    cat=get_object_or_404(Commerical,id=categoryId)
    

    cat_childs=cat.children.all()

    province=request.session.get("bb")
    smallCities=request.session.get("min")

      

    coms_to_show=None
    
    if cat.title in three_level_parent:

        if province and smallCities:


            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) |
                Q(smallCity__in=[int(i) for i in smallCities]) 
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).filter(
                Q(parent__parent__parent__title=cat.title)
            ).distinct()




        elif province and not smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
                
            ).filter(
                Q(parent__parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
        
        
        
        elif not province and smallCities:
            coms_to_show=Commerical.objects.filter(
                Q(smallCity__in=[int(i) for i in smallCities])
                 
            ).filter(
                Q(parent__parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
            
    elif cat.title in two_level_parent:

        if province and smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province])|
                Q(smallCity__in=[int(i) for i in smallCities]) 
                

            ).filter(
                Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
        elif province and not smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
                
            ).filter(
                Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
        elif not province and smallCities:
            coms_to_show=Commerical.objects.filter(
                Q(smallCity__in=[int(i) for i in smallCities])
               
            ).filter(
                 Q(parent__parent__title=cat.title) 
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()


    elif cat.title in two_and_three_parent:
        print("HEEHERERE CALLEDDD")
        if province and smallCities:
            print("AFTTERRR HERERRERREER")

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) | 
                Q(smallCity__in=[int(i) for i in smallCities]) 
                

            ).filter(
                Q(parent__parent__parent__title=cat.title) | Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
        elif province and not smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
                
            ).filter(
                Q(parent__parent__parent__title=cat.title) | Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
        elif not province and smallCities:
            coms_to_show=Commerical.objects.filter(
                Q(smallCity__in=[int(i) for i in smallCities])
                
            ).filter(
                Q(parent__parent__parent__title=cat.title) | Q(parent__parent__title=cat.title) 
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()



    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )


    contex={

        'cat_childs':cat_childs,
        'coms_to_show':coms_to_show,
        'cat':cat,
        'cits':cits,
        'immadate_location_image':immadate_location_image,
        'price_Title':price_Title,
        'moavezeh':moavezeh
    }

    return render(request,"core/eachCategory.html",contex)





def eachCategorySecondlevel(request,categoryId):

    cat=get_object_or_404(Commerical,id=categoryId)

    cat_childs=cat.children.all()
    print(cat_childs,"CCCHHILLDLDLDLLDLDLDLDLDLDLDLDLDLd")
    province=request.session.get("bb")
    smallCities=request.session.get("min")
    coms_to_show=None

    if cat.parent.title in three_level_parent:
        if province and smallCities:
            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) | 
                Q(smallCity__in=[int(i) for i in smallCities]) 
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.title) & Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

        elif province and not smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.title) &
                Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
        elif not province and smallCities:

            coms_to_show=Commerical.objects.filter(

                Q(smallCity__in=[int(i) for i in smallCities])
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.title) & 
                Q(parent__parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

    elif cat.parent.title in two_level_parent:
        print("SECONND TOUCHHED")
        if province and smallCities:
            print("FFFNNNNN")

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) | 
                Q(smallCity__in=[int(i) for i in smallCities]) 
            ).filter(
                 Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

        elif province and not smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
            ).filter(
                
                Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

        elif not province and smallCities:

            coms_to_show=Commerical.objects.filter(
                
                Q(smallCity__in=[int(i) for i in smallCities])
            ).filter(
                Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

    else:
        print("THIRS TOHHECCC")
        first_chat_child=cat.children.first()
        if first_chat_child.children.all():

                if province and smallCities:

                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities]) 
                        

                    ).filter(
                        Q(parent__parent__parent__title=cat.parent.title) &
                        Q(parent__parent__title=cat.title)
                    ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).distinct()
                    
                elif province and not smallCities:

                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) 
                        
                    ).filter(
                        Q(parent__parent__parent__title=cat.parent.title) &
                        Q(parent__parent__title=cat.title)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).distinct()

                elif not province and smallCities:
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])
                        
                    ).filter(
                        Q(parent__parent__parent__title=cat.parent.title) &
                        Q(parent__parent__title=cat.title)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).distinct()
        else:
                
                if province and smallCities:

                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities]) 
                        

                    ).filter(
                        Q(parent__parent__title=cat.parent.title) &
                        Q(parent__title=cat.title)
                    ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).distinct()
                    
                elif province and not smallCities:

                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) 
                        
                    ).filter(
                        Q(parent__parent__title=cat.parent.title) &
                        Q(parent__title=cat.title)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).distinct()

                elif not province and smallCities:
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])
                        
                    ).filter(
                        Q(parent__parent__title=cat.parent.title) &
                        Q(parent__title=cat.title)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).distinct()

    print("$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$")
    print(coms_to_show)
    print("$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$")

    

    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )

    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
        'cits':cits,
        'coms_to_show':coms_to_show,
        'GroupHasPrice':GroupHasPrice,
        'GroupHasMeter':GroupHasMeter,
        'GroupHasYearOfConstruction':GroupHasYearOfConstruction,
        'GroupHasExchangePossibale':GroupHasExchangePossibale,
        'GroupHasCommericalSituation_like_new_or_old':GroupHasCommericalSituation_like_new_or_old,
        'Group_Employments':Group_Employments
    }



    return render(request,"core/eachCategorySecondlevel.html",contex)





def eachCategoryThirdLevel(request,categoryId):

    cat=get_object_or_404(Commerical,id=categoryId)

    cat_childs=cat.children.all()
    province=request.session.get("bb")
    smallCities=request.session.get("min")
    coms_to_show=None

    if province and smallCities:
            print("noooooooooooooooooooooooooooooooo")
            print("noooooooooooooooooooooooooooooooo")
            print("noooooooooooooooooooooooooooooooo")
            print("noooooooooooooooooooooooooooooooo")

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) | 
                Q(smallCity__in=[int(i) for i in smallCities]) 
               

            ).filter(
                 Q(parent__parent__parent__title=cat.parent.parent.title) &
                Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

    elif province and not smallCities:

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.parent.title) &
                Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
    elif not province and smallCities:

            coms_to_show=Commerical.objects.filter(

                Q(smallCity__in=[int(i) for i in smallCities])
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.parent.title) &
                Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    

    contex={
        'cits':cits,
        'cat_childs':cat_childs,
        'catMain':cat,
        'coms_to_show':coms_to_show,
        'GroupHasPrice':GroupHasPrice,
        'GroupHasMeter':GroupHasMeter,
        'GroupHasYearOfConstruction':GroupHasYearOfConstruction,
        'GroupHasExchangePossibale':GroupHasExchangePossibale,
        'GroupHasCommericalSituation_like_new_or_old':GroupHasCommericalSituation_like_new_or_old,
        'Group_Employments':Group_Employments,
        'groupHas_Parking_And_Anbari_And_Floor':groupHas_Parking_And_Anbari_And_Floor,
        'groupHas_sanadEdari':groupHas_sanadEdari,
        'cloths_accessory':cloths_accessory
    }



    return render(request,"core/eachCategoryThirdLevel.html",contex)



class CityDetail(View):

    template_name="core/each_city.html"

    def get(self,request,name,*args,**kwargs):
        
        name=self.kwargs.get("name")
        

        city=get_object_or_404(City,name=name) 
        self.request.session["city_name2"]=city.id
        coms=city.commerical_set.all()

        contex={
            'city':city,
            'coms':coms
        }

        return render(request,"core/each_city.html",contex)
        
    
    



def testPost(request):
    print("$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$")
    print(type(request.GET.get("ids")))
    print("$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$")

  

    return render(request,"core/tt.html")




def handleAmlakFilter(request):



    province=request.session.get("bb")
    smallCities=request.session.get("min")


    defaultLocalIds=[]

    cities=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    for c in cities:
        for loc in c.location_set.all():
            defaultLocalIds.append(loc.id)
        

    locationIds=request.GET.get("ids")
    justImg=request.GET.get("justImg",False)
    instatnceComs=request.GET.get("instatnceComs","عادی")

 

    

    least_price=request.GET.get("least_price",0)
    max_price=request.GET.get("max_price",400000000)
    title=request.GET.get("catTitle")
    publisher=request.GET.get("publisher","همه")
    exchange=request.GET.get("exchange",False)
    publisherForCar=request.GET.get("publisherForCar","همه")
    phoneStatus=request.GET.get("phoneStatus","همه")
    choose_min_price_for_work=request.GET.get("choose_min_price_for_work",0)
    choose_max_price_for_work=request.GET.get("choose_max_price_for_work",20)
    farWork=request.GET.get("farWork",False)
    soldier=request.GET.get("soldier",False)


    
    publisher=publisher if len(publisher)>0 else "همه"

    locas_to_go=list(map(

            lambda x:int(x),locationIds.split(",")
            if len(locationIds)>=1 else defaultLocalIds
        ))

    coms_to_show=None



    match title:
        case "املاک":
            if province and smallCities:
                print("A")
                if bool(justImg):


                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                

                        ).filter(
                            Q(parent__parent__parent__title="املاک") &
                            Q(location__in=locas_to_go)&
                            Q(publisher=publisher)

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities])         
                    ).filter(
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)&
                        Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)&
                        Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                    Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)&
                        Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)&
                        Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)&
                        Q(publisher=publisher)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()

        case "وسایل نقلیه":

            if province and smallCities:
                print("A")
                if bool(justImg):
                    if exchange:


                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                     Q(parent__parent__parent__title="وسایل نقلیه")|
                                     Q(parent__parent__title="وسایل نقلیه")
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:

                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(publisherForCar=publisherForCar)
                                ).filter(
                                    Q(parent__parent__parent__title="وسایل نقلیه")|
                                    Q(parent__parent__title="وسایل نقلیه")
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    if exchange:
                        coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities])         
                            ).filter(
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(publisherForCar=publisherForCar)&
                            Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    else:

                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                            ).filter(
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if exchange:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(publisherForCar=publisherForCar)&
                            Q(ready_to_exchange=True)
                        ).filter(
                            Q(parent__parent__parent__title="وسایل نقلیه")|
                            Q(parent__parent__title="وسایل نقلیه")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(publisherForCar=publisherForCar)
                          
                        ).filter(
                            Q(parent__parent__parent__title="وسایل نقلیه")|
                            Q(parent__parent__title="وسایل نقلیه")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                            
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &   
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:


                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()


        case "کالای دیجیتال":
            if province and smallCities:
                print("A")
                if bool(justImg):
 
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(phone_status=phoneStatus)
                                    
                                ).filter(
                                     Q(parent__parent__parent__title="کالای دیجیتال")|
                                     Q(parent__parent__title="کالای دیجیتال")
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities])         
                        ).filter(
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                   
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
     
                else:

                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    


                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(phone_status=phoneStatus)

                            ).filter(
                                 Q(parent__parent__parent__title="کالای دیجیتال")|
                                 Q(parent__parent__title="کالای دیجیتال")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
  
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()


        case "تجهیزات و صنعتی" | "سرگرمی و فراغت" | "خانه و آشپزخانه" :
            if province and smallCities:
                print("A")
                if bool(justImg):
 
                        if exchange:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)
                                    
                                ).filter(
                                    Q(parent__parent__parent__title=title)|
                                    Q(parent__parent__title=title)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                    
                                ).filter(
                                    Q(parent__parent__parent__title=title)|
                                    Q(parent__parent__title=title)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                            ).filter(
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                            ).filter(
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if exchange:

                   
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(ready_to_exchange=True)
                        ).filter(
                            Q(parent__parent__parent__title=title)|
                            Q(parent__parent__title=title)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))  
                        ).filter(
                            Q(parent__parent__parent__title=title)|
                            Q(parent__parent__title=title)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
     
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) &
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) & 
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:

                    


                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)

                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
  
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(parent__parent__parent__title=title)|
                                Q(parent__parent__title=title)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

        case "اجتماعی":
            if province and smallCities:
                print("A")
                if bool(justImg):
 
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__parent__parent__title="اجتماعی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(least_price),int(max_price)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities])         
                        ).filter(
                            Q(parent__parent__parent__title="اجتماعی") &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                   
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__parent__parent__title="اجتماعی") &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
     
                else:

                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                            Q(parent__parent__parent__title="اجتماعی") &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    


                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__parent__title="اجتماعی") &
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))


                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
  
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__parent__title="اجتماعی") &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()


        case "استخدام و کاریابی":

            if province and smallCities:
                print("A")
                if bool(justImg):
 
                        if farWork:
                            if soldier:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__parent__title="استخدام و کاریابی") &
                                        Q(location__in=locas_to_go)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                        Q(soldier=True)&
                                        Q(farWork=True)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__parent__title="استخدام و کاریابی") &
                                        Q(location__in=locas_to_go)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                        Q(farWork=True)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                        else:
                            if soldier:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__parent__title="استخدام و کاریابی") &
                                        Q(location__in=locas_to_go)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                        Q(soldier=True)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__parent__title="استخدام و کاریابی") &
                                        Q(location__in=locas_to_go)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()


                else:
                    print("ELELLELELLSSSSSEEe")
                    if farWork:
                        if soldier:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                                ).filter(
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)&
                                    Q(soldier=True)
                                ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                                ).filter(
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)
                                ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                    else:


                        if soldier:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                                ).filter(
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                  
                                    Q(soldier=True)
                                ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                                ).filter(
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                   
                        if farWork:
                            if soldier:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)&
                                    Q(soldier=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        else:

                            if soldier:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(soldier=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

     
                else:
                    if farWork:
                        if soldier:


                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)&
                                    Q(soldier=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    else:

                        if soldier:


                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                               
                                    Q(soldier=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    
                    if farWork:
                        if soldier:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)&
                                    Q(soldier=True)


                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                                    Q(farWork=True)


                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    else:

                        if soldier:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))&
                            
                                    Q(soldier=True)


                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))


                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()


                else:
                    if farWork:
                        if soldier:

                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_min_price_for_work)))&
                                    Q(soldier=True)&
                                    Q(farWork=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_min_price_for_work)))&
                                    Q(farWork=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:

                        if soldier:

                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_min_price_for_work)))&
                                    Q(soldier=True)
                                

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__parent__title="استخدام و کاریابی") &
                                    Q(location__in=locas_to_go)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_min_price_for_work)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


    cat=get_object_or_404(Commerical,title=title)
    cat_childs=cat.children.all()
    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )

    contex={
        'cat_childs':cat_childs,
        'cat':cat,
        'coms_to_show':coms_to_show,
        'cits':cits,
        'justImg':bool(justImg),
        'instatnceComs':instatnceComs,
        'least_price':int(least_price),
        'max_price':int(max_price),
        'locas_to_go':locas_to_go,
        'immadate_location_image':immadate_location_image,
        'price_Title':price_Title,
        'moavezeh':moavezeh,
        'exchange':exchange,
        'farWork':farWork,
        'soldier':soldier,
        'publisher':publisher,
        'publisherForCar':publisherForCar,
        'phoneStatus':phoneStatus
        # 'choose_min_price_for_work':choose_min_price_for_work,

        
    }

    return render(request,"core/AmlakAfterFilter.html",contex)





def handleAmlakFilterSecondLevel(request):

    province=request.session.get("bb")
    smallCities=request.session.get("min")
    defaultLocalIds=[]

    cities=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    for c in cities:
        for loc in c.location_set.all():
            defaultLocalIds.append(loc.id)
        

    locationIds=request.GET.get("ids")
    justImg=request.GET.get("justImg",False)
    instatnceComs=request.GET.get("instatnceComs","عادی")
    title=request.GET.get("title")
    publisherForCar=request.GET.get("publisherForCar","همه")
    phoneStatus=request.GET.get("phoneStatus","همه")
    choose_min_price_for_work=request.GET.get("choose_min_price_for_work",0)
    choose_max_price_for_work=request.GET.get("choose_max_price_for_work",20)
    minKarkard=request.GET.get("minKarkard",10)
    maxKarkard=request.GET.get("maxKarkard",400)
    minYearOfConstruction=request.GET.get("minYearOfConstruction",1365)
    maxYearOfConstruction=request.GET.get("maxYearOfConstruction",1402)
    roomNumber=request.GET.get("roomNumber",1)
    publisherForAmlak=request.GET.get("publisher","همه")
    farWork=request.GET.get("farWork",False)
    soldier=request.GET.get("soldier",False)
    insurance=request.GET.get("insurance",False)
    exchange=request.GET.get("exchange",False)

    title=request.GET.get("title")
 

    least_price=request.GET.get("least_price",0)
    max_price=request.GET.get("max_price",400000000)

    maxMeter=request.GET.get("maxMeter",200)
    leastMeter=request.GET.get("leastMeter",65)

    maxVadieh=request.GET.get("maxVadieh",800)
    minVadieh=request.GET.get("minVadieh",30)

    maxEjareh=request.GET.get("maxEjareh",7)
    minEjareh=request.GET.get("minEjareh",1)

    locas_to_go=list(map(

            lambda x:int(x),locationIds.split(",")
            if len(locationIds)>=1 else defaultLocalIds
        ))
    # publisherForAmlak=publisherForAmlak if len(publisher)>0 else "همه"


    coms_to_show=None
    
    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )


    if title in typeOneForSecondLevelFilter_Amlak_Frosh:

        
        if province and smallCities:
          
                if bool(justImg):


                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak)&
                            Q(rooms__gte=int(roomNumber))                  
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber)) 
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()


        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(int(least_price),int(max_price))) & 
                        Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                        Q(publisher=publisherForAmlak)&
                        Q(rooms__gte=int(roomNumber))   

                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(int(least_price),int(max_price))) & 
                        Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                        Q(publisher=publisherForAmlak)&
                        Q(rooms__gte=int(roomNumber))  
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()


        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(int(least_price),int(max_price))) & 
                        Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                        Q(publisher=publisherForAmlak)&
                            Q(rooms__gte=int(roomNumber))  
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber)) 
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
    
    elif title in amlakEjareh:

        if province and smallCities:
          
                if bool(justImg):


                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber))               
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber))    
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()



        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber))   

                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()


        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(publisher=publisherForAmlak) &
                            Q(rooms__gte=int(roomNumber))   
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
    
    elif title in vasayelNaghliehMotor_va_Car:
        ourCom=get_object_or_404(Commerical,title=title)
        first_child=ourCom.children.first()

        if province and smallCities:
                
                if first_child.children.all():

          
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__parent__title=title)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q()
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__parent__title=title)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&  
                                    Q(ready_to_exchange=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                else:
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__title=title)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__title=title)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&  
                                    Q(ready_to_exchange=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            print("FUUUUUNNNNNNNNNN")
                            print("FUUUUUNNNNNNNNNN")
                            print("FUUUUUNNNNNNNNNN")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif province and not smallCities:

                print("B")
                if first_child.children.all():

                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 

                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 

                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                else:
                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 

                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 

                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif not province and smallCities:
                if first_child.children.all():


                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                    else:
                        if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

                
                else:
                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                    else:
                        if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

    elif title in vasayelNaghlieh_Both_and_supplies:

        if province and smallCities:
                        
            if bool(justImg):

                if exchange:

                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(location__in=locas_to_go)&
                            Q(parent__title=title)
                        ).filter(
                            Q(publisherForCar=publisherForCar)&
                            Q(ready_to_exchange=True)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(location__in=locas_to_go)&
                            Q(parent__title=title)
                        ).filter(
                            Q(publisherForCar=publisherForCar)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
            else:
                if exchange:

                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                        ).filter(
                            Q(publisherForCar=publisherForCar)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&  
                            Q(ready_to_exchange=True)

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif province and not smallCities:

                print("B")
                
                if bool(justImg):
                    if exchange:

                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()

                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(publisherForCar=publisherForCar)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


        elif not province and smallCities:
                
            if bool(justImg):
                if exchange:

                    coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(publisherForCar=publisherForCar)&
                            Q(ready_to_exchange=True)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:

                    coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(publisherForCar=publisherForCar)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
            else:
                if exchange:
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(publisherForCar=publisherForCar)&
                        Q(ready_to_exchange=True)&
                        Q(price__range=(int(least_price),int(max_price)))&
                        Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()
                else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(publisherForCar=publisherForCar)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

    elif title in digitalOrKitchenOrPersonalOrEntertaimentOrSupllies:

        ourCom=get_object_or_404(Commerical,title=title)
        first_child=ourCom.children.first()

        if province and smallCities:
                
                if first_child.children.all():

          
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__parent__title=title)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                  
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__parent__title=title)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)

                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                else:
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__title=title)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(location__in=locas_to_go)&
                                    Q(parent__title=title)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


        elif province and not smallCities:

                print("B")
                if first_child.children.all():

                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                else:
                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif not province and smallCities:
                if first_child.children.all():


                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                    else:
                        if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(phone_status=phoneStatus)&
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(phone_status=phoneStatus)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

                

                else:
                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(phone_status=phoneStatus)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                    else:
                        if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(phone_status=phoneStatus)&
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(phone_status=phoneStatus)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

    elif title in services:

        if province and smallCities:
                        
            if bool(justImg):

              
                coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                ).filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities]) 
                    ).filter(
                        Q(location__in=locas_to_go)&
                        Q(parent__title=title)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        img_length__gte=1
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()
            else:        
                coms_to_show=Commerical.objects.filter(
                    Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities]) 
                    ).filter(
                    Q(parent__title=title) &
                    Q(location__in=locas_to_go)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()

        elif province and not smallCities:

                print("B")
                
                if bool(justImg):
                    

                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()

                else:
                             
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()


        elif not province and smallCities:
                
            if bool(justImg):
                

                    coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
            else:
                
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()

    elif title in social:

        if province and smallCities:
                        
            if bool(justImg):

                if exchange:

                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(location__in=locas_to_go)&
                            Q(parent__title=title)
                        ).filter(
                            Q(ready_to_exchange=True)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(location__in=locas_to_go)&
                            Q(parent__title=title)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
            else:
                if exchange:

                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                        ).filter(
                            Q(publisherForCar=publisherForCar)&
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(ready_to_exchange=True)

                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif province and not smallCities:

                print("B")
                
                if bool(justImg):
                    if exchange:

                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()

                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                com_status=instatnceComs
                            ).distinct()
                else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


        elif not province and smallCities:
                
            if bool(justImg):
                if exchange:

                    coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(ready_to_exchange=True)&
                            Q(price__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
                else:

                    coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(price__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).distinct()
            else:
                if exchange:
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(ready_to_exchange=True)&
                        Q(price__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()
                else:
                        coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()


    elif title in employment:

        if province and smallCities:
                        
            if bool(justImg):

                if farWork:
                    if soldier:
                        if insurance:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                            Q(farWork=True)&
                                            Q(soldier=True)&
                                            Q(insurance=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                            Q(farWork=True)&
                                            Q(soldier=True)&
                    
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                    else:
                        if insurance:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                            Q(farWork=True)&
                                            Q(insurance=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                            Q(farWork=True)&
                                        
                    
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                else:
                    if soldier:
                        if insurance:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                     
                                            Q(soldier=True)&
                                            Q(insurance=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                  
                                            Q(soldier=True)&
                    
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                    else:
                        if insurance:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                      
                                            Q(insurance=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(location__in=locas_to_go)&
                                            Q(parent__title=title)
                                        ).filter(
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

            else:

                if farWork:
                    if soldier:
                        if insurance:
                                print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(farWork=True)&
                                        Q(soldier=True)&
                                        Q(insurance=True)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(farWork=True)&
                                        Q(soldier=True)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    else:
                        if insurance:
                                print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(farWork=True)&
                                      
                                        Q(insurance=True)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(farWork=True)&
                                     
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()




                else:
                        if soldier:
                            if insurance:
                                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(soldier=True)&
                                            Q(insurance=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            else:
                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(soldier=True)&
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        else:
                            if insurance:
                                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(insurance=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            else:
                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()


        elif province and not smallCities:

                print("B")
                
                if bool(justImg):

                    if farWork:
                        if soldier:

                            if insurance:
                                
                                     coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                                Q(soldier=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                                Q(soldier=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                        else:

                            if insurance:
                                
                                     coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                               
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                               
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            

                
                    else:

                        if soldier:

                            if insurance:
                                
                                     coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            
                                                Q(soldier=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                              
                                                Q(soldier=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                        else:

                            if insurance:
                                
                                     coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                             
                                               
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                             
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                            
                else:
                        if farWork:
                            if soldier:
                                if insurance:


                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                                Q(soldier=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                                else:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                                Q(soldier=True)&
                                  
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                            else:
                                if insurance:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                            
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                                else:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&                                
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()








                            # else farWork


                        else:
                            
                            if soldier:
                                if insurance:


                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                        
                                                Q(soldier=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                                else:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                             
                                                Q(soldier=True)&
                                  
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                            else:
                                if insurance:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                          
                                            
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                                else:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                                                           
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()



        elif not province and smallCities:
                
            if bool(justImg):
                if farWork:

                    if soldier:
                        if insurance:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                                Q(soldier=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(farWork=True)&
                                            Q(soldier=True)&
                                  
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    else:

                        if insurance:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(farWork=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(farWork=True)&
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                # else FarWork
                else:

                    if soldier:
                        if insurance:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                           
                                                Q(soldier=True)&
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                           
                                            Q(soldier=True)&
                                  
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    else:

                        if insurance:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                
                                                Q(insurance=True)&
                                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            
                                            Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()





            # else image
            else:
                if farWork:
                    if soldier:
                        if insurance:

                                coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(farWork=True)&
                                Q(soldier=True)&
                                Q(insurance=True)&
                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(farWork=True)&
                                Q(soldier=True)&
                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

                    else:
                        if insurance:

                                coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(farWork=True)&
                                
                                Q(insurance=True)&
                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(farWork=True)&
                                Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

                    # else farWork
                else:
                        if soldier:
                            if insurance:

                                    coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                  
                                    Q(soldier=True)&
                                    Q(insurance=True)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                            else:
                                coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(soldier=True)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        else:
                            if insurance:

                                    coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                
                                    
                                    Q(insurance=True)&
                                    Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                            else:
                                    coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                    
                                        Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

    cat=get_object_or_404(Commerical,title=title)
    cat_childs=cat.children.all()

    contex={

        'cat_childs':cat_childs,
        'catMain':cat,
        'cits':cits,
        'coms_to_show':coms_to_show,
        'GroupHasPrice':GroupHasPrice,
        'GroupHasMeter':GroupHasMeter,
        'GroupHasYearOfConstruction':GroupHasYearOfConstruction,
        'GroupHasExchangePossibale':GroupHasExchangePossibale,
        'GroupHasCommericalSituation_like_new_or_old':GroupHasCommericalSituation_like_new_or_old,
        'Group_Employments':Group_Employments,
     
        'justImg':bool(justImg),
        'instatnceComs':instatnceComs,
        'least_price':int(least_price),
        'max_price':int(max_price),
        'locas_to_go':locas_to_go,
        'immadate_location_image':immadate_location_image,
        'price_Title':price_Title,
        'moavezeh':moavezeh,
        'exchange':exchange,
        'farWork':farWork,
        'soldier':soldier,
        'publisherForAmlak':publisherForAmlak,
        'publisherForCar':publisherForCar,
        'phoneStatus':phoneStatus,
        'choose_min_price_for_work':int(choose_min_price_for_work),
        'choose_max_price_for_work':int(choose_max_price_for_work),
        'minKarkard':int(minKarkard),
        'maxKarkard':int(maxKarkard),
        'minVadieh':int(minVadieh),
        'maxVadieh':int(maxVadieh),
        'minEjareh':int(minEjareh),
        'maxEjareh':int(maxEjareh),
        'leastMeter':int(leastMeter),
        'maxMeter':int(maxMeter),
        'roomNumber':int(roomNumber),
        'minYearOfConstruction':int(minYearOfConstruction),
        'maxYearOfConstruction':int(maxYearOfConstruction),


    }
    return render(request,"core/handleAmlakFilterSecondLevel.html",contex)





def handleFilterThirdLevel(request):


    province=request.session.get("bb")
    smallCities=request.session.get("min")
    defaultLocalIds=[]

    cities=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    for c in cities:
        for loc in c.location_set.all():
            defaultLocalIds.append(loc.id)
        

    locationIds=request.GET.get("ids")
    justImg=request.GET.get("justImg",False)
    instatnceComs=request.GET.get("instatnceComs","عادی")
    title=request.GET.get("title")
    publisherForCar=request.GET.get("publisherForCar","همه")
    phoneStatus=request.GET.get("phoneStatus","همه")
    choose_min_price_for_work=request.GET.get("choose_min_price_for_work",0)
    choose_max_price_for_work=request.GET.get("choose_max_price_for_work",20)
    minKarkard=request.GET.get("minKarkard",10)
    maxKarkard=request.GET.get("maxKarkard",400)
    minYearOfConstruction=request.GET.get("minYearOfConstruction",1365)
    maxYearOfConstruction=request.GET.get("maxYearOfConstruction",1402)
    roomNumber=request.GET.get("roomNumber",1)
    publisherForAmlak=request.GET.get("publisherForAmlak","همه")
    farWork=request.GET.get("farWork",False)
    soldier=request.GET.get("soldier",False)
    insurance=request.GET.get("insurance",False)
    exchange=request.GET.get("exchange",False)
    internalOrExternal=request.GET.get("internalOrExternal","همه")

    parking=request.GET.get("parking",False)
    anbari=request.GET.get("anbari",False)
    sanadEdari=request.GET.get("sanadEdari",False)
    floor=request.GET.get("floor",1)
    color=request.GET.get("color","همه")
    esalat=request.GET.get("esalat","همه")
    simcartNums=request.GET.get("simcartNums",1)
    simcartType=request.GET.get("simcartType","ایرانسل")


    title=request.GET.get("title")
 

    least_price=request.GET.get("choose_min_price",0)
    max_price=request.GET.get("choose_max_price",400000000)

    maxMeter=request.GET.get("maxMeter",200)
    leastMeter=request.GET.get("leastMeter",65)

    maxVadieh=request.GET.get("maxVadieh",800)
    minVadieh=request.GET.get("minVadieh",30)

    maxEjareh=request.GET.get("maxEjareh",7)
    minEjareh=request.GET.get("minEjareh",1)
    memorySize=request.GET.get("memorySize",4)
    coverSimcart=request.GET.get("coverSimcart","ندارد")
    clothsType=request.GET.get("clothsType","همه")


    locas_to_go=list(map(

            lambda x:int(x),locationIds.split(",")
            if len(locationIds)>=1 else defaultLocalIds
        ))
        

    coms_to_show=None
    
    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )

    if title in apartemanForosh:

        if title in foroshJustForSanadEdari:

            if province and smallCities:
                    if bool(justImg):

                        if parking:
                            if anbari:
                                if sanadEdari:
                        
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else for anbari
                            else:

                                if sanadEdari:
                        
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)& 
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(  
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                        # else for parking
                        else:
                            if anbari:
                                if sanadEdari:
                        
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else for anbari
                            else:

                                if sanadEdari:
                        
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)& 
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(  
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()



                    # else for image
                    else:
                        print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                        if parking:
                            if anbari:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(anbari=True)&
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(anbari=True)&
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else for anbari
                            else:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                        # else for parking
                        else:
                            if anbari:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(anbari=True)&
                                                        
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(anbari=True)&
                                                        
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else for anbari
                            else:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                        Q(publisher=publisherForAmlak)&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()


            elif province and not smallCities:

                    print("B")

                    if bool(justImg):

                        if parking:

                            if anbari:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                            # else for anbari

                            else:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&    
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                        # else for parking
                        else:
                            if anbari:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                   
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                            # else for anbari

                            else:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&    
                                                   
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                   
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                    

                    # else for image
                    else:

                        if parking:

                            if anbari:
                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                            # else for anbari
                            else:

                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                        # else for parking
                        else:

                            if anbari:

                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                            # else for anbari
                            else:

                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()



            elif not province and smallCities:
                print("C")

                if bool(justImg):

                    if parking:

                        if anbari:
                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct() 


                        # else for anabri
                        else:

                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                 
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                   
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct() 


                    # else for parking
                    else:

                        if anbari:
                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct() 


                        # else for anabri
                        else:

                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct() 

                        





                # else for image
                else:

                    if parking:
                        if anbari:
                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                        # else for anbari
                        else:

                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                        
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                    
                    # else for parking
                    else:

                        if anbari:
                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                        # else for anbari
                        else:

                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

        # else for aparteman haie ke sanad edari  nadarn
        else:
            
            if province and smallCities:
          
                if bool(justImg):
                    
                    if parking:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                        # else for anbari
                        else:
                            
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                    # else for parking
                    else:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()


                # else for image
                else:

                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    if parking:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        # else for anbari
                        else:
                            print("BOBOBOBOBOOMMMMMM")
                            print("BOBOBOBOBOOMMMMMM")
                            print("BOBOBOBOBOOMMMMMM")
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    
                    # else for parking
                    else:

                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    

            elif province and not smallCities:

                    print("B")

                    if bool(justImg):

                        if parking:
                            if anbari:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        
                        # else for parking
                        else:
                            if anbari:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    

                # else for image
                    else:
                        if parking:
                            if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for anbari
                            else:
                                 coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        # else parking
                        else:
                            if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                           
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                            # else for anbari
                            else:
                                 coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()


            elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        if parking:
                            if anbari:
                                
                                    coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                            # else anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                            
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                        # else for parking
                        else:
                            if anbari:
                                
                                    coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                            # else anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                                      
                    # else image
                    else:

                        if parking:
                            if anbari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
        
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                        # else for parking
                        else:
                            if anbari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
        
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
        
    elif title in ejarehAll:

        if province and smallCities:
          
                if bool(justImg):
                    if parking:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(anbari=True)&
                                    Q(parking=True)&
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(publisher=publisherForAmlak)&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(parking=True)&
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(publisher=publisherForAmlak)&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                    # else for parking
                    else:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(anbari=True)&
                                  
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(publisher=publisherForAmlak)&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(publisher=publisherForAmlak)&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                # else for iamge
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    if parking:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        # else for  anbari
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(parking=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for parking
                    else:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                       
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        # else for  anbari
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
         
                

        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if parking:
                        if anbari:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                 
                                                    Q(parking=True)&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                    # else for parking
                    else:
                        if anbari:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(publisher=publisherForAmlak)&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    com_status=instatnceComs
                                                ).distinct()



                # else for image    
                else:
                    if parking:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                    # else for parking
                    else:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                        
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                           
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()



        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if parking:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                           
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                    # else for parking
                    else:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(publisher=publisherForAmlak)&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()


                # else for iamge
                else:
                    if parking:

                        if anbari:
                        
                                coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        # elsefor parking
                        else:
                             coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(                                       
                                        Q(parking=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for parking'
                    else:
                        if anbari:
                        
                                coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                       
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        # elsefor parking
                        else:
                             coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(                                       
                                    
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(publisher=publisherForAmlak)&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
    

    elif title in cars:

        if province and smallCities:
          
                if bool(justImg):

                    if exchange:

                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(publisherForCar=publisherForCar)&
                                    Q(ready_to_exchange=True)&
                                    Q(internal_or_external=internalOrExternal)&
                                    Q(color=color)&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(publisherForCar=publisherForCar)&
                                    Q(internal_or_external=internalOrExternal)&
                                    Q(color=color)&
                                    Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                    Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                # else for image
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    if  exchange:

                        coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(publisherForCar=publisherForCar)&
                            Q(ready_to_exchange=True)&
                            Q(internal_or_external=internalOrExternal)&
                            Q(color=color)&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()
                    else:
                         coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(publisherForCar=publisherForCar)&
                          
                            Q(internal_or_external=internalOrExternal)&
                            Q(color=color)&
                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).distinct()

        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(publisherForCar=publisherForCar)&
                                            Q(ready_to_exchange=True)&
                                            Q(internal_or_external=internalOrExternal)&
                                            Q(color=color)&
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(publisherForCar=publisherForCar)&
    
                                            Q(internal_or_external=internalOrExternal)&
                                            Q(color=color)&
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()


                # else for image

                else:
                    if exchange:

                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(publisherForCar=publisherForCar)&
                                        Q(ready_to_exchange=True)&
                                        Q(internal_or_external=internalOrExternal)&
                                        Q(color=color)&
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                        Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))    
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(publisherForCar=publisherForCar)&
                                  
                                        Q(internal_or_external=internalOrExternal)&
                                        Q(color=color)&
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                        Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))    
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        


        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                    Q(publisherForCar=publisherForCar)&
                                Q(ready_to_exchange=True)&
                                Q(internal_or_external=internalOrExternal)&
                                Q(color=color)&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction))) 
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                Q(publisherForCar=publisherForCar)&
                               
                                Q(internal_or_external=internalOrExternal)&
                                Q(color=color)&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct() 
                    
                # else for image
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                            Q(publisherForCar=publisherForCar)&
                                            Q(ready_to_exchange=True)&
                                            Q(internal_or_external=internalOrExternal)&
                                            Q(color=color)&
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction))) 
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                            Q(publisherForCar=publisherForCar)&
                                     
                                            Q(internal_or_external=internalOrExternal)&
                                            Q(color=color)&
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction))) 
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

    elif title in tablet_and_mobile:

        if title == "تبلت":

                if province and smallCities:
          
                    if bool(justImg):
                        if exchange:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(cover_simcart=coverSimcart)&
                                            Q(ready_to_exchange=True)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        # else for exchange
                        else:
                             coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(cover_simcart=coverSimcart)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()



                    # else for image
                    else:
                        if exchange:

                            print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                        Q(cover_simcart=coverSimcart)&
                                        Q(ready_to_exchange=True)  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        
                        # else for exhange
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                        Q(cover_simcart=coverSimcart)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        
                elif province and not smallCities:

                        print("B")

                        if bool(justImg):
                            if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(cover_simcart=coverSimcart)&
                                            Q(ready_to_exchange=True)  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        
                            # else for exhange
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(cover_simcart=coverSimcart)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        
                        # else for image

                        else:
                            if exhange:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(cover_simcart=coverSimcart)&
                                            Q(ready_to_exchange=True) 
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()

                            # else for exchange
                            else:
                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(cover_simcart=coverSimcart)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        if exchange:

                                    coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))&
                                                Q(phone_status=phoneStatus)&
                                                Q(esalat=esalat)&
                                                Q(sim_cart_number__gte=simcartNums)&
                                                Q(color=color)&
                                                Q(memory_size__gte=memorySize)&
                                                Q(cover_simcart=coverSimcart)&
                                                Q(ready_to_exchange=True)   
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))&
                                                Q(phone_status=phoneStatus)&
                                                Q(esalat=esalat)&
                                                Q(sim_cart_number__gte=simcartNums)&
                                                Q(color=color)&
                                                Q(memory_size__gte=memorySize)&
                                                Q(cover_simcart=coverSimcart)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                    
                    # else for image
                    else:
                        if exchange:

                                coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                        Q(cover_simcart=coverSimcart)&
                                        Q(ready_to_exchange=True)   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                        Q(cover_simcart=coverSimcart)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
    
        


        # else for not tablet
        else:
            if province and smallCities:
          
                    if bool(justImg):
                        if exchange:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(ready_to_exchange=True)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                        
                        # else for exchange
                        else:
                             coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                            Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            img_length__gte=1
                                        ).filter(
                                            com_status=instatnceComs
                                        ).distinct()



                    # else for image
                    else:
                        if exchange:

                            print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                        Q(ready_to_exchange=True)  
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        
                        # else for exhange
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        
            elif province and not smallCities:

                    print("B")

                    if bool(justImg):
                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                       
                                        Q(ready_to_exchange=True)  
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    
                        # else for exhange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    
                    # else for image

                    else:
                        if exhange:

                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)&
                                        
                                        Q(ready_to_exchange=True) 
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()

                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(phone_status=phoneStatus)&
                                        Q(esalat=esalat)&
                                        Q(sim_cart_number__gte=simcartNums)&
                                        Q(color=color)&
                                        Q(memory_size__gte=memorySize)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)&
                                            Q(ready_to_exchange=True)   
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(phone_status=phoneStatus)&
                                            Q(esalat=esalat)&
                                            Q(sim_cart_number__gte=simcartNums)&
                                            Q(color=color)&
                                            Q(memory_size__gte=memorySize)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            com_status=instatnceComs
                                        ).distinct()
                
                # else for image
                else:
                    if exchange:

                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(phone_status=phoneStatus)&
                                    Q(esalat=esalat)&
                                    Q(sim_cart_number__gte=simcartNums)&
                                    Q(color=color)&
                                    Q(memory_size__gte=memorySize)&
                                    Q(ready_to_exchange=True)   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(phone_status=phoneStatus)&
                                    Q(esalat=esalat)&
                                    Q(sim_cart_number__gte=simcartNums)&
                                    Q(color=color)&
                                    Q(memory_size__gte=memorySize)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


    elif title =="سیم کارت":
        
        if province and smallCities:
          
                if bool(justImg):
                    if  exchange:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(simcartType=simcartType)&
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for exhange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(simcartType=simcartType)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                
                # else for image
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    if exchange:
                        coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(simcartType=simcartType)&
                                Q(ready_to_exchange=True)   
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(simcartType=simcartType)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if exchange:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(simcartType=simcartType)&
                                    Q(ready_to_exchange=True)   
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(simcartType=simcartType) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                else:
                    if exchange:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(simcartType=simcartType)&
                                    Q(ready_to_exchange=True)   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(simcartType=simcartType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()

        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))&
                                                Q(simcartType=simcartType)&
                                                Q(ready_to_exchange=True)  
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(simcartType=simcartType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                        
                # else for image
                else:
                    if exchange:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(simcartType=simcartType)&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(simcartType=simcartType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()

    elif title in themSelf:

        if province and smallCities:
          
                if bool(justImg):
                    if exchange:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                            ).filter(
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                Q(price__range=(int(least_price),int(max_price))) &
                                                Q(ready_to_exchange=True)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                img_length__gte=1
                                            ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                    
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                img_length__gte=1
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

                # else for image
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                        Q(ready_to_exchange=True)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        

        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price))) &
                                        Q(ready_to_exchange=True)   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                
                # else for image
                else:
                    if exchange:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    Q(ready_to_exchange=True)    
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price))) &
                                        Q(ready_to_exchange=True)   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) 
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                else:
                    if exchange:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    Q(ready_to_exchange=True)    
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()


    elif title in male_or_female:
        if province and smallCities:
          
                if bool(justImg):
                    if exchange:
                                coms_to_show=Commerical.objects.annotate(
                                            img_length=Length("commericalimage")
                                        ).filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                            ).filter(
                                                Q(parent__title=title) &
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                Q(price__range=(int(least_price),int(max_price))) &
                                                Q(ready_to_exchange=True)&
                                                Q(cloths_type=clothsType)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                img_length__gte=1
                                            ).filter(
                                                com_status=instatnceComs
                                            ).distinct()
                    
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price))) &
                                Q(cloths_type=clothsType)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                img_length__gte=1
                            ).filter(
                                com_status=instatnceComs
                            ).distinct()

                # else for image
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                   Q(price__range=(int(least_price),int(max_price))) &
                                   Q(ready_to_exchange=True)&
                                   Q(cloths_type=clothsType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &       
                                    Q(cloths_type=clothsType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                        

        elif province and not smallCities:

                print("B")

                if bool(justImg):
                    if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price))) &
                                        Q(ready_to_exchange=True)&
                                        Q(cloths_type=clothsType)  
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    # else for exchange
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price))) &
                                        Q(cloths_type=clothsType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                
                # else for image
                else:
                    if exchange:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    Q(ready_to_exchange=True)&
                                    Q(cloths_type=clothsType)   
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    Q(cloths_type=clothsType)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()

        elif not province and smallCities:
                print("C")

                if bool(justImg):
                    if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                        Q(price__range=(int(least_price),int(max_price))) &
                                        Q(ready_to_exchange=True)&
                                        Q(cloths_type=clothsType)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        com_status=instatnceComs
                                    ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    
                                    Q(cloths_type=clothsType)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    com_status=instatnceComs
                                ).distinct()


                else:
                    if exchange:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    Q(ready_to_exchange=True)&
                                    Q(cloths_type=clothsType)   
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) &
                                    Q(cloths_type=clothsType)  
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    com_status=instatnceComs
                                ).distinct()



    cat=get_object_or_404(Commerical,title=title)
    cat_childs=cat.children.all()

    contex={

       
        'cits':cits,
        'cat_childs':cat_childs,
        'catMain':cat,
        'coms_to_show':coms_to_show,
        'GroupHasPrice':GroupHasPrice,
        'GroupHasMeter':GroupHasMeter,
        'GroupHasYearOfConstruction':GroupHasYearOfConstruction,
        'GroupHasExchangePossibale':GroupHasExchangePossibale,
        'GroupHasCommericalSituation_like_new_or_old':GroupHasCommericalSituation_like_new_or_old,
        'Group_Employments':Group_Employments,
        'groupHas_Parking_And_Anbari_And_Floor':groupHas_Parking_And_Anbari_And_Floor,
        'groupHas_sanadEdari':groupHas_sanadEdari,
        'cloths_accessory':cloths_accessory,
     
        'justImg':bool(justImg),
        'instatnceComs':instatnceComs,
        'least_price':int(least_price),
        'max_price':int(max_price),
        'locas_to_go':locas_to_go,
        'immadate_location_image':immadate_location_image,
        'price_Title':price_Title,
        'moavezeh':moavezeh,
        'exchange':exchange,
        'farWork':farWork,
        'soldier':soldier,
        'publisherForAmlak':publisherForAmlak,
        'publisherForCar':publisherForCar,
        'phoneStatus':phoneStatus,
        'choose_min_price_for_work':int(choose_min_price_for_work),
        'choose_max_price_for_work':int(choose_max_price_for_work),
        'minKarkard':int(minKarkard),
        'maxKarkard':int(maxKarkard),
        'minVadieh':int(minVadieh),
        'maxVadieh':int(maxVadieh),
        'minEjareh':int(minEjareh),
        'maxEjareh':int(maxEjareh),
        'leastMeter':int(leastMeter),
        'maxMeter':int(maxMeter),
        'roomNumber':int(roomNumber),
        'minYearOfConstruction':int(minYearOfConstruction),
        'maxYearOfConstruction':int(maxYearOfConstruction),
        'clothsType':clothsType,
        'coverSimcart':coverSimcart,
        'memorySize':memorySize,
        'simcartType':simcartType,
        'simcartNums':simcartNums,
        'esalat':esalat,
        'color':color,
        'sanadEdari':sanadEdari,
        'parking':parking,
        'anbari':anbari,
        'floor':floor,
        'internalOrExternal':internalOrExternal,
    }


    return render(request,"core/filterAmlakThirdLevel.html",contex)



class CommericalDetail(View):

    def get(self,request,comId,*args,**kwargs):

        com=get_object_or_404(Commerical,id=comId)
        contex={
            'c':com
        }
        return render(request,"core/CommericalDetail.html",contex)




def createThread(request,comId):
    com=get_object_or_404(Commerical,id=comId)
    thread=None
    t=Thread.objects.filter(
        Q(sender=com.user ,receiver=request.user) | Q(sender=request.user ,receiver=com.user)
    ).exists()
    
    if t:
        thread=t
    else:
        thread=Thread.objects.create(
            sender=request.user,receiver=com.user,commerical=com
        )
    return redirect("threadView",threadId=thread.id)




def threadView(request,threadId):

    t=get_object_or_404(Thread,id=threadId)

    messages=Message.objects.filter(
        thread=t
    ).order_by("-created")

    contex={
        'messages':messages,
        'thread':t
    }
    return render(request,"core/threaView.html",contex)





    
def load_more(request):

    if request.method=="POST":
        offset=int(request.POST.get("offset"))
        limit=5
        big=request.session.get("bb")
        ls=request.session.get("mini")
        
        
       
        bigInJson=[int(i) for i in big]

        ci=City.objects.filter(id__in=bigInJson)

        
    

        filtred_coms=None
        if big and ls:

            filtred_coms=Commerical.objects.filter(
            Q(city__in=bigInJson) | Q(smallCity__in=[int(i) for i in ls])
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()[offset:offset+limit]

            print("OONNNEEe")
        else:
            filtred_coms=Commerical.objects.filter(
                Q(city__in=bigInJson) 
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).distinct()[offset:offset+limit]
            print("TWOOWOOWOWOOWOW")
         
       

        print(filtred_coms,"FFFIILLFLFLFLLFLFL")


        totalData=Commerical.objects.filter(
             ~Q(parent=None) & ~Q(title__in=title_not_to_be)
        ).count()
    

    
     
        #             "parent.parent.parent.title":c.parent.parent.parent.title,
        #             "parent.parent.title":c.parent.parent.title,
        #             "parent.title":c.parent,
        #             "title":c.title,
        #             "created":c.created,
        #             "price":c.price,
        #             "year_of_construction":c.year_of_construction,
        #             "vadieh":c.vadieh,
        #             "rent":c.rent,
        #             "karkard_mashin":c.karkard_mashin,
        #             "phone_status":c.phone_status,
        data=filtred_coms.values(

                "parent__parent__parent",
                "parent__parent",
                "parent",
                "parent__parent__parent__title",
                "parent__parent__title",
                "parent__title",
                "price",
                "title",
                "year_of_construction",
                "vadieh",
                "rent",
                "karkard_mashin",
                "phone_status",
                "created",
                # "commericalimage"
 

            )
        print(data)
        a2= json.dumps(list(data), cls=DjangoJSONEncoder)
        print(type(a2),)

        return JsonResponse({"data":a2})




class MakeCommerical(View):

    def get(self,request,*args,**kwargs):
        
        coms=Commerical.objects.filter(     
          parent=None
            )
  
    
        contex={
            'cats2':coms
        }

        return render(request,"core/makeCommerical.html",contex)



class NewCommericalForm(View):
    
    def get(self,request,id=None,parent_id=None,*args,**kwargs):
        coms_to_show=None
        if parent_id:
            coms_to_show=get_object_or_404(Commerical,id=id)
        else:
            coms_to_show=get_object_or_404(Commerical,id=id)

        all_cits=City.objects.all()
        all_locs=Location.objects.all()

        locs=[]
        for l in all_locs:
            locs.append({
                "id":l.id,
                "name":l.name,
                "city":l.city.name,
                "city_id":l.city.id
            })

        print(locs)


        contex={

            'coms_to_show':coms_to_show,
            'cits':all_cits,
            'all_locs':json.dumps(locs),
            'locs':all_locs,
            'GroupHasMeter':GroupHasMeter,
            'GroupHasExchangePossibale':GroupHasExchangePossibale,
            'GroupHasPrice':GroupHasPrice,
            'GroupHasCommericalSituation_like_new_or_old':GroupHasCommericalSituation_like_new_or_old,
            'male_or_female':male_or_female
        }

        return render(request,"core/newCommerical.html",contex)


    def post(self,request,*args,**kwargs):

        images=None
        if self.request.POST.getlist("images"):

            images=self.request.POST.getlist("images")
        
        
        city_id=self.request.POST.get("city")
        location_id=self.request.POST.get("location")
        title=request.POST.get("title")
        detail=self.request.POST.get("detail")

        city=get_object_or_404(City,id=city_id)
        location=get_object_or_404(Location,id=location_id)

        
        frosh=["فروش مسکونی","فروش اداری و تجاری"]

        new_com=None
        if self.request.POST.get("parent_parent_title"):

            parent_parent_title=self.request.POST.get("parent_parent_title")
            com_id=self.request.POST.get("self_id_three_level")
            print(com_id,"TTITLTITLTITL")

            com_self=get_object_or_404(Commerical,id=com_id) 

            match parent_parent_title:

                case "املاک":
                    price=self.request.POST.get("price")
                    meter=self.request.POST.get("meter")
                    vadieh=self.request.POST.get("vadieh")
                    ejareh=self.request.POST.get("ejareh") 
                    rooms=self.request.POST.get("rooms")
                    floor=self.request.POST.get("floor")
                    parking=self.request.POST.get("parking")
                    anbari=self.request.POST.get("anbari")
                    publisher=self.request.POST.get("publisher")

                    if com_self.parent.title in frosh:

                        if com_self.parent.title == "فروش اداری و تجاری":
                            sandEdari=self.request.POST.get("sandEdari")

                            new_com=Commerical(
                                sanad_adari=sandEdari,
                                floor=floor,rooms=rooms,parking=True if parking else False,
                                anbari=True if anbari else False,meter=meter,price=price,city=city,
                                location=location,title=title,detail=detail,publisher=publisher
                            )

                        
            
              
                    

        return JsonResponse({
            'yes':True
        })






def first(request):

    contex={
        'name':'mohammad',
        'age':22
    }
    if request.method=="POST":
        contex={
            "name":"alireza"
        }
    return render(request,"core/test1.html",contex)


def second(request):
    contex={
        'email':'mohammadalipanah80@gmail.com',
        'cool':'yes'
    }
    return render(request,"core/second.html",contex)



