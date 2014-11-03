// JScript 文件
//DIV居中
function vMiddle()
{
    var middleDiv=document.getElementById("wrap");
    var divHeight=middleDiv.offsetHeight;
    var bodyHeight=document.body.offsetHeight ;
    if(bodyHeight>divHeight)
      middleDiv.style.marginTop=-divHeight/2+"px";
    else
    {
       middleDiv.style.marginTop=0;
       middleDiv.style.top=0;
    }
}
//单击单题卡转到相应题目
function GoToProblemX(obj)
{
    var hd = document.getElementById("hfPaperID");
    hd.value = obj.id;
    document.getElementById("GoBtn").click();
}
function showTimeIsBegin(time){
var self=this;
//下面这句为重点，setTimeout这个函数我就不多讲了（百度一下），说下setTimeout的参数
//一般在在网上看到的都会这样写setTimeout("showTimeIsBegin()",1000);
//大家都发现了吧，如果你按照这个逻辑去写的话肯定是错误的，除非你的时间是直接定义在JS函数里的
//所以说，这里你必须定义一个上面的“var self=this;”然后将其重写在传入time参数，如下
window.setTimeout(function(){self.showTimeIsBegin(time);}, 1000);
//下面的这句BirthDay=new Date()原来是这样写的BirthDay=new Date('3-14-2012 14:23:59');
//可以看出它直接把结束时间的参数写在函数里了
//如果是这样的话，就没动态控制的意义了，所以改成如下形式
BirthDay=new Date(time);
today=new Date();
timeold=(BirthDay.getTime()-today.getTime());
sectimeold=timeold/1000
secondsold=Math.floor(sectimeold);
msPerDay=24*60*60*1000
e_daysold=timeold/msPerDay
daysold=Math.floor(e_daysold);
e_hrsold=(e_daysold-daysold)*24;
hrsold=Math.floor(e_hrsold);
e_minsold=(e_hrsold-hrsold)*60;
minsold=Math.floor((e_hrsold-hrsold)*60);
seconds=Math.floor((e_minsold-minsold)*60);
if(daysold<0)
{
span_dt_dt.innerHTML="时间到！";
}else
{
span_dt_dt.innerHTML=daysold+"天"+hrsold+"小时"+minsold+"分"+seconds+"秒" ;

}
}
//记得这里重新调用也要传参数，别忘记了
 //showTimeIsBegin(time);
