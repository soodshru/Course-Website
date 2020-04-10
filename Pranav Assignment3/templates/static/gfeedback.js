function resetform() {
document.getElementById("myform").reset();
document.getElementById("t1").style.backgroundColor = "white";
document.getElementById("t2").style.backgroundColor = "white";
document.getElementById("t3").style.backgroundColor = "white";
document.getElementById("t4").style.backgroundColor = "white";
document.getElementById("t5").style.backgroundColor = "white";
}

function handleOnfocus(inst){
	inst.style.color = "blue"
	inst.style.backgroundColor = "lightgrey";
}

function handleOnfocus1(inst){
	inst.style.color = "Indigo"
	inst.style.backgroundColor = "lightgrey";
	inst.style.font = "bold 14px Times, sans-serif";
}

function newImage(){
	document.getElementById("img1").src = "static/Anna_Bretscher.jpg";
}

function oldImage(){
	document.getElementById("img1").src = "static/abbas.png";
}


