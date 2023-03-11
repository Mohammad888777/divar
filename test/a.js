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