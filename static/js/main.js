 function validateemail()  
{  
var x=document.myform.email.value;  
var atposition=x.indexOf("@");  
var dotposition=x.lastIndexOf(".");  
if (atposition<1 || dotposition<atposition+2 || dotposition+2>=x.length){  
  alert("Please enter a valid e-mail address \n atpostion:"+atposition+"\n dotposition:"+dotposition);  
  return false;  
  }  

var num=document.myform.mob.value;  
if (isNaN(num)){
    alert("please enter numericals only in mobile number");  
    document.getElementById("mob").innerHTML="Enter Numeric value only";  
    return false;  
  }else{  
    return true;  
    }  
  }

