from django import template
from jalali_date import datetime2jalali
from django.utils import timezone
from ..utilty import findTimeDiffrence


register=template.Library()




@register.filter(expects_localtime=True)
def findTime(value):

        time_to_go=''

        to_irani_now=datetime2jalali(timezone.now())


        if  to_irani_now.year - value.year ==0:

            if to_irani_now.month - value.month==0:
                
                if to_irani_now.day-value.day ==0:
                    if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<1:
                        if 0<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=5:
                            time_to_go="لحظاتی پیش"
                        elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=10:
                            time_to_go="دقایقی پیش"

                        elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=15:
                            time_to_go="یک ربع پیش"
                        
                        elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/60 <=59:
                            time_to_go="نیم ساعت پیش"
                            
                    if 1<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<2:
                        time_to_go="یک ساعت پیش"

                    elif 2<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<3:
                        time_to_go="دو ساعت پیش"
                    
                    elif 3<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<4:
                        time_to_go="سه ساعت پیش"

                    elif 4<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<5:
                        time_to_go="چهار ساعت پیش"
                    elif 5<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<6:
                        time_to_go="پنج ساعت پیش"
                    
                    elif 6<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<7:
                        time_to_go="شش ساعت پیش"
                    
                    elif 7<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<8:
                        time_to_go="هفت ساعت پیش"
                    
                    elif 8<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<9:
                        time_to_go="هشت ساعت پیش"

                    elif 9<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<10:
                        time_to_go="نه ساعت پیش"
                    elif 10<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<11:
                        time_to_go="ده ساعت پیش"
                    elif 11<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<12:
                        time_to_go="یازده ساعت پیش"
                    elif 12<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<13:
                        time_to_go="دوازده ساعت پیش"
                    elif 13<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<14:
                        time_to_go="سیزده ساعت پیش"
                    
                    elif 14<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<15:
                        time_to_go="چهارده ساعت پیش"
                    
                    elif 15<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<16:
                        time_to_go="پانزده ساعت پیش"
                    
                    elif 16<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<17:
                        time_to_go="شانزده ساعت پیش"
                    
                    elif 17<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<18:
                        time_to_go="هفده ساعت پیش"

                    elif 18<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<19:
                        time_to_go="هجده ساعت پیش"
                    elif 19<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<20:
                        time_to_go="نوزده ساعت پیش"
                    elif 20<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<21:
                        time_to_go="بیست ساعت پیش"
                    elif 21<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<22:
                        time_to_go="بیست و یک ساعت پیش"
                    elif 22<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<23:
                        time_to_go="بیست و دو ساعت پیش"
                    
                    elif 23<=findTimeDiffrence(timezone.now(),value).total_seconds()/3600<24:
                        time_to_go="بیست و سه ساعت پیش"
                elif to_irani_now.day-value.day==1:
                    time_to_go ="دیروز"

                elif to_irani_now.day-value.day==2:
                    time_to_go ="پریروز"
                
                elif to_irani_now.day-value.day==3:
                    time_to_go ="سه روز پیش"
                elif to_irani_now.day-value.day==4:
                    time_to_go ="چهار روز پیش"
                
                elif to_irani_now.day-value.day==5:
                    time_to_go ="پنج روز پیش"
                elif to_irani_now.day-value.day==6:
                    time_to_go ="شش روز پیش"
                elif 6<to_irani_now.day-value.day<14:
                    time_to_go =" یک هفته پیش"
                elif 14<=to_irani_now.day-value.day<20:
                    time_to_go =" دو هفته پیش"
                
                elif 20<=to_irani_now.day-value.day<28:
                    time_to_go =" سه هفته پیش"
                
                elif 28<=to_irani_now.day-value.day<=31:
                    time_to_go =" چهار هفته پیش"
            elif to_irani_now.month -value.month ==1:
                time_to_go="یک ماه پیش"
    

        return time_to_go
            


                    

                        



                

                
        
        

