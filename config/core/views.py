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

from .utilty import (findTimeDiffrence,title_not_to_be,
                     three_level_parent,
                     two_level_parent,
                     two_and_three_parent,
                     filteramlak_groupA,
                     filteramlak_groupB

                     )
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core import serializers




def lcoationIdsssss():
    return [i.id for i in Location.objects.all()]
    





class CityView(View):
    
    
    def get(self,request,*args,**kwargs):

        all_citites=City.objects.all()
        
        if self.request.session.get("city_name2",None):
            del self.request.session["city_name2"]
        
        

        contex={
            'cities':all_citites
        }

        return render(request,"main/index.html",contex)

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

        print(filtred_coms,"FFFIILLFLFLFLLFLFL")

        

        

  
        

        contex={

            'cities':ci,
            'coms':filtred_coms,
            'all_cats':all_cats,
            
        }
      
        
        return render(request,"core/after_search_city.html",contex)
    



def eachCategory(request,categoryId):

    cat=get_object_or_404(Commerical,id=categoryId)
    

    cat_childs=cat.children.all()

    province=request.session.get("bb")
    smallCities=request.session.get("min")

      

    coms_to_show=None
    
    if cat.title in three_level_parent:
        print("MOOOOOOOOOOOOOOOOOWWW")
        print("MOOOOOOOOOOOOOOOOOWWW")
        print("MOOOOOOOOOOOOOOOOOWWW")

        if province and smallCities:
            print("SEOCCCCCCCCCCCCC")
            print("SEOCCCCCCCCCCCCC")
            print("SEOCCCCCCCCCCCCC")
            print("SEOCCCCCCCCCCCCC")

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
        'cits':cits
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
        print("FIRSTTT _TOOOCHHEDD")
        
        if province and smallCities:
            print("noooooooooooooooooooooooooooooooo")
            print("noooooooooooooooooooooooooooooooo")
            print("noooooooooooooooooooooooooooooooo")
            print("noooooooooooooooooooooooooooooooo")

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
                Q(parent__parent__title=cat.parent.title) &
                Q(parent__title=cat.title)
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

        elif not province and smallCities:

            coms_to_show=Commerical.objects.filter(
                
                Q(smallCity__in=[int(i) for i in smallCities])
                

            ).filter(
                Q(parent__parent__parent__title=cat.parent.title) & 
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

    


    print(coms_to_show,"COOMMMM")
    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )

    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
        'cits':cits,
        'coms_to_show':coms_to_show
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

    

    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
        'coms_to_show':coms_to_show
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
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(justImg,type(justImg),"TTYYP")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$")

    

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
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(least_price,max_price))
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
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(least_price,max_price))
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
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(least_price,max_price))
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
                    Q(price__range=(least_price,max_price))
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
                    Q(location__in=locas_to_go)
                ).filter(
                    Q(price__range=(least_price,max_price))
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
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(least_price,max_price))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                        com_status=instatnceComs
                    ).distinct()



    print(coms_to_show,"CCPPOSOCOASCASFAFSAFASFASDASD")
    cat=get_object_or_404(Commerical,title="املاک")
    cat_childs=cat.children.all()
    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )
    print(bool(justImg),"IIMAGESSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    print("^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^")
    print(type(max_price))
    print(least_price)
    print("^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^")
    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
        'coms_to_show':coms_to_show,
        'cits':cits,
        'justImg':bool(justImg),
        'instatnceComs':instatnceComs,
        'least_price':int(least_price),
        'max_price':int(max_price)

        
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
    parent_parent_title=request.GET.get("parent_parent_title")

    


    

    least_price=request.GET.get("least_price",0)
    max_price=request.GET.get("max_price",400000000)

    maxMeter=request.GET.get("maxMeter",200)
    leastMeter=request.GET.get("leastMeter",0)

    maxVadieh=request.GET.get("maxVadieh",900)
    minVadieh=request.GET.get("minVadieh",0)

    maxEjareh=request.GET.get("maxEjareh",8)
    minEjareh=request.GET.get("minEjareh",0)
    





    locas_to_go=list(map(

            lambda x:int(x),locationIds.split(",")
            if len(locationIds)>=1 else defaultLocalIds
        ))

    coms_to_show=None
    if parent_parent_title in filteramlak_groupA:
        print('TYPYPYPYPYPPe OONOOONONONONONON')


        if province and smallCities:
                print("COCOCOCOCOTTINUEE")
          
                if bool(justImg):
                    print("WIWIIWIWIWI IMAGGEHEGEGEGEGEGE")


                    coms_to_show=Commerical.objects.annotate(
                        img_length=Length("commericalimage")
                    ).filter(
                            Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__parent__title="املاک") &
                            Q(location__in=locas_to_go)
                        ).filter(

                            Q(price__range=(int(least_price),int(max_price))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter))) 
                            
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__parent__title="املاک") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price)))& 
                            Q(meter__range=(int(leastMeter),int(maxMeter))) 
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
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
                        Q(price__range=(int(least_price),int(max_price)))&
                        Q(meter__range=(int(leastMeter),int(maxMeter)))

                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(price__range=(int(least_price),int(max_price)))& 
                        Q(meter__range=(int(leastMeter),int(maxMeter)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
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
                        Q(price__range=(int(least_price),int(max_price)))&
                        Q(meter__range=(int(leastMeter),int(maxMeter)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__parent__title="املاک") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(price__range=(int(least_price),int(max_price)))& 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()



    elif parent_parent_title in filteramlak_groupB:
        print("CCCCCCCLLALLALALEDLDLDLLDDLD")
        if province and smallCities:
          
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

                            Q(vadieh__range=(int(minVadieh),int(maxVadieh))) & 
                            Q(meter__range=(int(leastMeter),int(maxMeter))) &
                            Q(rent__range=(int(minEjareh),int(maxEjareh)))
                            
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            img_length__gte=1
                        ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()
                else:
                    print("ELLLLLLLLLLLSSSSSSSSSSSSSSSSSSSSSS")
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) | 
                            Q(smallCity__in=[int(i) for i in smallCities]) 
                        ).filter(
                            Q(parent__parent__parent__title="املاک") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))& 
                            Q(meter__range=(int(leastMeter),int(maxMeter))) &
                            Q(rent__range=(int(minEjareh),int(maxEjareh)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
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
                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                        Q(rent__range=(int(minEjareh),int(maxEjareh)))

                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                        Q(city__in=[int(i) for i in province]) &
                        Q(parent__parent__parent__title="املاک") &
                        Q(location__in=locas_to_go)
                    ).filter(
                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))& 
                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                        Q(rent__range=(int(minEjareh),int(maxEjareh)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
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
                        Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
                        Q(meter__range=(int(leastMeter),int(maxMeter)))&
                        Q(rent__range=(int(minEjareh),int(maxEjareh)))
                    ).filter(
                        ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                    ).filter(
                            img_length__gte=1
                    ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()
                else:
                    coms_to_show=Commerical.objects.filter(
                            Q(smallCity__in=[int(i) for i in smallCities])&
                            Q(parent__parent__parent__title="املاک") &
                            Q(location__in=locas_to_go)
                        ).filter(
                            Q(vadieh__range=(int(minVadieh),int(maxVadieh)))& 
                            Q(meter__range=(int(leastMeter),int(maxMeter)))&
                            Q(rent__range=(int(minEjareh),int(maxEjareh)))
                        ).filter(
                            ~Q(parent=None) & ~Q(title__in=title_not_to_be)
                        ).filter(
                            com_status=instatnceComs
                        ).filter(
                            Q(parent__parent__title=parent_parent_title)
                        ).distinct()






    cat=get_object_or_404(Commerical,title=parent_parent_title)
    cat_childs=cat.children.all()
    cits=City.objects.filter(
        id__in=[int(i) for i in province]
    )

    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
        'coms_to_show':coms_to_show,
        'cits':cits,
        'justImg':bool(justImg),
        'instatnceComs':instatnceComs,
        'least_price':int(least_price) if least_price != "undefined" else 0,
        'max_price':int(max_price) if max_price !="undefined" else 200,
        'maxmeter':int(maxMeter),
        'leastMeter':int(leastMeter),
        'maxVadieh':int(maxVadieh),
        'minVadieh':int(minVadieh),
        'maxEjareh':int(maxEjareh),
        'minEjareh':int(minEjareh),


        
    }

    return render(request,"core/handleAmlakFilterSecondLevel.html",contex)











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
