#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from .models import Commerical,City,SmallCity
import json
from django.http import JsonResponse
from django.db.models import Q

def categories(request):
    
    aaa=request.session.get("city_name2",1)
    ci=City.objects.get(id=int(aaa))
    # print(ci)

    coms=Commerical.objects.filter(
        
        parent=None
        
    )
  

    cits=City.objects.all().values_list("name")

    comps=[''.join(i) for i in cits]

    city_choosen=request.path.replace("/","")
    
    
    flag=False
    if city_choosen in comps:
        flag=True
    


 

    # print(coms)
    return {
        'cats2':coms,
       "flag":flag
    }


def allCities(request):
    
    p=request.session.get("bb")
    items=request.session.get("min")


    

    city_to_show=''
    count=0
    c=None
    sm=None

    just_one_city=None
    second_one_city=None

    if p:

        if len(p)==1 and not items:
            just_one_city=City.objects.get(id=int(p[0]))
            city_to_show=just_one_city.name
            

        elif len(p)==1 and items:
            second_one_city=City.objects.get(id=int(p[0]))
            sm=SmallCity.objects.filter(
                id__in=[int(i) for i in items]
            )
            print("SSMSMSMSMS",sm)
            count+=(sm.count()+1)
            print("here 2")
      


        elif type(p) !=int and not items:

            c=City.objects.filter(
                id__in=[int(i) for i in p]
            )

            count+=c.count()
            print("third")
       
        elif type(p)!= int and items:
            c=City.objects.filter(
                id__in=[int(i) for i in p]
            )
            sm=SmallCity.objects.filter(
                id__in=[int(i) for i in items]
            )
            count+=c.count()+sm.count()
            print("fourththhtht")
            
    elif not p and items:

            sm=SmallCity.objects.filter(
                id__in=[int(i) for i in items]
            )
            print("LASSASATATASTASTAS")

    

    # print("@@@@@@@@@@@@@@")
    # print("@@@@@@@@@@@@@@")
    
    # print("@@@@@@@@@@@@@@")
    # print("@@@@@@@@@@@@@@")

    

    show_result=None
    if count:
        show_result=count
    else:
        show_result=city_to_show

    
    
    alls=City.objects.all()
    x=[]
    for i in alls:
        x.append({
            "name":i.name,
            "minis":[{"name":j.name,"id":j.id} for j in i.smallcity_set.all()],
            "cityId":i.id
        })
    
    
    return {
        'all_city':json.dumps(x),
        'cities':alls,
        'show_result':show_result,
        'city_to_send':c,
        'mini_city_to_send':sm ,
        'just_one_city':just_one_city ,
        'second_one_city':second_one_city,
    }

