from datetime import datetime
from jalali_date import datetime2jalali
from django.utils import timezone


PUBLISHER_CHOICES=(
    ('همه','همه'),
    ('شخخصی','شخخصی'),
    ('املاک','املاک')
)

PUBLISHERForCar_CHOICES=(
    ('همه','همه'),
    ('درخواست','درخواست'),
    ('فروشی','فروشی')
)

FUEL_CHOICES=(
    ("گاز",'گاز'),
    ("بنزین",'بنزین'),
    ("گاز و بنزین","گاز و بنزین"),
    ("گازاایل","گازاایل")
)

ENGIN_TYPE=(
    ("سالم","سالم"),
    ("نیاز به تعمیر","نیاز به تعمیر"),
    ("تعویض شده","تعویض شده")
)

BODY_STATUS=(
    ("سالم و بی‌خط و خش","سالم و بی‌خط و خش"),
    ("رنگ","رنگ"),
    ("بی رنگ","بی رنگ"),
    ("خط و خش جزیی","خط و خش جزیی"),
    ("صافکاری بی‌رنگ","صافکاری بی‌رنگ"),
    ("رنگ‌شدگی","رنگ‌شدگی"),
    ("دوررنگ","دوررنگ"),
    ("تمام‌رنگ","تمام‌رنگ"),
    ("تصادفی","تصادفی"),
    ("اوراقی","اوراقی")

)

SHASTITYPE=(
    ("هر دو سالم و پلمپ","هر دو سالم و پلمپ"),
    ("عقب ضربه‌خورده","عقب ضربه‌خورده"),
    ("عقب رنگ‌شده","عقب رنگ‌شده"),
    ("جلو ضربه‌خورده","جلو ضربه‌خورده"),
    ("جلو رنگ‌شده","جلو رنگ‌شده"),
    ("عقب ضربه‌خورده، جلو رنگ‌شده","عقب ضربه‌خورده، جلو رنگ‌شده"),
    ("عقب رنگ‌شده، جلو ضربه‌خورده","عقب رنگ‌شده، جلو ضربه‌خورده"),
    ("هردو ضربه‌خورده","هردو ضربه‌خورده"),
    ("هردو رنگ‌شده","هردو رنگ‌شده")
)

TRANSMITION_TYPE=(
    ("دنده ای","دنده ای"),
    ("اتومات","اتومات"),
)


PHONE_STATUS=(
    ('همه','همه'),
    ("نو","نو"),
    ("در حد نو","در حد نو"),
    ("کارکرده","کارکرده"),

)
ORIGINAL_OR_NOT=(
    ('همه','همه'),
    ("اصل","اصل"),
    ("تقلبی","تقلبی"),
)

COMMERICAL_STATUS=(
    ("ویژه","ویژه"),
    ("فوری","فوری"),
    ("ستاره دار","ستاره دار"),
    ("عادی","عادی"),
)

COVERSIMCART=(
    ("دارد","دارد"),
    ("ندارد","ندارد")
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



COLORS=(
    ("همه","همه"),
    ("سفید","سفید"),
    ("مشکی","مشکی"),
    ("زرد","زرد"),
    ("آبی","آبی"),
    ("سبز","سبز"),
    ("قرمز","قرمز"),
)


INTERNALOREXTERNAL=(
    ("همه","همه"),
    ("داخلی","داخلی"),
    ("خارجی","خارجی"),
)

MEMORYSIZE=(
    (4,4),
    (8,8),
    (16,16),
    (32,32),
    (64,64),
    (128,128),
    (256,256),
)

SIMCARTTYPE=(
    ("ایرانسل","ایرانسل"),
    ("همراه اول","همراه اول"),
    ("رایتل","رایتل"),
)


CLOSTHTYPE=(
    ("همه","همه"),
    ("مردانه","مردانه"),
    ("زنانه","زنانه"),
    ("بچگانه","بچگانه"),
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







title_not_to_be=[
                    "املاک","فروش مسکونی","آپارتمان فروش","خانه و ویلا فروش"       ,
                    "اجاره مسکونی","آپارتمان اجاره","خانه و ویلا اجاره","فروش اداری و تجاری",
                    "دفتر کار، اتاق اداری و مطب","مغازه و غرفه","صنعتی،‌ کشاورزی و تجاری",
                    "اجاره اداری و تجاری","اجاره کوتاه مدت","آپارتمان و سوئیت","ویلا و باغ","دفتر کار و فضای آموزشی",
                    "پروژه‌های ساخت و ساز","وسایل نقلیه","خودرو","سواری و وانت","کلاسیک","اجاره‌ای",
                    "سنگین","موتور سیکلت","قطعات یدکی و لوازم جانبی","قایق و سایر وسایل نقلیه",
                    "کالای دیجیتال","خانه و آشپزخانه","لوازم خانگی برقی","ظروف و لوازم آشپزخانه","خوردنی و آشامیدنی",
                    "خیاطی و بافتنی","مبلمان و صنایع چوب","نور و روشنایی","لوازم دکوری و تزئینی","تشک، روتختی و رختخواب",
                    "تهویه، سرمایش و گرمایش","شست‌وشو و نظافت","حمام و سرویس بهداشتی",
                    "خدمات","موتور و ماشین","فرش، گلیم و موکت","پذیرایی/مراسم",
                    "خدمات رایانه‌ای و موبایل","مالی/حسابداری/بیمه","حمل و نقل",
                    "پیشه و مهارت","آرایشگری و زیبایی","سرگرمی","نظافت","باغبانی و درختکاری",
                    "آموزشی","وسایل شخصی","کیف، کفش و لباس","زیورآلات و اکسسوری",
                    "آرایشی، بهداشتی و درمانی","کفش و لباس بچه","وسایل بچه و اسباب بازی","لوازم التحریر",
                    "سرگرمی و فراغت","بلیط","تور و چارتر","کتاب و مجله","حیوانات",
                    "کلکسیون و سرگرمی","آلات موسیقی","ورزش و تناسب اندام","اسباب‌ بازی","اجتماعی",
                    "رویداد","داوطلبانه","گم‌شده‌ها","تجهیزات و صنعتی","مصالح و تجهیزات ساختمان",
                    "ابزارآلات","ماشین‌آلات صنعتی","تجهیزات کسب‌وکار","عمده فروشی","اداری و مدیریت",
                    "استخدام و کاریابی","سرایداری و نظافت","معماری ،عمران و ساختمانی","خدمات فروشگاه و رستوران","رایانه و فناوری اطلاعات",
                    "مالی و حسابداری و حقوقی","بازاریابی و فروش","صنعتی و فنی و مهندسی","آموزشی",
                    "حمل و نقل","درمانی و زیبایی و بهداشتی","هنری و رسانه"


                    
]

three_level_parent=[
    "املاک","خانه و آشپزخانه","اجتماعی","اجتماعی"
]


two_level_parent=[
    "استخدام و کاریابی","خدمات",
]

two_and_three_parent=[
    "وسایل نقلیه","وسایل شخصی","سرگرمی و فراغت","کالای دیجیتال","تجهیزات و صنعتی"
]







immadate_location_image=[
    "املاک","وسایل نقلیه","کالای دیجیتال",
    "خانه و آشپزخانه","خدمات","وسایل شخصی","سرگرمی و فراغت",
    "اجتماعی","تجهیزات و صنعتی","استخدام و کاریابی"
]

price_Title=[
    "وسایل نقلیه","کالای دیجیتال", "خانه و آشپزخانه",
    "سرگرمی و فراغت","اجتماعی","تجهیزات و صنعتی","وسایل شخصی"
]


moavezeh=[
    "تجهیزات و صنعتی", "سرگرمی و فراغت",
    "خانه و آشپزخانه",
    "وسایل شخصی","وسایل نقلیه"
]







GroupHasPrice=[

    "فروش مسکونی","فروش اداری و تجاری","خودرو","موتور سیکلت",
    "قطعات یدکی و لوازم جانبی","قایق و سایر وسایل نقلیه",
    "موبایل و تبلت","رایانه","کنسول","صوتی و تصویری","تلفن رومیزی",
    "لوازم خانگی برقی","ظروف و لوازم آشپزخانه","خوردنی و آشامیدنی",
    "خیاطی و بافتنی","مبلمان و صنایع چوب","نور و روشنایی","فرش، گلیم و موکت",
    "تشک، روتختی و رختخواب","لوازم دکوری و تزئینی","تهویه، سرمایش و گرمایش",
    "شست‌وشو و نظافت","حمام و سرویس بهداشتی","کیف، کفش و لباس","زیورآلات و اکسسوری","آرایشی، بهداشتی و درمانی",
    "کفش و لباس بچه","وسایل بچه و اسباب بازی","لوازم التحریر","بلیط",
    "تور و چارتر","کتاب و مجله","دوچرخه/اسکیت/اسکوتر","حیوانات","کلکسیون و سرگرمی",'آلات موسیقی',
    'ورزش و تناسب اندام','اسباب‌ بازی','رویداد','داوطلبانه','گم‌شده‌ها','مصالح و تجهیزات ساختمان',
    'ابزارآلات','ماشین‌آلات صنعتی','تجهیزات کسب‌وکار','عمده فروشی'




]

GroupHasMeter=[
    "فروش مسکونی",'اجاره مسکونی','فروش اداری و تجاری',
    "اجاره اداری و تجاری",'اجاره کوتاه مدت','پروژه‌های ساخت و ساز'
]


GroupHasYearOfConstruction=[
    "خودرو","موتور سیکلت"
]



GroupHasExchangePossibale=[

    "خودرو","موتور سیکلت","قطعات یدکی و لوازم جانبی","قایق و سایر وسایل نقلیه",
    "موبایل و تبلت","رایانه","کنسول","صوتی و تصویری","تلفن رومیزی",
    "لوازم خانگی برقی","ظروف و لوازم آشپزخانه","خوردنی و آشامیدنی",
    "خیاطی و بافتنی","مبلمان و صنایع چوب","نور و روشنایی","فرش، گلیم و موکت",
    "تشک، روتختی و رختخواب","لوازم دکوری و تزئینی","تهویه، سرمایش و گرمایش",
    "شست‌وشو و نظافت","حمام و سرویس بهداشتی","کیف، کفش و لباس","زیورآلات و اکسسوری",
    "آرایشی، بهداشتی و درمانی","کفش و لباس بچه","وسایل بچه و اسباب بازی","لوازم التحریر","بلیط",
    "تور و چارتر","کتاب و مجله","دوچرخه/اسکیت/اسکوتر","حیوانات","کلکسیون و سرگرمی",'آلات موسیقی',
    'ورزش و تناسب اندام','اسباب‌ بازی','رویداد','داوطلبانه','گم‌شده‌ها',
    'مصالح و تجهیزات ساختمان','ابزارآلات','ماشین‌آلات صنعتی','تجهیزات کسب‌وکار','عمده فروشی'


]


GroupHasCommericalSituation_like_new_or_old=["موبایل و تبلت","رایانه","کنسول","صوتی و تصویری","تلفن رومیزی",
        "لوازم خانگی برقی","ظروف و لوازم آشپزخانه","خوردنی و آشامیدنی",
        "خیاطی و بافتنی","مبلمان و صنایع چوب","نور و روشنایی","فرش، گلیم و موکت",
        "تشک، روتختی و رختخواب","لوازم دکوری و تزئینی","تهویه، سرمایش و گرمایش",
        "شست‌وشو و نظافت","حمام و سرویس بهداشتی",
        "کیف، کفش و لباس","زیورآلات و اکسسوری",
        "آرایشی، بهداشتی و درمانی","کفش و لباس بچه","وسایل بچه و اسباب بازی",
        "لوازم التحریر","بلیط",
        "تور و چارتر","کتاب و مجله","دوچرخه/اسکیت/اسکوتر","حیوانات",
        "کلکسیون و سرگرمی",'آلات موسیقی',
        'ورزش و تناسب اندام','اسباب‌ بازی',
        'مصالح و تجهیزات ساختمان','ابزارآلات','ماشین‌آلات صنعتی',
        'تجهیزات کسب‌وکار','عمده فروشی'
]

Group_Employments=[
    "اداری و مدیریت",'سرایداری و نظافت',
    'معماری ،عمران و ساختمانی','خدمات فروشگاه و رستوران',
    'رایانه و فناوری اطلاعات','مالی و حسابداری و حقوقی','بازاریابی و فروش',
    'صنعتی و فنی و مهندسی','حمل و نقل','درمانی و زیبایی و بهداشتی','آموزشی','هنری و رسانه'

]
















typeOneForSecondLevelFilter_Amlak_Frosh=[
    "فروش مسکونی","فروش اداری و تجاری"
]


amlakEjareh=['اجاره مسکونی', "اجاره اداری و تجاری"]








vasayelNaghliehMotor_va_Car=["موتور سیکلت","خودرو"]
vasayelNaghlieh_Both_and_supplies=["قطعات یدکی و لوازم جانبی","قایق و سایر وسایل نقلیه"]
digitalOrKitchenOrPersonalOrEntertaimentOrSupllies=["موبایل و تبلت","رایانه","کنسول","صوتی و تصویری","تلفن رومیزی",
            "لوازم خانگی برقی","ظروف و لوازم آشپزخانه","خوردنی و آشامیدنی",
            "خیاطی و بافتنی","مبلمان و صنایع چوب","نور و روشنایی","فرش، گلیم و موکت",
            "تشک، روتختی و رختخواب","لوازم دکوری و تزئینی","تهویه، سرمایش و گرمایش",
            "شست‌وشو و نظافت","حمام و سرویس بهداشتی",
            "کیف، کفش و لباس","زیورآلات و اکسسوری",
            "آرایشی، بهداشتی و درمانی","کفش و لباس بچه","وسایل بچه و اسباب بازی",
            "لوازم التحریر","بلیط",
            "تور و چارتر","کتاب و مجله","دوچرخه/اسکیت/اسکوتر","حیوانات",
            "کلکسیون و سرگرمی",'آلات موسیقی',
            'ورزش و تناسب اندام','اسباب‌ بازی',
            'مصالح و تجهیزات ساختمان','ابزارآلات','ماشین‌آلات صنعتی',
            'تجهیزات کسب‌وکار','عمده فروشی'
]

services=[
    'موتور و ماشین','پذیرایی/مراسم','خدمات رایانه‌ای و موبایل',
    'مالی/حسابداری/بیمه','حمل و نقل','پیشه و مهارت','آرایشگری و زیبایی',
    'سرگرمی','نظافت','باغبانی و درختکاری','آموزشی',
]

social=[
    'رویداد','داوطلبانه','داوطلبانه'
]

employment=[
    'اداری و مدیریت','سرایداری و نظافت','معماری ،عمران و ساختمانی','خدمات فروشگاه و رستوران',
    'رایانه و فناوری اطلاعات','مالی و حسابداری و حقوقی','بازاریابی و فروش','صنعتی و فنی و مهندسی',
    'آموزشی','حمل و نقل','درمانی و زیبایی و بهداشتی','هنری و رسانه'
]


digitals=["موبایل و تبلت","رایانه","کنسول","صوتی و تصویری","تلفن رومیزی"]

kitchen=["لوازم خانگی برقی","ظروف و لوازم آشپزخانه","خوردنی و آشامیدنی",
            "خیاطی و بافتنی","مبلمان و صنایع چوب","نور و روشنایی","فرش، گلیم و موکت",
            "تشک، روتختی و رختخواب","لوازم دکوری و تزئینی","تهویه، سرمایش و گرمایش",
            "شست‌وشو و نظافت","حمام و سرویس بهداشتی"]

personal=[ "کیف، کفش و لباس","زیورآلات و اکسسوری",
            "آرایشی، بهداشتی و درمانی","کفش و لباس بچه","وسایل بچه و اسباب بازی",
            "لوازم التحریر",]



# third levels filter 


apartemanForosh=["آپارتمان فروش","خانه و ویلا فروش","زمین و کلنگی فروش",
"دفتر کار، اتاق اداری و مطب","مغازه و غرفه","صنعتی،‌ کشاورزی و تجاری"
]


foroshJustForSanadEdari=["دفتر کار، اتاق اداری و مطب",
"مغازه و غرفه","صنعتی،‌ کشاورزی و تجاری"]


ejarehAll=["آپارتمان اجاره","خانه و ویلا اجاره",
"دفتر کار، اتاق اداری و مطب","مغازه و غرفه","صنعتی،‌ کشاورزی و تجاری"
]


cars=[
    "سواری و وانت","کلاسیک","اجاره‌ای","سنگین"
]

tablet_and_mobile=["تبلت","گوشی موبایل"]



themSelf=[
"رایانه همراه","رایانه رومیزی","قطعات و لوازم جانبی","مودم و تجهیزات شبکه",
"پرینتر/اسکنر/کپی/فکس","فیلم و موسیقی","وربین عکاسی و فیلم‌برداری",
"پخش‌کننده همراه","سیستم صوتی خانگی","ویدئو و پخش کننده","تلویزیون و پروژکتور","دوربین مداربسته","یخچال و فریزر",
"آب‌سردکن و تصفیه آب","ماشین لباسشویی و خشک‌کن لباس","ماشین ظرفشویی","جاروبرقی، جاروشارژی و بخارشو","اتو و لوازم اتو","بمیوه و آب‌مرکبات‌گیر",
"خردکن، آسیاب و غذاساز","سماور، چای‌ساز و قهوه‌ساز","اجاق گاز و لوازم برقی پخت‌وپز","هود","سایر لوازم برقی",
"سفره، حوله و دستمال آشپزخانه","آب‌چکان و نظم‌دهنده ظروف","قوری، کتری و قهوه‌ساز دستی","ظروف سرو و پذیرایی",
"ظروف پخت‌وپز","چرخ خیاطی و ریسندگی","لوازم خیاطی و بافتنی","مبلمان خانگی و میزعسلی","میز و صندلی غذاخوری",
"بوفه، ویترین و کنسول","کتابخانه، شلف و قفسه‌های دیواری","جاکفشی، کمد و دراور","تخت و سرویس خواب","میز تلفن","میز تلویزیون",
"میز تحریر و کامپیوتر","مبلمان اداری","صندلی و نیمکت","لوستر و چراغ آویز","چراغ خواب و آباژور",
"ریسه و چراغ تزئینی","لامپ و چراغ","فرش","تابلو فرش","روفرشی","پادری","موکت","گلیم، جاجیم و گبه","پشتی",
"رختخواب، بالش و پتو","تشک تختخواب","سرویس روتختی","پرده، رانر و رومیزی","آینه","ساعت دیواری و تزئینی",
"تابلو، نقاشی و عکس","مجسمه، تندیس و ماکت","گل مصنوعی","گل و گیاه طبیعی","صنایع دستی و سایر لوازم تزئینی","آبگرمکن، پکیج و شوفاژ",
"بخاری، هیتر و شومینه","کولر آبی","کولر گازی و فن‌کوئل","پنکه و تصفیه‌کنندهٔ هوا","مواد شوینده و دستمال کاغذی",
"لوازم نظافت","بندرخت و رخت‌آویز","لوازم حمام","لوازم سرویس بهداشتی",
"اسباب بازی",
"کالسکه و لوازم جانبی","صندلی بچه","اسباب و اثاث بچه","کنسرت",
"تئاتر و سینما","کارت هدیه و تخفیف","اماکن و مسابقات ورزشی","ورزشی","اتوبوس، مترو و قطار",
"آموزشی","ادبی","تاریخی","مذهبی","مجلات","گربه","موش و خرگوش","خزنده","پرنده","ماهی","لوازم جانبی","حیوانات مزرعه",
"سگ","سکه، تمبر و اسکناس","اشیای عتیقه","گیتار، بیس و امپلیفایر","سازهای بادی","پیانو/کیبورد/آکاردئون",
"سنتی","درام و پرکاشن","ویولن","ورزش‌های توپی","کوهنوردی و کمپینگ","غواصی و ورزش‌های آبی","ماهیگیری",
"تجهیزات ورزشی","ورزش‌های زمستانی","اسب و تجهیزات اسب سواری","حراج","گردهمایی و همایش","ورزشی",
"تحقیقاتی","حیوانات","اشیا","پزشکی","فروشگاه و مغازه","کافی‌شاپ و رستوران","آرایشگاه و سالن های زیبایی",
"دفتر کار","",

]

male_or_female=["کیف/کفش/کمربند","لباس","ساعت","جواهرات","بدلیجات"]