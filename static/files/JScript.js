// JScript 文件
function InitAjax()
{
    var ajax = false; 
    try
    {
    ajax = new ActiveXObject("Msxml2.XMLHTTP");
    }
    catch (e)
    { 
        try 
        { 
          ajax = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (E)
        { 
          ajax = false; 
        } 
    }
    if (!ajax && typeof XMLHttpRequest!='undefined')
    {
     ajax = new XMLHttpRequest();
    } 
    return ajax;
}
function datexml(url,value){
  var number = Math.random();
　var url = url +"?qaaq=" + number +  value;
　var ajax = InitAjax();
　ajax.open("GET", url, false); 
　ajax.send(null); 
//ajax.onreadystatechange = function() { }
　if(ajax.readyState == 4 && ajax.status == 200)
　{
　  return ajax.responseText;
　} 
} 
function keydown(e)
{
    var keyvalue = event.keyCode;
    if(keyvalue == 97)
    {
       if(document.getElementById('answer1') != null)
       {
            document.getElementById('answer1').click();
       }
    }
    else if(keyvalue == 98)
    {
       if(document.getElementById('answer2') != null)
       {
            document.getElementById('answer2').click();
       }
    }
    else if(keyvalue == 99)
    {
       if(document.getElementById('answer3') != null)
       {
            document.getElementById('answer3').click();
       }
    }
    else if(keyvalue == 101)
    {
       if(document.getElementById('answer4') != null)
       {
            document.getElementById('answer4').click();
       }
    }
    else if(keyvalue == 100)
    {
       if(document.getElementById('UpPage') != null)
       {
            document.getElementById('UpPage').click();
       }
    }
    else if(keyvalue == 102)
    {
        if(document.getElementById('DownPage') != null)
       {
            document.getElementById('DownPage').click();
       }
    }
    else if(keyvalue == 13)
    {
        if(document.getElementById('Sanswer') != null)
       {
            document.getElementById('Sanswer').click();
       }
    }
    else if(keyvalue == 106)
    {
       if(document.getElementById('EndKSButton') != null)
       {
            document.getElementById('EndKSButton').click();
       }
    }
    else
    {
        return false;
    }
}
 
 function   document.onkeydown()   
{   
var   e=event.srcElement;   
if(event.keyCode== 97 )   
{   
if(document.getElementById('answerA') != null)
       {
document.getElementById("answerA").click();   
}

}   
else if(event.keyCode== 98 )   
{   
if(document.getElementById('answerB') != null)
       {
document.getElementById("answerB").click();   
}
}   
if(event.keyCode== 99 )   
{   
if(document.getElementById('answerC') != null)
       {
document.getElementById("answerC").click();   
}
}   
if(event.keyCode== 100 )   
{   
if(document.getElementById('Pro') != null)
       {
document.getElementById("Pro").click();   
}   
}  
if(event.keyCode== 101 )   
{   
if(document.getElementById('answerD') != null)
       {
document.getElementById("answerD").click();   
}  
}    
if(event.keyCode== 102 )   
{   
if(document.getElementById('Next') != null)
       {
document.getElementById("Next").click();   
}   
}   
if(event.keyCode== 104 )   
{   
if(document.getElementById('answerE') != null)
       {
document.getElementById("answerE").click();   
}  
}   
if(event.keyCode== 106 )   
{   
if(document.getElementById('End') != null)
       {
document.getElementById("End").click();   
} 
}   
if(event.keyCode== 111 )   
{   
if(document.getElementById('answerF') != null)
       {
document.getElementById("answerF").click();   
}  
}  
if(event.keyCode== 13 )   
{   
if(document.getElementById('Next') != null)
       {
document.getElementById("Next").click();   
}  
}  
} 