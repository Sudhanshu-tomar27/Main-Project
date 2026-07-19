/* =====================================
   THREE LINE MENU
===================================== */


function toggleMenu(){


let menu =
document.getElementById(
"menuBox"
);



if(menu.style.display==="block"){


menu.style.display="none";


}

else{


menu.style.display="block";


}


}





/* =====================================
   SAVE DOCUMENT
===================================== */


function saveFile(){


let filename = prompt(
"Enter file name"
);



if(filename==null || filename=="")
{

return;

}



let form=document.createElement(
"form"
);


form.method="POST";

form.action="/save-file";



let input=document.createElement(
"input"
);



input.name="filename";

input.value=filename;



form.appendChild(input);


document.body.appendChild(form);


form.submit();


}





/* =====================================
   TRANSLATION
===================================== */


function translateText(){


let language = prompt(

"Translate into:\n\n1. Hindi\n2. English"

);



if(language=="1"){


window.location.href=

"/translate/hi";


}



else if(language=="2"){


window.location.href=

"/translate/en";


}



}

function saveFile(){


let name = prompt(
"Enter file name"
);



if(name != null && name != ""){


let form =
document.createElement("form");



form.method="POST";

form.action="/save-file";



let input =
document.createElement("input");



input.name="filename";

input.value=name;



form.appendChild(input);



document.body.appendChild(form);


form.submit();


}



}