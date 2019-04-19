function myFunction(c) {
	var x=document.getElementById("mySearch").placeholder;
	var x2=document.getElementById("first").value;
	document.getElementById("demo").innerHTML = typeof x+ typeof x2;
	x2=String(x2);
	document.getElementById("demo").innerHTML = typeof x+ typeof x2;
	if(x.localeCompare(x2)) {
	   document.getElementById("demo").innerHTML = "Done";
    }
}


