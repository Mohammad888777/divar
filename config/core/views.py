from django.shortcuts import render,get_object_or_404,redirect
from .models import (Commerical,SavedCommerical,
                    SmallCity,City,Thread,Message,
                    Feature,Tag,Location,CommericalImage
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
from .mixins import Loginrequired

from .utils2 import (
    groupHas_Parking_And_Anbari_And_Floor,groupHas_sanadEdari,
    cloths_accessory,justFloor,for_daily_rent,mosharekat

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
        # print("BEFFOORREEE")
        # print("BEFFOORREEE")
        # print("BEFFOORREEE")
        # print(self.request.GET)
        # print("AFTTTERRRR")
        # print("AFTTTERRRR")
        bigInJson=[int(i) for i in big]

        ci=City.objects.filter(id__in=bigInJson)

        
    

        filtred_coms=None
        if big and ls:

            filtred_coms=Commerical.objects.filter(
            Q(city__in=bigInJson) | Q(smallCity__in=ls)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()
            # print("OONNNEEe")
        else:
            filtred_coms=Commerical.objects.filter(
                Q(city__in=bigInJson) 
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).distinct()
            # print("TWOOWOOWOWOOWOW")
         
        all_cats=Commerical.objects.filter(
            parent=None
        )

        # print(filtred_coms,"FFFIILLFLFLFLLFLFL")
        for c in filtred_coms:
            print(c.city.name)

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
                        Q(price__range=(int(least_price),int(max_price))) 
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        img_length__gte=1
                    ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                    ).distinct()


    elif province and not smallCities:

            print("B")

            if bool(justImg):
                print("ITTSSSSSSSS")
                print("ITTSSSSSSSS")
                print("ITTSSSSSSSS")
                print("ITTSSSSSSSS")
                coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                ).filter(
                    Q(city__in=[int(i) for i in province]) &
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(int(least_price),int(max_price)))|
                    Q(vadieh__range=(int(least_price),int(max_price)))
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).filter(
                        img_length__gte=1
                ).filter(

                      Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))

                    ).distinct()
            else:
                coms_to_show=Commerical.objects.filter(
                    Q(city__in=[int(i) for i in province]) &
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(least_price,max_price))|
                    Q(vadieh__range=(int(least_price),int(max_price)))
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                    ).distinct()


    elif not province and smallCities:
            print("C")

            if bool(justImg):
                coms_to_show=Commerical.objects.annotate(
                    img_length=Length("commericalimage")
                ).filter(
                    Q(smallCity__in=[int(i) for i in smallCities])&
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(int(least_price),int(max_price)))|
                     Q(vadieh__range=(int(least_price),int(max_price)))
                   
                ).filter(
                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                ).filter(
                        img_length__gte=1
                ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                    ).distinct()
            else:
                coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(least_price,max_price))|
                        Q(vadieh__range=(int(least_price),int(max_price)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                    ).distinct()

    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    # for i in cits:
    #     for l in i.location_set.all():
    #         if l.id in locas_to_go :
    #             print("yese","********************************")
    #         else:
    #             print("NONONONOONONON")
    

 
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
            print("calleddd gooodd")
            print("calleddd gooodd")
            print("calleddd gooodd")

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
                    print("?????")
                    print("?????")
                    print("?????")
                    print("?????")

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
            print("marseeeyeyeyeyyeyeyeyeyey")
            print("marseeeyeyeyeyyeyeyeyeyey")
            print("marseeeyeyeyeyyeyeyeyeyey")

            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) 
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.parent.title) &
                Q(parent__title=cat.title)&
                Q(parent__id=cat.id)
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
        'cloths_accessory':cloths_accessory,
        'justFloor':justFloor
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
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q() if publisher == "همه" else  Q(publisher=publisher)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                        Q(smallCity__in=[int(i) for i in smallCities])         
                    ).filter(
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q() if publisher == "همه" else  Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                    ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q() if publisher == "همه" else  Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                    Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q() if publisher == "همه" else  Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q() if publisher == "همه" else  Q(publisher=publisher)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                        ).filter(
                            Q() if publisher == "همه" else  Q(publisher=publisher)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)
                                ).filter(
                                     Q(parent__parent__parent__title="وسایل نقلیه")|
                                     Q(parent__parent__title="وسایل نقلیه")
                                ).filter(
                                    Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                                ).filter(
                                    Q(parent__parent__parent__title="وسایل نقلیه")|
                                    Q(parent__parent__title="وسایل نقلیه")
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                                ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    else:

                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities])         
                            ).filter(
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                        ).filter(
                            Q(parent__parent__parent__title="وسایل نقلیه")|
                            Q(parent__parent__title="وسایل نقلیه")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))                          
                        ).filter(
                            Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                        ).filter(
                            Q(parent__parent__parent__title="وسایل نقلیه")|
                            Q(parent__parent__title="وسایل نقلیه")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                            
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &   
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                    else:
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                else:
                    if exchange:

                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)
                            ).filter(
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    else:
                        coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if publisherForCar == "همه" else  Q(publisherForCar=publisherForCar)
                            ).filter(
                                Q(parent__parent__parent__title="وسایل نقلیه")|
                                Q(parent__parent__title="وسایل نقلیه")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q() if phoneStatus == "همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                     Q(parent__parent__parent__title="کالای دیجیتال")|
                                     Q(parent__parent__title="کالای دیجیتال")
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities])         
                        ).filter(
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            Q() if phoneStatus == "همه" else Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                   
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            Q() if phoneStatus == "همه" else Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
     
                else:

                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            Q() if phoneStatus == "همه" else Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    


            elif not province and smallCities:
                print("C")

                if bool(justImg):

                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(location__in=locas_to_go)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if phoneStatus == "همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                 Q(parent__parent__parent__title="کالای دیجیتال")|
                                 Q(parent__parent__title="کالای دیجیتال")
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
  
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(location__in=locas_to_go)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            Q() if phoneStatus == "همه" else Q(phone_status=phoneStatus)
                        ).filter(
                             Q(parent__parent__parent__title="کالای دیجیتال")|
                             Q(parent__parent__title="کالای دیجیتال")
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()


        case "تجهیزات و صنعتی" | "سرگرمی و فراغت" | "خانه و آشپزخانه" | "وسایل شخصی":
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()

        case "خدمات":
            
            if province and smallCities:
                print("A")
                if bool(justImg):
 
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__parent__title="خدمات") &
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                else:
                    print("ELELLELELLSSSSSEEe")
                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities])         
                        ).filter(
                            Q(parent__parent__title="خدمات") &
                            Q(location__in=locas_to_go)
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()


            elif province and not smallCities:

                print("B")

                if bool(justImg):
                   
                        coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                        ).filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__parent__title="خدمات") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
     
                else:

                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                            Q(parent__parent__title="خدمات") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    


            elif not province and smallCities:
                print("C")

                if bool(justImg):
                    


                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title="خدمات") &
                                Q(location__in=locas_to_go)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
  
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__parent__title="خدمات") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
        'phoneStatus':phoneStatus,
        'choose_min_price_for_work':int(choose_min_price_for_work),
        'choose_max_price_for_work':int(choose_max_price_for_work),

        
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
    max_day_rent_paid_for_house=request.GET.get("max_day_rent_paid_for_house",900)
    min_day_rent_paid_for_house=request.GET.get("min_day_rent_paid_for_house",100)



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
                            Q(rooms__gte=int(roomNumber))                  
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber)) 
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    print("FOUNDDDDD")
                    print("FOUNDDDDD")
                    print("FOUNDDDDD")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(int(least_price),int(max_price))) & 
                        Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                        Q(rooms__gte=int(roomNumber))  
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber))  
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber)) 
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber))               
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber))    
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(rent__range=(int(minEjareh),int(maxEjareh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(rooms__gte=int(roomNumber))   
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
    
    elif title == "اجاره کوتاه مدت":

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
                            Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) &                         
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))               
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                             Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) &           
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))    
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                             Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) &  
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                            Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                             Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))   
                    ).filter(
                        Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                             Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) &  
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  &
                            Q(rooms__gte=int(roomNumber))   
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
    

    elif title == "پروژه‌های ساخت و ساز":
        
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
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                    ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    print("OOOKOKOKOKOKOKOKOKOKO")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(                            
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                    ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                    ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__title=title) &
                            Q(location__in=locas_to_go)
                        ).filter(
                             Q(day_rent_paid__range=(int(min_day_rent_paid_for_house),int(max_day_rent_paid_for_house))) &  
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                        ).filter(
                            Q() if publisherForAmlak == "همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            print("BBEEEEBBB")
                            print("BBEEEEBBB")
                            print("BBEEEEBBB")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                    Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                ).filter(
                                    Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()

                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                            ).filter(
                                    Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)| Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            print("sELELLELELELELLFLFLFL")
                            print("sELELLELELELELLFLFLFL")
                            print("sELELLELELELELLFLFLFL")
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))                    
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(production_year=None)| Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(production_year=None)| Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))  
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None) |Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()

                    else:
                        if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)| Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q(production_year=None)|Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                            ).filter(
                                Q(karkard_mashin=None)|Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                            ).filter(
                                Q() if publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(ready_to_exchange=True)&
                            Q(price__range=(int(least_price),int(max_price)))
                        ).filter(
                            Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(price__range=(int(least_price),int(max_price)))&
                            Q(ready_to_exchange=True)
                        ).filter(
                            Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                    ).distinct()
                else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  publisherForCar == "همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q() if  phoneStatus == "همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                                ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                                ).filter(
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(price__range=(int(least_price),int(max_price)))&
                                    Q(ready_to_exchange=True)
                                ).filter(
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()

                        else:
                            print("CLICKCKKCKC")
                            print("CLICKCKKCKC")
                            print("CLICKCKKCKC")
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                            ).filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                    Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                                ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price))) 
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(city__in=[int(i) for i in province]) &
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
                        else:

                            coms_to_show=Commerical.objects.annotate(
                            img_length=Length("commericalimage")
                            ).filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()


                    else:
                        if exchange:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(ready_to_exchange=True)&
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(ready_to_exchange=True)&
                                    Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                    img_length__gte=1
                            ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                Q(smallCity__in=[int(i) for i in smallCities])&
                                Q(parent__title=title) &
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if  phoneStatus=="همه" else Q(phone_status=phoneStatus)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()

                else:
                             
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                        ).distinct()
            else:
                
                    coms_to_show=Commerical.objects.filter(
                        Q(smallCity__in=[int(i) for i in smallCities])&
                        Q(parent__title=title) &
                        Q(location__in=locas_to_go)
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
        'min_day_rent_paid_for_house':int(min_day_rent_paid_for_house),
        'max_day_rent_paid_for_house':int(max_day_rent_paid_for_house),
        'insurance':insurance


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

    roomNumber=int(request.GET.get("roomNumber")) if request.GET.get("roomNumber") else request.GET.get("roomNumber")



    publisherForAmlak=request.GET.get("publisherForAmlak","همه")
    farWork=request.GET.get("farWork",False)
    soldier=request.GET.get("soldier",False)
    insurance=request.GET.get("insurance",False)
    exchange=request.GET.get("exchange",False)
    internalOrExternal=request.GET.get("internalOrExternal","همه")

    parking=request.GET.get("parking",False)
    anbari=request.GET.get("anbari",False)
    sanadEdari=request.GET.get("sanadEdari",False)

    floor=int(request.GET.get("floor",1)) if request.GET.get("floor") else request.GET.get("floor")


    color=request.GET.get("color","همه")

    esalat=request.GET.get("esalat","همه")
    simcartNums=request.GET.get("simcartNums",1)
    simcartType=request.GET.get("simcartType","ایرانسل")


    title=request.GET.get("title")
    parent_id=int(request.GET.get("catId"))
 

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
    dayRent=request.GET.get("dayRent")



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
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                 
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)& 
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                   
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(  
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                               
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                    Q(sanad_adari=True)& 
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedari
                                else:
                                    coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                                ).filter(
                                                    Q(city__in=[int(i) for i in province]) | 
                                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(  
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    
                                                    Q(floor__gte=floor)
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    img_length__gte=1
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(anbari=True)&
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(anbari=True)&
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                            # else for anbari
                            else:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(parking=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                        # else for parking
                        else:
                            if anbari:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(anbari=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(anbari=True)&
                                                        
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                            # else for anbari
                            else:
                                if sanadEdari:

                                        coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(sanad_adari=True)&
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadedair
                                else:   
                                    coms_to_show=Commerical.objects.filter(
                                                Q(city__in=[int(i) for i in province]) | 
                                                Q(smallCity__in=[int(i) for i in smallCities]) 
                                                ).filter(
                                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                                    Q(location__in=locas_to_go)
                                                ).filter(
                                                        Q(price__range=(int(least_price),int(max_price)))&
                                                        Q(rooms__gte=roomNumber)&
                                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                        Q(floor__gte=floor)   
                                                ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                                ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                            # else for anbari

                            else:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&    
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                        # else for parking
                        else:
                            if anbari:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                            # else for anbari

                            else:
                                if sanadEdari:
                                    
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                                # else for sanadEdari
                                else:
                                     coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                   
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                    

                    # else for image
                    else:

                        if parking:

                            if anbari:
                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()

                            # else for anbari
                            else:

                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(leastMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()

                        # else for parking
                        else:

                            if anbari:

                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()

                            # else for anbari
                            else:

                                if sanadEdari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                                # else for sanadEdari
                                else:
                                    print("BOOOMOOMOMOMOMOMOMO")
                                    print("BOOOMOOMOMOMOMOMOMO")
                                    print("BOOOMOOMOMOMOMOMOMO")
                                    coms_to_show=Commerical.objects.filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct() 


                        # else for anabri
                        else:

                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                 
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                   
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct() 


                    # else for parking
                    else:

                        if anbari:
                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(anbari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct() 


                        # else for anabri
                        else:

                            if sanadEdari:
                                        coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(sanad_adari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()

                            # else sanadEdari  
                            else:

                                coms_to_show=Commerical.objects.annotate(
                                                img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)   
                                            ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct() 

                        

                # else for image
                else:

                    if parking:
                        if anbari:
                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()

                        # else for anbari
                        else:

                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                        
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()

                    
                    # else for parking
                    else:

                        if anbari:
                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()

                        # else for anbari
                        else:

                            if sanadEdari:
                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(sanad_adari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for sanadEdari
                            else :
                                 coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)    
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()

                        # else for anbari
                        else:
                            
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                       Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()

                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)             
                                    ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                    
                    # else for parking
                    else:

                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                            Q(smallCity__in=[int(i) for i in smallCities]) 
                                        ).filter(
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                        ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                                ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(parking=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)    
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        
                        # else for parking
                        else:
                            if anbari:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                        ).filter(
                                    Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)    

                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                    

                # else for image
                    else:
                        if parking:
                            if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for anbari
                            else:
                                 coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else parking
                        else:
                            if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            # else for anbari
                            else:
                                 print("FUNNN")
                                 print("FUNNN")
                                 print("FUNNN")
                                 print("FUNNN")
                                 coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                            # else anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                            
                                                    Q(parking=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                        # else for parking
                        else:
                            if anbari:
                                
                                    coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                            # else anbari
                            else:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(smallCity__in=[int(i) for i in smallCities])&
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(    
                                                    Q(price__range=(int(least_price),int(max_price)))&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor) 
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                                      
                    # else image
                    else:

                        if parking:
                            if anbari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                           Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
        
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                           Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                
                                            Q(parking=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()

                        # else for parking
                        else:
                            if anbari:

                                    coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(anbari=True)&
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
        
                            # else for anbari
                            else:
                                coms_to_show=Commerical.objects.filter(
                                            Q(smallCity__in=[int(i) for i in smallCities])&
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)  
                                        ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
        


    elif title in for_daily_rent:
        # day_rent_paid

        if province and smallCities: 
          
                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(day_rent_paid__lte=int(dayRent))&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))         
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()


                # else for image
                else:

                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(day_rent_paid__lte=int(dayRent))&
                                Q(rooms__gte=roomNumber)&
                                Q(meter__range=(int(leastMeter),int(maxMeter)))
                            ).filter(
                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    

        elif province and not smallCities:

                print("B")

                if bool(justImg):

                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                            ).filter(
                        Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &Q(parent__id=parent_id)&
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(day_rent_paid__lte=int(dayRent))&
                            Q(rooms__gte=roomNumber)&
                            Q(meter__range=(int(leastMeter),int(maxMeter)))
                        ).filter(
                            Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
               

            # else for image
                else:
                    print("********************")
                    print("********************")
                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &Q(parent__id=parent_id)&
                            Q(location__in=locas_to_go)
                        ).filter(
                                Q(day_rent_paid__lte=int(dayRent))&
                                Q(rooms__gte=roomNumber)&
                                Q(meter__range=(int(leastMeter),int(maxMeter))) 
                        ).filter(
                            Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()


        elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(    
                                            Q(day_rent_paid__lte=int(dayRent))&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                                      
                    # else image
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(day_rent_paid__lte=int(dayRent))&
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))  
                                ).filter(
                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()
          

    elif title in mosharekat:

        if province and smallCities: 
          
                if bool(justImg):
                    coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))       
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()


                # else for image
                else:

                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(meter__range=(int(leastMeter),int(maxMeter)))
                            ).filter(
                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                    

        elif province and not smallCities:

                print("B")

                if bool(justImg):

                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                            ).filter(
                        Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &Q(parent__id=parent_id)&
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(meter__range=(int(leastMeter),int(maxMeter)))  
                        ).filter(
                            Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                img_length__gte=1
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
               

            # else for image
                else:
                    print("********************")
                    print("********************")
                    coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) &
                            Q(parent__title=title) &Q(parent__id=parent_id)&
                            Q(location__in=locas_to_go)
                        ).filter(
                                Q(meter__range=(int(leastMeter),int(maxMeter)))  
                        ).filter(
                            Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()


        elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        
                        coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(    
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                                      
                    # else image
                    else:
                        coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(meter__range=(int(leastMeter),int(maxMeter))) 
                                ).filter(
                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(anbari=True)&
                                    Q(parking=True)&
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()

                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(parking=True)&
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(anbari=True)&
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()

                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                    Q(smallCity__in=[int(i) for i in smallCities]) 
                                ).filter(
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                    Q(rooms__gte=roomNumber)&
                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                    Q(floor__gte=floor)&
                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))
                                ).filter(
                                    Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                    img_length__gte=1
                                ).filter(
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        # else for  anbari
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                    # else for parking
                    else:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        # else for  anbari
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter( 
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(parking=True)&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(parking=True)&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                    # else for parking
                    else:
                        if anbari:
                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(anbari=True)&
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                            ).filter(
                                                Q(city__in=[int(i) for i in province]) &
                                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                                Q(location__in=locas_to_go)
                                            ).filter(
                                                    Q(rooms__gte=roomNumber)&
                                                    Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                                    Q(floor__gte=floor)&
                                                    Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                                    Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                            ).filter(
                                                Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                            ).filter(
                                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                            ).filter(
                                                    img_length__gte=1
                                            ).filter(
                                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                                ).distinct()



                # else for image    
                else:
                    if parking:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()

                    # else for parking
                    else:
                        if anbari:

                                coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(city__in=[int(i) for i in province]) &
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh))) 
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(parking=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()

                    # else for parking
                    else:
                        if anbari:

                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                       Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(anbari=True)&
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for anbari
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(rooms__gte=roomNumber)&
                                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                            Q(floor__gte=floor)&
                                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                            Q(rent__range=(int(minEjareh),int(maxEjareh)))  
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()


                # else for iamge
                else:
                    if parking:

                        if anbari:
                        
                                coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(parking=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        # elsefor parking
                        else:
                             coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(                                       
                                        Q(parking=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                    # else for parking'
                    else:
                        if anbari:
                        
                                coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(anbari=True)&
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        # elsefor parking
                        else:
                             coms_to_show=Commerical.objects.filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(                                       
                                        Q(rooms__gte=roomNumber)&
                                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                                        Q(floor__gte=floor)&
                                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                                        Q(rent__range=(int(minEjareh),int(maxEjareh)))   
                                    ).filter(
                                        Q() if publisherForAmlak=="همه" else Q(publisher=publisherForAmlak)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
    


    elif title in cars:

        if title ==  "سواری و وانت":

            if province and smallCities:
            
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parnt_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&                                    
                                        Q(ready_to_exchange=True)& 
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                        Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                    ).filter(
                                            Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                        Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))
                                    ).filter(
                                            Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()


                    # else for image
                    else:
                        print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                        if  exchange:

                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) &Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))&
                                
                                Q(ready_to_exchange=True)&
                                
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                            ).filter(
                                    Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                            ).filter(
                                    Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()

            elif province and not smallCities:

                    print("B")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) & QQ(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))&
                                               
                                                Q(ready_to_exchange=True)&
                                                
                                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                                        ).filter(
                                            Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) & Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))&
                                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                                Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
                                        ).filter(
                                            Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()


                    # else for image

                    else:
                        if exchange:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(ready_to_exchange=True)&
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))    
                                    ).filter(
                                            Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            print("MIMIMIMIMIMI")
                            print("MIMIMIMIMIMI")
                            print("MIMIMIMIMIMI")
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))&
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))    
                                    ).filter(
                                            Q() if internalOrExternal =="همه" else Q(internal_or_external=internalOrExternal)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()

        elif title == "کلاسیک":

            if province and smallCities:
            
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) & Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        
                                        Q(ready_to_exchange=True)  
                                     
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()


                    # else for image
                    else:
                        print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                        if  exchange:

                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))&
                                Q(ready_to_exchange=True)          
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()

            elif province and not smallCities:

                    print("B")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))&
                                                Q(ready_to_exchange=True)
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price))) 
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()


                    # else for image

                    else:
                        if exchange:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))& 
                                            Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            print("EBIIII")
                            print("EBIIII")
                            print("EBIIII")
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))   
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            
            elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                           Q(price__range=(int(least_price),int(max_price)))&
                              
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                     Q(price__range=(int(least_price),int(max_price))) 
                                ).filter(
                                    Q() if color == "همه" else (Q(color=color))
                                ).filter(
                                    Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct() 
                        
                    # else for image
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))&
                                        
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                       Q(price__range=(int(least_price),int(max_price))) 
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()

        elif title == "اجاره‌ای":
            if province and smallCities:
            
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) & Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(day_rent_paid__lte=dayRent)&             
                                        Q(ready_to_exchange=True)  
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(day_rent_paid__lte=dayRent)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()


                    # else for image
                    else:
                        print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                        if  exchange:

                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(day_rent_paid__lte=dayRent)& 
                                Q(ready_to_exchange=True)          
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(day_rent_paid__lte=dayRent)
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()

            elif province and not smallCities:

                    print("B")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(day_rent_paid__lte=dayRent)& 
                                                Q(ready_to_exchange=True)
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(day_rent_paid__lte=dayRent) 
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()


                    # else for image

                    else:
                        if exchange:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(day_rent_paid__lte=dayRent)& 
                                            Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(day_rent_paid__lte=dayRent)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            
            elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                           Q(day_rent_paid__lte=dayRent)& 
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                     Q(day_rent_paid__lte=dayRent)
                                ).filter(
                                    Q() if color == "همه" else (Q(color=color))
                                ).filter(
                                    Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct() 
                        
                    # else for image
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(day_rent_paid__lte=dayRent)& 
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                       Q(day_rent_paid__lte=dayRent)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()

        elif title == "سنگین":
            if province and smallCities:
            
                    if bool(justImg):

                        if exchange:

                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) & Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))& 
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&            
                                        Q(ready_to_exchange=True)  
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                img_length=Length("commericalimage")
                                    ).filter(
                                        Q(city__in=[int(i) for i in province]) | 
                                        Q(smallCity__in=[int(i) for i in smallCities]) 
                                    ).filter(
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))& 
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        img_length__gte=1
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()


                    # else for image
                    else:
                        print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                        if  exchange:

                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))& 
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                Q(ready_to_exchange=True)          
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                            Q(city__in=[int(i) for i in province]) | 
                                Q(smallCity__in=[int(i) for i in smallCities]) 
                            ).filter(
                                Q(parent__title=title) & Q(parent__id=parent_id)&
                                Q(location__in=locas_to_go)
                            ).filter(
                                Q(price__range=(int(least_price),int(max_price)))& 
                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                            ).filter(
                                Q() if color == "همه" else (Q(color=color))
                            ).filter(
                                Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                            ).filter(
                                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                            ).filter(
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                            ).distinct()

            elif province and not smallCities:

                    print("B")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))& 
                                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                                Q(ready_to_exchange=True)
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()
                        
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                        img_length=Length("commericalimage")
                                        ).filter(
                                            Q(city__in=[int(i) for i in province]) &
                                            Q(parent__title=title) &Q(parent__id=parent_id)&
                                            Q(location__in=locas_to_go)
                                        ).filter(
                                                Q(price__range=(int(least_price),int(max_price)))& 
                                                Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard))) 
                                        ).filter(
                                            Q() if color == "همه" else (Q(color=color))
                                        ).filter(
                                            Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                        ).filter(
                                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                        ).filter(
                                                img_length__gte=1
                                        ).filter(
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                            ).distinct()


                    # else for image

                    else:
                        if exchange:

                                coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))& 
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
                                            Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.filter(
                                        Q(city__in=[int(i) for i in province]) &
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                            Q(price__range=(int(least_price),int(max_price)))& 
                                            Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                            
            elif not province and smallCities:
                    print("C")

                    if bool(justImg):
                        if exchange:

                                coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                    ).filter(
                                        Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))& 
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))& 
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                            img_length__gte=1
                                    ).filter(
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                        ).distinct()
                        # else for exchange
                        else:
                            coms_to_show=Commerical.objects.annotate(
                                    img_length=Length("commericalimage")
                                ).filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                    Q(parent__title=title) &Q(parent__id=parent_id)&
                                    Q(location__in=locas_to_go)
                                ).filter(
                                     Q(price__range=(int(least_price),int(max_price)))& 
                                     Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                ).filter(
                                    Q() if color == "همه" else (Q(color=color))
                                ).filter(
                                    Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                ).filter(
                                    ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                ).filter(
                                        img_length__gte=1
                                ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct() 
                        
                    # else for image
                    else:
                        if exchange:

                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                        Q(price__range=(int(least_price),int(max_price)))& 
                                        Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))& 
                                        Q(ready_to_exchange=True)
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                    ).distinct()
                        else:
                            coms_to_show=Commerical.objects.filter(
                                    Q(smallCity__in=[int(i) for i in smallCities])&
                                        Q(parent__title=title) &Q(parent__id=parent_id)&
                                        Q(location__in=locas_to_go)
                                    ).filter(
                                       Q(price__range=(int(least_price),int(max_price)))& 
                                       Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))
                                    ).filter(
                                        Q() if color == "همه" else (Q(color=color))
                                    ).filter(
                                        Q() if publisherForCar =="همه" else Q(publisherForCar=publisherForCar)
                                    ).filter(
                                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                                    ).filter(
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                            Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                        Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
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
                                    Q(com_status="فوری") if instatnceComs=="فوری" else  (Q(com_status= "عادی")| Q(com_status= "فوری"))
                                ).distinct()



    cat=get_object_or_404(Commerical,title=title,id=parent_id)
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
        'justFloor':justFloor,
     
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
        'roomNumber':int(roomNumber) if roomNumber else roomNumber,
        'minYearOfConstruction':int(minYearOfConstruction),
        'maxYearOfConstruction':int(maxYearOfConstruction),
        'clothsType':clothsType,
        'coverSimcart':coverSimcart,
        'memorySize':int(memorySize),
        'simcartType':simcartType,
        'simcartNums':int(simcartNums),
        'esalat':esalat,
        'color':color,
        'sanadEdari':sanadEdari,
        'parking':parking,
        'anbari':anbari,
        'floor':int(floor) if floor else floor,
        'internalOrExternal':internalOrExternal,
        'dayRent':int(dayRent) if dayRent else dayRent
    }


    return render(request,"core/filterAmlakThirdLevel.html",contex)



class CommericalDetail(View):

    def get(self,request,comId,*args,**kwargs):

        com=get_object_or_404(Commerical,id=comId)

        # time_to_go=''

        # to_irani_now=datetime2jalali(timezone.now())
        # print("OKAYYYY")
        # print("OKAYYYY")
        # print("OKAYYYY")
        # value=com.iranTimeCreated
        # a=findTimeDiffrence(timezone.now(),value).total_seconds()
        # print(a)
       


        # if  to_irani_now.year - value.year ==0:

        #     if to_irani_now.month - value.month==0:
        #         print("ONE MONTH")
        #         print("ONE MONTH")
                
        #         if to_irani_now.day-value.day ==0:
        #             if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<1:
        #                 if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=5:
        #                     time_to_go="لحظاتی پیش"
        #                 elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=10:
        #                     time_to_go="دقایقی پیش"

        #                 elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=15:
        #                     time_to_go="یک ربع پیش"
                        
        #                 elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=59:
        #                     time_to_go="نیم ساعت پیش"
                            
        #             if 1<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<2:
        #                 time_to_go="یک ساعت پیش"

        #             elif 2<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<3:
        #                 time_to_go="دو ساعت پیش"
                    
        #             elif 3<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<4:
        #                 time_to_go="سه ساعت پیش"

        #             elif 4<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<5:
        #                 time_to_go="چهار ساعت پیش"
        #             elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<6:
        #                 time_to_go="پنج ساعت پیش"
                    
        #             elif 6<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<7:
        #                 time_to_go="شش ساعت پیش"
                    
        #             elif 7<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<8:
        #                 time_to_go="هفت ساعت پیش"
                    
        #             elif 8<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<9:
        #                 time_to_go="هشت ساعت پیش"

        #             elif 9<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<10:
        #                 time_to_go="نه ساعت پیش"
        #             elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<11:
        #                 time_to_go="ده ساعت پیش"
        #             elif 11<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<12:
        #                 time_to_go="یازده ساعت پیش"
        #             elif 12<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<13:
        #                 time_to_go="دوازده ساعت پیش"
        #             elif 13<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<14:
        #                 time_to_go="سیزده ساعت پیش"
                    
        #             elif 14<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<15:
        #                 time_to_go="چهارده ساعت پیش"
                    
        #             elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<16:
        #                 time_to_go="پانزده ساعت پیش"
                    
        #             elif 16<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<17:
        #                 time_to_go="شانزده ساعت پیش"
                    
        #             elif 17<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<18:
        #                 time_to_go="هفده ساعت پیش"

        #             elif 18<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<19:
        #                 time_to_go="هجده ساعت پیش"
        #             elif 19<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<20:
        #                 time_to_go="نوزده ساعت پیش"
        #             elif 20<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<21:
        #                 time_to_go="بیست ساعت پیش"
        #             elif 21<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<22:
        #                 time_to_go="بیست و یک ساعت پیش"
        #             elif 22<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<23:
        #                 time_to_go="بیست و دو ساعت پیش"
                    
        #             elif 23<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<24:
        #                 time_to_go="بیست و سه ساعت پیش"
        #         elif to_irani_now.day-value.day==1:
        #             time_to_go ="دیروز"

        #         elif to_irani_now.day-value.day==2:
        #             time_to_go ="پریروز"
                
        #         elif to_irani_now.day-value.day==3:
        #             time_to_go ="سه روز پیش"
        #         elif to_irani_now.day-value.day==4:
        #             time_to_go ="چهار روز پیش"
                
        #         elif to_irani_now.day-value.day==5:
        #             time_to_go ="پنج روز پیش"
        #         elif to_irani_now.day-value.day==6:
        #             time_to_go ="شش روز پیش"
        #         elif 6<to_irani_now.day-value.day<14:
        #             time_to_go =" یک هفته پیش"
        #         elif 14<=to_irani_now.day-value.day<20:
        #             time_to_go =" دو هفته پیش"
                
        #         elif 20<=to_irani_now.day-value.day<28:
        #             time_to_go =" سه هفته پیش"
                
        #         elif 28<=to_irani_now.day-value.day<=31:
        #             time_to_go =" چهار هفته پیش"
        #     elif to_irani_now.month -value.month ==1:
        #         time_to_go="یک ماه پیش"
        # else:

        #     if to_irani_now.month - value.month==0:
        #         print("ONE MONTH")
        #         print("ONE MONTH")
                
        #         if to_irani_now.day-value.day ==0:
        #             if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<1:
        #                 if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=5:
        #                     time_to_go="لحظاتی پیش"
        #                 elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=10:
        #                     time_to_go="دقایقی پیش"

        #                 elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=15:
        #                     time_to_go="یک ربع پیش"
                        
        #                 elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=59:
        #                     time_to_go="نیم ساعت پیش"
                            
        #             if 1<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<2:
        #                 time_to_go="یک ساعت پیش"

        #             elif 2<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<3:
        #                 time_to_go="دو ساعت پیش"
                    
        #             elif 3<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<4:
        #                 time_to_go="سه ساعت پیش"

        #             elif 4<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<5:
        #                 time_to_go="چهار ساعت پیش"
        #             elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<6:
        #                 time_to_go="پنج ساعت پیش"
                    
        #             elif 6<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<7:
        #                 time_to_go="شش ساعت پیش"
                    
        #             elif 7<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<8:
        #                 time_to_go="هفت ساعت پیش"
                    
        #             elif 8<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<9:
        #                 time_to_go="هشت ساعت پیش"

        #             elif 9<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<10:
        #                 time_to_go="نه ساعت پیش"
        #             elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<11:
        #                 time_to_go="ده ساعت پیش"
        #             elif 11<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<12:
        #                 time_to_go="یازده ساعت پیش"
        #             elif 12<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<13:
        #                 time_to_go="دوازده ساعت پیش"
        #             elif 13<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<14:
        #                 time_to_go="سیزده ساعت پیش"
                    
        #             elif 14<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<15:
        #                 time_to_go="چهارده ساعت پیش"
                    
        #             elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<16:
        #                 time_to_go="پانزده ساعت پیش"
                    
        #             elif 16<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<17:
        #                 time_to_go="شانزده ساعت پیش"
                    
        #             elif 17<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<18:
        #                 time_to_go="هفده ساعت پیش"

        #             elif 18<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<19:
        #                 time_to_go="هجده ساعت پیش"
        #             elif 19<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<20:
        #                 time_to_go="نوزده ساعت پیش"
        #             elif 20<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<21:
        #                 time_to_go="بیست ساعت پیش"
        #             elif 21<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<22:
        #                 time_to_go="بیست و یک ساعت پیش"
        #             elif 22<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<23:
        #                 time_to_go="بیست و دو ساعت پیش"
                    
        #             elif 23<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<24:
        #                 time_to_go="بیست و سه ساعت پیش"
        #         elif to_irani_now.day-value.day==1:
        #             time_to_go ="دیروز"

        #         elif to_irani_now.day-value.day==2:
        #             time_to_go ="پریروز"
                
        #         elif to_irani_now.day-value.day==3:
        #             time_to_go ="سه روز پیش"
        #         elif to_irani_now.day-value.day==4:
        #             time_to_go ="چهار روز پیش"
                
        #         elif to_irani_now.day-value.day==5:
        #             time_to_go ="پنج روز پیش"
        #         elif to_irani_now.day-value.day==6:
        #             time_to_go ="شش روز پیش"
        #         elif 6<to_irani_now.day-value.day<14:
        #             time_to_go =" یک هفته پیش"
        #         elif 14<=to_irani_now.day-value.day<20:
        #             time_to_go =" دو هفته پیش"
                
        #         elif 20<=to_irani_now.day-value.day<28:
        #             time_to_go =" سه هفته پیش"
                
        #         elif 28<=to_irani_now.day-value.day<=31:
        #             time_to_go =" چهار هفته پیش"
        #     elif to_irani_now.month -value.month ==1 or to_irani_now.month -value.month==-11:
        #         print("CCCLLAEDD")
        #         time_to_go="یک ماه پیش"




        # print(time_to_go)  

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



class NewCommericalForm(Loginrequired,View):
    
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
        ej=["اجاره مسکونی","اجاره اداری و تجاری"]

        new_com=None
        if self.request.POST.get("parent_parent_title"):
 
            parent_parent_title=self.request.POST.get("parent_parent_title")
            com_id=self.request.POST.get("self_id_three_level")
            print(com_id,"TTITLTITLTITL")

            com_self=get_object_or_404(Commerical,id=com_id) 
  
            match parent_parent_title:

                case "املاک":
                    
                    meter=self.request.POST.get("meter")
                    
                    rooms=self.request.POST.get("rooms")
                   
                    parking=self.request.POST.get("parking")
                    anbari=self.request.POST.get("anbari")
                    publisher=self.request.POST.get("publisher")
                    

                    if com_self.parent.title in frosh:
                        price=self.request.POST.get("price")

                        if com_self.parent.title == "فروش اداری و تجاری":
                            floor=self.request.POST.get("floor")
                            sandEdari=self.request.POST.get("sandEdari",False)
                            price_each_meter=self.request.POST.get("price_each_meter")
                            constuction_melk=self.request.POST.get("constuction_melk")
                            new_com=Commerical(
                                sanad_adari=sandEdari,
                                floor=floor,rooms=rooms,parking=True if parking else False,
                                anbari=True if anbari else False,meter=meter,price=price,city=city,
                                location=location,title=title,detail=detail,publisher=publisher,
                                user=self.request.user,parent=com_self,price_each_meter=price_each_meter,year_of_construction=constuction_melk
                            )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()
  
                        else:
                            if com_self.title=="آپارتمان فروش":
                                floor=self.request.POST.get("floor")
                                constuction_melk=self.request.POST.get("constuction_melk")
                                price_each_meter=self.request.POST.get("price_each_meter")
                                new_com=Commerical(year_of_construction=constuction_melk,
                                    floor=floor,rooms=rooms,parking=True if parking else False,
                                    anbari=True if anbari else False,meter=meter,price=price,city=city,
                                    location=location,title=title,detail=detail,publisher=publisher,
                                    user=self.request.user,parent=com_self,price_each_meter=price_each_meter
                                )
                                new_com.save()
                                if images:
                                    for img in images:
                                        i=CommericalImage(image=img,commerical=new_com)
                                        i.save()
                                new_com.save()

                            else:
                                constuction_melk=self.request.POST.get("constuction_melk")

                                price_each_meter=self.request.POST.get("price_each_meter")
                                new_com=Commerical(year_of_construction=constuction_melk,
                                 rooms=rooms,parking=True if parking else False,
                                    anbari=True if anbari else False,meter=meter,price=price,city=city,
                                    location=location,title=title,detail=detail,publisher=publisher,
                                    user=self.request.user,parent=com_self,price_each_meter=price_each_meter
                                )
                                new_com.save()
                                if images:
                                    for img in images:
                                        i=CommericalImage(image=img,commerical=new_com)
                                        i.save()
                                new_com.save()

                    elif com_self.parent.title in ej:
                        vadieh=self.request.POST.get("vadieh")
                        ejareh=self.request.POST.get("ejareh") 
                        constuction_melk=self.request.POST.get("constuction_melk")
                        floor=self.request.POST.get("floor")

                        if com_self.parent.title == "اجاره اداری و تجاری":
                            sandEdari=self.request.POST.get("sandEdari",False)

                            new_com=Commerical(
                                sanad_adari=sandEdari,year_of_construction=constuction_melk,
                                floor=floor,rooms=rooms,parking=True if parking else False,
                                anbari=True if anbari else False,meter=meter,city=city,
                                location=location,title=title,detail=detail,publisher=publisher,
                                user=self.request.user,vadieh=vadieh,rent=ejareh,parent=com_self
                            )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                        else:
                            if com_self.title == "آپارتمان اجاره":
                                floor=self.request.POST.get("floor")
                                constuction_melk=self.request.POST.get("constuction_melk")

                                new_com=Commerical(year_of_construction=constuction_melk,
                                    floor=floor,rooms=rooms,parking=True if parking else False,
                                    anbari=True if anbari else False,meter=meter,city=city,
                                    location=location,title=title,detail=detail,publisher=publisher,
                                    user=self.request.user,vadieh=vadieh,rent=ejareh,parent=com_self
                                )
                                new_com.save()
                                if images:
                                    for img in images:
                                        i=CommericalImage(image=img,commerical=new_com)
                                        i.save()
                                new_com.save()
                            else:
                                constuction_melk=self.request.POST.get("constuction_melk")
                                new_com=Commerical(year_of_construction=constuction_melk,
                                    rooms=rooms,parking=True if parking else False,
                                    anbari=True if anbari else False,meter=meter,city=city,
                                    location=location,title=title,detail=detail,publisher=publisher,
                                    user=self.request.user,vadieh=vadieh,rent=ejareh,parent=com_self
                                )
                                new_com.save()
                                if images:
                                    for img in images:
                                        i=CommericalImage(image=img,commerical=new_com)
                                        i.save()
                                new_com.save()
                        
                    elif com_self.title == "اجاره کوتاه مدت":
                        day_rent_paid=self.request.POST.get("day_rent")
                        new_com=Commerical(
                                    rooms=rooms,
                                    meter=meter,city=city,
                                    location=location,title=title,detail=detail,publisher=publisher,
                                    user=self.request.user,day_rent_paid=day_rent_paid,parent=com_self
                                )
                        new_com.save()
                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()
                    else:
                        new_com=Commerical(
                                   meter=meter,city=city,
                                    location=location,title=title,detail=detail,publisher=publisher,
                                    user=self.request.user,parent=com_self
                                )
                        new_com.save()
                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()              
                
                case "وسایل نقلیه":

                    price_for_car=self.request.POST.get("price")
                    

                    if com_self.parent.title == "خودرو":

                        if com_self.title=="سواری و وانت":

                            production_year=self.request.POST.get("yearOfConstruction")
                            brand=self.request.POST.get("brand")
                            body_status=self.request.POST.get("body_status")
                            engin_type=self.request.POST.get("engin_type")
                            shasti_type=self.request.POST.get("shasti_type")
                            insurance_time=self.request.POST.get("insurance_time")
                            girbox=self.request.POST.get("girbox")
                            color=self.request.POST.get("color")
                            exchange=self.request.POST.get("exchange",False)
                            publisherForCar=self.request.POST.get("publisherForCar")
                            inter_or_exter=self.request.POST.get("inter_or_exter")
                            karkard=self.request.POST.get("karkard")
                            fuel_type=self.request.POST.get("fuel_type")

                            new_com=Commerical(
                                    price=price_for_car,city=city,production_year=production_year,brand_or_tip=brand,insurance_time=insurance_time,
                                    internal_or_external=inter_or_exter,karkard_mashin=karkard,ready_to_exchange=bool(exchange),fuel_type=fuel_type,
                                    location=location,title=title,detail=detail,publisherForCar=publisherForCar,body_type=body_status,
                                    user=self.request.user,girbox=girbox,color=color,engin_type=engin_type,shasti_type=shasti_type,parent=com_self
                                )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()
        
                        elif com_self.title == "سنگین":
                            karkard=self.request.POST.get("karkard")
                            exchange=self.request.POST.get("exchange",False)
                            publisherForCar=self.request.POST.get("publisherForCar")
                            color=self.request.POST.get("color")
                            

                            new_com=Commerical(
                                    price=price_for_car,city=city,color=color,
                                    karkard_mashin=karkard,ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,publisherForCar=publisherForCar,
                                    user=self.request.user,parent=com_self
                                )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                        elif  com_self.title=="کلاسیک":
                            exchange=self.request.POST.get("exchange",False)
                            publisherForCar=self.request.POST.get("publisherForCar")
                            color=self.request.POST.get("color")

                            new_com=Commerical(
                                    price=price_for_car,city=city,ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,publisherForCar=publisherForCar,
                                    user=self.request.user,parent=com_self,color=color
                                )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                        elif com_self.title=="اجاره‌ای":
                            exchange=self.request.POST.get("exchange",False)
                            publisherForCar=self.request.POST.get("publisherForCar")
                            color=self.request.POST.get("color")

                            new_com=Commerical(
                                    day_rent_paid=price_for_car,city=city,ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,publisherForCar=publisherForCar,
                                    user=self.request.user,parent=com_self,color=color
                                )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                case "کالای دیجیتال":

                    price_for_digital=self.request.POST.get("price")

                    if com_self.parent.title =="موبایل و تبلت":
                        
                        if com_self.title =="موبایل":

                            simCartNums=self.request.POST.get("simCartNums")
                            esalet=self.request.POST.get("esalet")
                            phone_brand=self.request.POST.get("phone_brand")
                            memory_size=self.request.POST.get("memory_size")
                            ram_size=self.request.POST.get("ram_size")
                            color=self.request.POST.get("color")
                            phone_status=self.request.POST.get("phone_status")
                            exchange=self.request.POST.get("exchange",False)

                            new_com=Commerical(
                                    price=price_for_digital,city=city,color=color,phone_status=phone_status,
                                    ready_to_exchange=bool(exchange),memory_size=memory_size,
                                    location=location,title=title,detail=detail,esalat=esalet,ram_size=ram_size,
                                    user=self.request.user,sim_cart_number=simCartNums,brand_or_tip=phone_brand,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                        elif com_self.title =="تبلت":

                            window_size=self.request.POST.get("window_size")
                            esalet=self.request.POST.get("esalet")
                            phone_brand=self.request.POST.get("phone_brand")
                            memory_size=self.request.POST.get("memory_size")
                            ram_size=self.request.POST.get("ram_size")
                            color=self.request.POST.get("color")
                            phone_status=self.request.POST.get("phone_status")
                            os_type=self.request.POST.get("os_type")
                            cover_simcart=self.request.POST.get("cover_simcart")
                            exchange=self.request.POST.get("exchange",False)


                            new_com=Commerical(
                                    price=price_for_digital,city=city,color=color,phone_status=phone_status,window_size=window_size,
                                    ready_to_exchange=bool(exchange),memory_size=memory_size,
                                    location=location,title=title,detail=detail,esalat=esalet,ram_size=ram_size,
                                    user=self.request.user,brand_or_tip=phone_brand,os_typpe=os_type,cover_simcart=cover_simcart,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                        elif com_self.title == "سیم کارت":

                            simcart_type=self.request.POST.get('simcart_type')
                            phone_status=self.request.POST.get("phone_status")
                            exchange=self.request.POST.get("exchange",False)

                            new_com=Commerical(
                                    price=price_for_digital,city=city,phone_status=phone_status,
                                    ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,simcartType=simcart_type,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()
                        
                        else:
                            phone_status=self.request.POST.get("phone_status")
                            exchange=self.request.POST.get("exchange",False)

                            new_com=Commerical(
                                    price=price_for_digital,city=city,phone_status=phone_status,
                                    ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()
                        
                    elif com_self.parent.title=="رایانه":

                        if com_self.title == "رایانه همراه" or com_self.title == "رایانه رومیزی":

                            window_size=self.request.POST.get("window_size")
                            esalet=self.request.POST.get("esalet")
                            phone_brand=self.request.POST.get("phone_brand")
                            memory_size=self.request.POST.get("memory_size")
                            ram_size=self.request.POST.get("ram_size")
                            color=self.request.POST.get("color")
                            phone_status=self.request.POST.get("phone_status")
                            os_type=self.request.POST.get("os_type")
                            cover_simcart=self.request.POST.get("cover_simcart")
                            exchange=self.request.POST.get("exchange",False)


                            new_com=Commerical(
                                    price=price_for_digital,city=city,color=color,phone_status=phone_status,window_size=window_size,
                                    ready_to_exchange=bool(exchange),memory_size=memory_size,
                                    location=location,title=title,detail=detail,esalat=esalet,ram_size=ram_size,
                                    user=self.request.user,brand_or_tip=phone_brand,os_typpe=os_type,cover_simcart=cover_simcart,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                        else:
                            
                            phone_status=self.request.POST.get("phone_status")
                            exchange=self.request.POST.get("exchange",False)
                            new_com=Commerical(
                                    price=price_for_digital,city=city,phone_status=phone_status,
                                    ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()
                    
                    elif com_self.parent.title == "صوتی و تصویری":
                            phone_status=self.request.POST.get("phone_status")
                            exchange=self.request.POST.get("exchange",False)
                            new_com=Commerical(
                                    price=price_for_digital,city=city,phone_status=phone_status,
                                    ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,parent=com_self
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                case "خانه و آشپزخانه":
                    phone_status=self.request.POST.get("phone_status")
                    exchange=self.request.POST.get("exchange",False)
                    price_for_kitchen=self.request.POST.get("price")

                    new_com=Commerical(
                                    price=price_for_kitchen,city=city,phone_status=phone_status,
                                    ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,parent=com_self
                                )

                    new_com.save()
                    if images:
                        for img in images:
                            i=CommericalImage(image=img,commerical=new_com)
                            i.save()
                    new_com.save()

                case "وسایل شخصی":

                    if com_self.parent.title=="کیف، کفش و لباس" or com_self.parent.title == "زیورآلات و اکسسوری":

                        phone_status=self.request.POST.get("phone_status")
                        exchange=self.request.POST.get("exchange",False)
                        price_for_personal=self.request.POST.get("price")
                        male_or_female=self.request.POST.get("male_or_female")

                        new_com=Commerical(
                                        price=price_for_personal,city=city,phone_status=phone_status,
                                        ready_to_exchange=bool(exchange),
                                        location=location,title=title,detail=detail,
                                        user=self.request.user,parent=com_self,cloths_type=male_or_female
                                    )

                        new_com.save()
                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()

                    elif com_self.parent.title == "وسایل بچه و اسباب بازی":

                        phone_status=self.request.POST.get("phone_status")
                        exchange=self.request.POST.get("exchange",False)
                        price_for_personal=self.request.POST.get("price")
                      

                        new_com=Commerical(
                                        price=price_for_personal,city=city,phone_status=phone_status,
                                        ready_to_exchange=bool(exchange),
                                        location=location,title=title,detail=detail,
                                        user=self.request.user,parent=com_self
                                    )

                        new_com.save()
                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()
                
                case "سرگرمی و فراغت" | "اجتماعی" | "تجهیزات و صنعتی":
   
                        exchange=self.request.POST.get("exchange",False)
                        price_for_entertaiment=self.request.POST.get("price")
    
                        new_com=Commerical(
                                        price=price_for_entertaiment,city=city,
                                        ready_to_exchange=bool(exchange),
                                        location=location,title=title,detail=detail,
                                        user=self.request.user,parent=com_self,
                                    )

                        new_com.save()
                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()

  


        else:

            parent_title_second_level=self.request.POST.get("parent_title")
            com_id_two_level=self.request.POST.get("self_id")
            
            com_self_two_level=get_object_or_404(Commerical,id=com_id_two_level)


            match parent_title_second_level:
                case "وسایل نقلیه":
                    price_for_second_transportation=self.request.POST.get("price")

                    if com_self_two_level.title == "موتور سیکلت":

                            production_year=self.request.POST.get("yearOfConstruction")
                            brand=self.request.POST.get("brand")
                            exchange=self.request.POST.get("exchange",False)
                            publisherForCar=self.request.POST.get("publisherForCar")
                            karkard=self.request.POST.get("karkard")

                            new_com=Commerical(
                                    price=price_for_second_transportation,city=city,production_year=production_year,brand_or_tip=brand,
                                    karkard_mashin=karkard,ready_to_exchange=bool(exchange),
                                    location=location,title=title,detail=detail,publisherForCar=publisherForCar,
                                    user=self.request.user,parent=com_self_two_level
                                )
                            new_com.save()
                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()
                    else:
                        exchange=self.request.POST.get("exchange",False)
                        publisherForCar=self.request.POST.get("publisherForCar")

                        new_com=Commerical(
                                    price=price_for_second_transportation,city=city
                                    ,ready_to_exchange=bool(exchange),publisherForCar=publisherForCar,
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,parent=com_self_two_level
                                )
                        new_com.save()
                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()
                case "کالای دیجیتال":
                    
                    price_for_digital=self.request.POST.get("price")

                    if com_self_two_level.title == "کنسول" or com_self_two_level.title == "تلفن رومیزی":

                            phone_status=self.request.POST.get("phone_status")
                            exchange=self.request.POST.get("exchange",False)

                            new_com=Commerical(
                                    price=price_for_digital,city=city,phone_status=phone_status,
                                    ready_to_exchange=Tbool(exchange),
                                    location=location,title=title,detail=detail,
                                    user=self.request.user,parent=com_self_two_level
                                )

                            new_com.save()

                            if images:
                                for img in images:
                                    i=CommericalImage(image=img,commerical=new_com)
                                    i.save()
                            new_com.save()

                    
                case "خانه و آشپزخانه":

                        price_for_kitchen=self.request.POST.get("price")
                        phone_status=self.request.POST.get("phone_status")
                        exchange=self.request.POST.get("exchange",False)

                        new_com=Commerical(
                                price=price_for_kitchen,city=city,phone_status=phone_status,
                                ready_to_exchange=bool(exchange),
                                location=location,title=title,detail=detail,
                                user=self.request.user,parent=com_self_two_level
                            )

                        new_com.save()

                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()

                case "خدمات":

                        new_com=Commerical(
                              city=city,
                                location=location,title=title,detail=detail,
                                user=self.request.user,parent=com_self_two_level
                            )

                        new_com.save()

                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()
                

                case "وسایل شخصی":

                    if com_id_two_level.title == "آرایشی، بهداشتی و درمانی" or com_id_two_level.title=="لوازم التحریر":
                        
                        price_for_personal=self.request.POST.get("price")
                        phone_status=self.request.POST.get("phone_status")
                        exchange=self.request.POST.get("exchange",False)

                        new_com=Commerical(
                                city=city,price=price_for_personal,phone_status=phone_status,
                                location=location,title=title,detail=detail,ready_to_exchange=bool(exchange),
                                user=self.request.user,parent=com_self_two_level
                            )

                        new_com.save()

                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()

                case "سرگرمی و فراغت" | "تجهیزات و صنعتی":

                        price_for_entertaiment=self.request.POST.get("price")
                        exchange=self.request.POST.get("exchange",False)

                        new_com=Commerical(
                                city=city,price=price_for_entertaiment,
                                location=location,title=title,detail=detail,ready_to_exchange=bool(exchange),
                                user=self.request.user,parent=com_self_two_level
                            )

                        new_com.save()

                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()

                case "استخدام و کاریابی":
                        insurance=self.request.POST.get("insurance",False)
                        pendding_type=self.request.POST.get("pendding_type")
                        work_type=self.request.POST.get("work_type")
                        sabegheh=self.request.POST.get("sabegheh")
                        soldier=self.request.POST.get("soldier",False)
                        farWork=self.request.POST.get("farWork",False)
                        salary=self.request.POST.get("salary",False)
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        print(insurance,bool(insurance),)
                        print(soldier)
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
                  

                        new_com=Commerical(
                                city=city,
                                location=location,title=title,detail=detail,insurance=bool(insurance) ,salary=salary,
                                how_we_pay=pendding_type,how_college_are=work_type,price_for_work=sabegheh,
                                soldier=bool(soldier),farWork=bool(farWork),
                                user=self.request.user,parent=com_self_two_level
                            )

                        new_com.save()

                        if images:
                            for img in images:
                                i=CommericalImage(image=img,commerical=new_com)
                                i.save()
                        new_com.save()


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



