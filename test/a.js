const persianDate=require('persian-date');


var a=[
  {
    "name": "شیراز",
    "minis": [
      {
        "name": "مرودشت",
        "id": 1
      },
      {
        "name": "زرقان",
        "id": 2
      }
    ],
    "cityId": 1
  }
]
a.forEach(item=>{
  item["minis"].forEach(el=>{
    console.log("aa")
    console.log(el.id)
  })
})
let $r='mohammad'
console.log($r)

let e={
  1:"mohammad",
  name:"alireza"
}
console.log(e["1"])

let rr=[1,2,3,4,5,6,7,8,9]
console.log(rr.slice(5))
console.log(rr[-5])
rr[0]="aa"
rr[40]="rrrrr"
console.log(rr) 

function test(name,age){
  console.log(name,age)
}
test(name="mohammad",age="44")

// let today = new Date().toTimeString().toLocaleDateString('fa-IR');
// console.log(today);



// let aa=new Date().toLocaleTimeString("fa-IR")
// console.log(aa)

// let b="2023-03-05T19:35:26.218Z";
// let v=new Date(b).toLocaleTimeString("fa-IR")
// console.log(aa)
// console.log(v)





// var date = new Date('22:00:00');
// var date2 = new Date('1400-03-2 20:00:00');
// // let l=date-date2
// // console.log(l/3600)
// console.log(date2.getHours())



// console.log()
// console.log()

let ee=new Date("2023-03-14T19:35:26.218Z")
// console.log(ee.getUTCMonth()+1)
// console.log(new Date().getUTCMonth()+1)
// console.log(ee.getUTCDate())
// console.log(new Date().getUTCDate())

console.log(new Date().getHours())
console.log(ee.getHours())


// function handleTimeJs(commericalTime){
//   let now=new Date()
//   var result=''


//   var hourDiff = now.getTime() - commericalTime.getTime(); //in ms
//   var secDiff = hourDiff / 1000;

//   var toHHH=secDiff/3600
//   console.log(secDiff/60,'dddddddddddddddddddddddd')
//   if(now.getFullYear()-commericalTime.getFullYear() ===0){
//     if((now.getUTCMonth()+1)-(commericalTime.getUTCMonth()+1)===0){
//       if(now.getUTCDate() - commericalTime.getUTCDate() ===0 ){
        
//         if(0<=toHHH && toHHH<1){
//           console.log("func",)

//             if(secDiff/60 >0){
//               if(0<=secDiff<=5){
//                   result='لحظاتی پیش'
//               }else if(5<secDiff<=10){
//                 result="دقایقی پیش"
//               }else if(10<secDiff<=15){
//                 result="یک ربع پیش"
//               }else if(15<secDiff<=59){
//                 result="نیم ساعت پیش"
//               }
//             }


//         }else if(secDiff/3600>=1){
//           console.log('daadadd')
//             if(1<=secDiff/3600<2){
//               result="یک ساعت پیش"
//             }else if(2<=secDiff/3600<3){
//               result="دو ساعت پیش"
//             }else if(3<=secDiff/3600<4){
//               result="سه ساعت پیش"
//             }else if(4<=secDiff/3600<5){
//               result="چهار ساعت پیش"
//             }else if(5<=secDiff/3600<6){
//               result="پنج ساعت پیش"
//             }else if(6<=secDiff/3600<7){
//               result="شش ساعت پیش"
//             }else if(7<=secDiff/3600<8){
//               result="هفت ساعت پیش"
//             }else if(8<=secDiff/3600<9){
//               result="هشت ساعت پیش"
//             }else if(9<=secDiff/3600<10){
//               result="نه ساعت پیش"
//             }else if(10<=secDiff/3600<11){
//               result="ده ساعت پیش"
//             }else if(11<=secDiff/3600<12){
//               result="یازده ساعت پیش"
//             }else if(12<=secDiff/3600<13){
//               result="دوازده ساعت پیش"
//             }else if(13<=secDiff/3600<14){
//               result="سیزده ساعت پیش"
//             }else if(14<=secDiff/3600<15){
//               result="چهارده ساعت پیش"
//             }else if(15<=secDiff/3600<16){
//               result="پانزده ساعت پیش"
//             }else if(16<=secDiff/3600<17){
//               result="شانزده ساعت پیش"
//             }else if(17<=secDiff/3600<18){
//               result="هفده ساعت پیش"
//             }else if(18<=secDiff/3600<19){
//               result="هجده ساعت پیش"
//             }else if(19<=secDiff/3600<20){
//               result="نوزده ساعت پیش"
//             }else if(20<=secDiff/3600<21){
//               result="یست ساعت پیش"
//             }else if(21<=secDiff/3600<22){
//               result="بیست و یک ساعت پیش"
//             }else if(22<=secDiff/3600<23){
//               result="بیست و دو ساعت پیش"
//             }else if(23<=secDiff/3600<24){
//               result="بیست و سه ساعت پیش"
//             }

//         }else if(secDiff/3600<0){
//           console.log("YYOYOYOYO")
//           if(-21<=secDiff/3600<-22){
//             result="سه ساعت پیش"

//           }else if(-22<=secDiff/3600<-23){
//             result="دو ساعت پیش"

//           }else if(-23<=secDiff/3600<-24){
//             result="یک ساعت پیش"

//           }else if(-20<=secDiff/3600<-21){
//             result="چهار ساعت پیش"

//           }else if(-19<=secDiff/3600<-20){
//             result="پنج ساعت پیش"

//           }else if(-18<=secDiff/3600<-19){
//             result="شش ساعت پیش"

//           }else if(-17<=secDiff/3600<-18){
//             result="هفت ساعت پیش"

//           }else if(-16<=secDiff/3600<-17){
//             result="هشت ساعت پیش"

//           }else if(-15<=secDiff/3600<-16){
//             result="نه ساعت پیش"

//           }else if(-14<=secDiff/3600<-15){
//             result="ده ساعت پیش"

//           }else if(-13<=secDiff/3600<-14){
//             result="یازده ساعت پیش"

//           }else if(-12<=secDiff/3600<-13){
//             result="دوازده ساعت پیش"

//           }else if(-11<=secDiff/3600<-12){
//             result="سیزده ساعت پیش"

//           }else if(-10<=secDiff/3600<-11){
//             result="چهارده ساعت پیش"

//           }else if(-9<=secDiff/3600<-10){
//             result="پانزده ساعت پیش"

//           }else if(-8<=secDiff/3600<-9){
//             result="شانزده ساعت پیش"

//           }else if(-7<=secDiff/3600<-8){
//             result="هفده ساعت پیش"

//           }else if(-6<=secDiff/3600<-7){
//             result="هجده ساعت پیش"

//           }else if(-5<=secDiff/3600<-6){
//             result="نوزده ساعت پیش"

//           }else if(-4<=secDiff/3600<-5){
//             result="بیست ساعت پیش"

//           }else if(-3<=secDiff/3600<-4){
//             result="بیست و یک ساعت پیش"

//           }else if(-2<=secDiff/3600<-3){
//             result="بیست و دو ساعت پیش"

//           }else if(-1<=secDiff/3600<-2){
//             result="بیست و سه ساعت پیش"

//           }


//         }


//       }
//     }
//   }
//   return result
// }
// let y=handleTimeJs(ee)
// console.log(y)












































var timeStart = new Date("Mon Jan 01 2007 7:00:00 GMT+0530").getTime();
var timeEnd = new Date("Mon Jan 01 2007 01:00:00 GMT+0530").getTime();
var hourDiff = timeEnd - timeStart; //in ms
var secDiff = hourDiff / 1000; //in s
// var minDiff = hourDiff / 60 / 1000; //in minutes
// var hDiff = hourDiff / 3600 / 1000; //in hours
// var humanReadable = {};
// humanReadable.hours = Math.floor(hDiff);
// humanReadable.minutes = minDiff - 60 * humanReadable.hours;
// // console.log(humanReadable); //{hours: 0, minutes: 30}
console.log(secDiff/3600)

let rrr=["mohammad","a","b","c"]
let title="a"
if(rrr.includes(title)){
  console.log("ye")
}