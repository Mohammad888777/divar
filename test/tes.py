# # from datetime import datetime
# # # from jalali_date import datetime2jalali
# # # from django.utils import timezone
# # a = '220044'
# # b = '180022'
# # time1 = datetime.strptime(a,"%H%M%S") # convert string to time
# # time2 = datetime.strptime(b,"%H%M%S") 
# # diff = time1 -time2
# # a=diff.total_seconds()/3600 
# # print(a)



# # # # to_irani_now=datetime2jalali(timezone.now())
# # # last=Commerical.objects.last()

# # # value=last.iranTimeCreated

# # # time_to_go=''

# # # to_irani_now=datetime2jalali(timezone.now())


# # # if  to_irani_now.year - value.year ==0:

# # #     if to_irani_now.month - value.month==0:
        
# # #         if to_irani_now.day-value.day ==0:
# # #             if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<1:
# # #                 if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=5:
# # #                     time_to_go="لحظاتی پیش"
# # #                 elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=10:
# # #                     time_to_go="دقایقی پیش"

# # #                 elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=15:
# # #                     time_to_go="یک ربع پیش"
                
# # #                 elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=59:
# # #                     time_to_go="نیم ساعت پیش"
                    
# # #             if 1<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<2:
# # #                 time_to_go="یک ساعت پیش"

# # #             elif 2<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<3:
# # #                 time_to_go="دو ساعت پیش"
            
# # #             elif 3<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<4:
# # #                 time_to_go="سه ساعت پیش"

# # #             elif 4<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<5:
# # #                 time_to_go="چهار ساعت پیش"
# # #             elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<6:
# # #                 time_to_go="پنج ساعت پیش"
            
# # #             elif 6<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<7:
# # #                 time_to_go="شش ساعت پیش"
            
# # #             elif 7<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<8:
# # #                 time_to_go="هفت ساعت پیش"
            
# # #             elif 8<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<9:
# # #                 time_to_go="هشت ساعت پیش"

# # #             elif 9<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<10:
# # #                 time_to_go="نه ساعت پیش"
# # #             elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<11:
# # #                 time_to_go="ده ساعت پیش"
# # #             elif 11<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<12:
# # #                 time_to_go="یازده ساعت پیش"
# # #             elif 12<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<13:
# # #                 time_to_go="دوازده ساعت پیش"
# # #             elif 13<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<14:
# # #                 time_to_go="سیزده ساعت پیش"
            
# # #             elif 14<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<15:
# # #                 time_to_go="چهارده ساعت پیش"
            
# # #             elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<16:
# # #                 time_to_go="پانزده ساعت پیش"
            
# # #             elif 16<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<17:
# # #                 time_to_go="شانزده ساعت پیش"
            
# # #             elif 17<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<18:
# # #                 time_to_go="هفده ساعت پیش"

# # #             elif 18<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<19:
# # #                 time_to_go="هجده ساعت پیش"
# # #             elif 19<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<20:
# # #                 time_to_go="نوزده ساعت پیش"
# # #             elif 20<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<21:
# # #                 time_to_go="بیست ساعت پیش"
# # #             elif 21<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<22:
# # #                 time_to_go="بیست و یک ساعت پیش"
# # #             elif 22<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<23:
# # #                 time_to_go="بیست و دو ساعت پیش"
            
# # #             elif 23<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<24:
# # #                 time_to_go="بیست و سه ساعت پیش"
# # #         elif to_irani_now.day-value.day==1:
# # #             time_to_go ="دیروز"

# # #         elif to_irani_now.day-value.day==2:
# # #             time_to_go ="پریروز"
        
# # #         elif to_irani_now.day-value.day==3:
# # #             time_to_go ="سه روز پیش"
# # #         elif to_irani_now.day-value.day==4:
# # #             time_to_go ="چهار روز پیش"
        
# # #         elif to_irani_now.day-value.day==5:
# # #             time_to_go ="پنج روز پیش"
# # #         elif to_irani_now.day-value.day==6:
# # #             time_to_go ="شش روز پیش"
# # #         elif 6<to_irani_now.day-value.day<14:
# # #             time_to_go =" یک هفته پیش"
# # #         elif 14<=to_irani_now.day-value.day<20:
# # #             time_to_go =" دو هفته پیش"
        
# # #         elif 20<=to_irani_now.day-value.day<28:
# # #             time_to_go =" سه هفته پیش"
        
# # #         elif 28<=to_irani_now.day-value.day<=31:
# # #             time_to_go =" چهار هفته پیش"
# # #     elif to_irani_now.month -value.month ==1:
# # #         time_to_go="یک ماه پیش"

# # # a=findTimeDiffrence(timezone.now(),value).total_seconds()/3600
# # # print(a)
# # # print(time_to_go)


# # text = "چرا کار نمیکنی؟" .encode("utf-8")# also using u"...." results the same
# # print(text)
# # import persian
# # print(persian.convert_ar_characters("علي") )
# # a="شیراز"

# # import os

# # a=[{"id":1,"name":"d"},{"id":1,"name":"fff"},{"id":4,"name":"d"}]
# # a.sort(key=lambda x:x["id"])
# # f=[]
# # for i in a:
# #     if i["id"] not in f:
# #         f.append(i["id"])
# # print(f)

# # a="True"
# # print(bool(a))
# # b="False"
# # print(bool(b))
# a=45
# match a:
#     case 88:
#         print("asd")
#     case 1 | 45:
#         print("orrr")
# a=[i for i in range(1,11)]
# b=[i for i in range(11,21)]
# c=[i for i in range(21,31)]
# c=7

# Q(farWork=True)&
# Q(soldier=True)&
# Q(insurance=True)&
# Q(price_for_work__range=(int(choose_min_price_for_work),int(choose_max_price_for_work)))
# if anbari:

#                                 coms_to_show=Commerical.objects.filter(
#                                         Q(city__in=[int(i) for i in province]) | 
#                                             Q(smallCity__in=[int(i) for i in smallCities]) 
#                                         ).filter(
#                                             Q(parent__parent__title=title) &
#                                             Q(location__in=locas_to_go)
#                                         ).filter(
#                                             Q(anbari=True)&
#                                             Q(parking=True)&
#                                             Q(price__range=(int(least_price),int(max_price)))&
#                                             Q(rooms__gte=roomNumber)&
#                                             Q(meter__range=(int(leastMeter),int(leastMeter)))&
#                                             Q(publisher=publisherForAmlak)&
#                                             Q(floor__gte=floor)   
#                                         ).filter(
#                                             ~Q(parent=None) & ~Q(title__in=title_not_to_be)
#                                         ).filter(
#                                             com_status=instatnceComs
#                                         ).distinct()
#                         # else for anbari
#                         else:
#                             coms_to_show=Commerical.objects.filter(
#                                         Q(city__in=[int(i) for i in province]) | 
#                                             Q(smallCity__in=[int(i) for i in smallCities]) 
#                                         ).filter(
#                                             Q(parent__parent__title=title) &
#                                             Q(location__in=locas_to_go)
#                                         ).filter(
#                                             Q(parking=True)&
#                                             Q(price__range=(int(least_price),int(max_price)))&
#                                             Q(rooms__gte=roomNumber)&
#                                             Q(meter__range=(int(leastMeter),int(leastMeter)))&
#                                             Q(publisher=publisherForAmlak)&
#                                             Q(floor__gte=floor)   
#                                         ).filter(
#                                             ~Q(parent=None) & ~Q(title__in=title_not_to_be)
#                                         ).filter(
#                                             com_status=instatnceComs
#                                         ).distinct()





# Q(anbari=True)&
# Q(parking=True)&
# Q(rooms__gte=roomNumber)&
# Q(meter__range=(int(leastMeter),int(leastMeter)))&
# Q(publisher=publisherForAmlak)&
# Q(floor__gte=floor)&
# Q(vadieh__range=(int(minVadieh),int(maxVadieh)))&
# Q(rent__range=(int(minEjareh),int(maxEjareh)))


# coms_to_show=Commerical.objects.annotate(
#                                     img_length=Length("commericalimage")
#                                     ).filter(
#                                         Q(city__in=[int(i) for i in province]) &
#                                         Q(parent__title=title) &
#                                         Q(location__in=locas_to_go)
#                                     ).filter(
#                                             Q(price__range=(int(least_price),int(max_price)))&
#                                             Q(publisherForCar=publisherForCar)&
#                                             Q(exchange=True)&
#                                             Q(internal_or_external=internalOrExternal)&
#                                             Q(color=color)&
#                                             Q(karkard_mashin__range=(int(minKarkard),int(maxKarkard)))&
#                                             Q(production_year__range=(int(minYearOfConstruction),int(maxYearOfConstruction)))   
#                                     ).filter(
#                                         ~Q(parent=None) & ~Q(title__in=title_not_to_be)
#                                     ).filter(
#                                             img_length__gte=1
#                                     ).filter(
#                                             com_status=instatnceComs
#                                         ).distinct()





# Q(price__range=(int(least_price),int(max_price)))&
# Q(phone_status=phoneStatus)&
# Q(esalat=esalat)&
# Q(sim_cart_number__gte=simcartNums)&
# Q(color=color)&
# Q(memory_size__gte=memorySize)&
# Q(cover_simcart=coverSimcart)&
# Q(exchange=True)

# coms_to_show=Commerical.objects.annotate(
#                             img_length=Length("commericalimage")
#                             ).filter(
#                                 Q(city__in=[int(i) for i in province]) &
#                                 Q(parent__parent__title=title) &
#                                 Q(location__in=locas_to_go)
#                             ).filter(
#                                     Q(price__range=(int(least_price),int(max_price)))&
#                                     Q(simcartType=simcartType)&
#                                     Q(exchange=True)   
#                             ).filter(
#                                 ~Q(parent=None) & ~Q(title__in=title_not_to_be)
#                             ).filter(
#                                     img_length__gte=1
#                             ).filter(
#                                     com_status=instatnceComs
#                                 ).distinct()
# Q(price__range=(int(least_price),int(max_price))) &
# Q(exchange=True) 


# Q(parking=True)&
#                                             Q(price__range=(int(least_price),int(max_price)))&
#                                             Q(rooms__gte=roomNumber)&
#                                             Q(meter__range=(int(leastMeter),int(leastMeter)))&
#                                             Q(publisher=publisherForAmlak)&
#                                             Q(floor__gte=floor)  


a=99
b="hello" if a==5 else 7|2
print(b)