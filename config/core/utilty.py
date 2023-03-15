from datetime import datetime
from jalali_date import datetime2jalali
from django.utils import timezone


PUBLISHER_CHOICES=(
    ('شخخصی','شخخصی'),
    ('املاک','املاک')
)

FUEL_CHOICES=(
    ("گاز",'گاز'),
    ("بنزین",'بنزین'),
    ("گاز و بنزین","گاز و بنزین"),
    ("گازاایل","گازاایل")
)

ENGIN_TYPE=(
    ("سالم","سالم"),
    ("متوسط","متوسط")
)

BODY_STATUS=(
    ("رنگ","رنگ"),
    ("بی رنگ","بی رنگ")
)

TRANSMITION_TYPE=(
    ("دنده ای","دنده ای"),
    ("اتومات","اتومات"),
)


PHONE_STATUS=(
    ("نو","نو"),
    ("در حد نو","در حد نو"),
    ("کارکرده","کارکرده"),

)
ORIGINAL_OR_NOT=(
    ("اصل","اصل"),
    ("تقلبی","تقلبی"),
)

COMMERICAL_STATUS=(
    ("ویژه","ویژه"),
    ("فوری","فوری"),
    ("ستاره دار","ستاره دار"),
    ("عادی","عادی"),
)



RENT_STATUS=(
    ("کامل","کامل"),
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("7","7"),
  
)

def findTimeDiffrence(time_1,time_2):
    
    time_1_to_jalili=datetime2jalali(time_1)
    fmt = '%H:%M:%S'
    time_1_to_str=time_1_to_jalili.strftime(fmt)

    s1=""
    for i in time_1_to_str:
        if i == ".":
            break
        else:
            s1+=i
    s1=s1.replace(":","")

    time_2_to_str=time_2.time().strftime(fmt)
    time_2_to_str=time_2_to_str.replace(":","")

    time1=datetime.strptime(s1,"%H%M%S")
    time2=datetime.strptime(time_2_to_str,"%H%M%S")

    return time1-time2







title_not_to_be=["فروش مسکونی","اجاره مسکونی",
                         "آپارتمان","خانه و ویلا",
                        "آپارتمان","خانه و ویلا",
                        "خانه و ویلا فروش","آپارتمان فروش",
                        "خانه و ویلا اجاره","آپارتمان اجاره",
                        "گوشی موبایل ","سواری و وانت","کلاسیک"
                        
                        ]

three_level_parent=[
    "املاک","خانه و آشپزخانه","اجتماعی","اجتماعی"
]


two_level_parent=[
    "استخدام و کاریابی","خدمات",""
]

two_and_three_parent=[
    "وسایل نقلیه","وسایل شخصی","سرگرمی و فراغت","کالای دیجیتال","تجهیزات و صنعتی"
]






filteramlak_groupA=[
    "فروش مسکونی","فروش اداری و تجاری",
]

filteramlak_groupB=[
"اجاره مسکونی","اجاره اداری و تجاری","اجاره کوتاه مدت"
]


