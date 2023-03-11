from django.shortcuts import render,get_object_or_404,redirect
from .models import (Commerical,SavedCommerical,
                    SmallCity,City,Thread,Message,
                    Feature,Tag,Location
                    )
from django.contrib import messages
from django.views import View
from django.views.generic import ListView,UpdateView,DetailView
from django.db.models import Q,F
from datetime import datetime
from jalali_date import datetime2jalali
from django.utils import timezone

from .utilty import (findTimeDiffrence,title_not_to_be,
                     three_level_parent,
                     two_level_parent,
                     two_and_three_parent
                     )
from django.http import JsonResponse

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


    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
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

    # locs=lcoationIdsssss()

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
    print("#########################")
    print("#########################")
    print("#########################")
    print("#########################")
    print(defaultLocalIds)
    print(len(locationIds))
    print("#########################")
    print("#########################")
    print("#########################")
    print("#########################")

    least_price=request.GET.get("least_price",0)
    max_price=request.GET.get("max_price",400000000)

    locas_to_go=list(map(

            lambda x:int(x),locationIds.split(",")
            if len(locationIds)>=1 else defaultLocalIds
        ))

    coms_to_show=None

    print(locas_to_go)

    if province and smallCities:
            print("A")
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
            ).distinct()

    elif province and not smallCities:
            print("B")
            coms_to_show=Commerical.objects.filter(
                Q(city__in=[int(i) for i in province]) &
                Q(parent__parent__parent__title="املاک") &
                Q(location__in=locas_to_go)
            ).filter(
                Q(price__range=(least_price,max_price))
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

    elif not province and smallCities:
            print("C")
            coms_to_show=Commerical.objects.filter(
                Q(smallCity__in=[int(i) for i in smallCities])&
                Q(parent__parent__parent__title="املاک") &
                Q(location__in=locas_to_go)
            ).filter(
                Q(price__range=(least_price,max_price))
            ).filter(
                ~Q(parent=None) & ~Q(title__in=title_not_to_be)
            ).distinct()

    print(coms_to_show,"CCPPOSOCOASCASFAFSAFASFASDASD")
    cat=get_object_or_404(Commerical,title="املاک")
    cat_childs=cat.children.all()

    
    contex={
        'cat_childs':cat_childs,
        'catMain':cat,
        'coms_to_show':coms_to_show,
        
    }

    return render(request,"core/AmlakAfterFilter.html",contex)



class CommericalDetail(View):

    def get(self,request,comId,*args,**kwargs):

        com=get_object_or_404(Commerical,id=comId)
        