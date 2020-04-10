function resetform() {
document.getElementById("myform").reset();
}


function validate() {
	
	var utorid = document.getElementById("utorid");
	var lab = document.getElementById("lab");
	var bt = document.getElementById("mybtn");
	var a1 = document.getElementById("a1");
	var a2 = document.getElementById("a2");
	var a3 = document.getElementById("a3");
	var midterm = document.getElementById("midterm");
	var final = document.getElementById("final");


	if(utorid.value =="" || lab.value =="" || a1.value =="" || a2.value=="" || a3.value=="" || midterm.value=="" || final.value=="")
	{
		alert("Incomplete Form");
		if(utorid.value=="")
		{
			utorid.style.backgroundColor = "orange";
		}
		if(lab.value=="")
		{
			lab.style.backgroundColor = "orange";
		}
		if(a1.value=="")
		{
			a1.style.backgroundColor = "orange";
		}
		if(a2.value=="")
		{
			a2.style.backgroundColor = "orange";
		}
		if(a3.value=="")
		{
			a3.style.backgroundColor = "orange";
		}
		if(midterm.value=="")
		{
			midterm.style.backgroundColor = "orange";
		}
		if(final.value=="")
		{
			final.style.backgroundColor = "orange";
		}
	}
	else
	{
		bt.disabled = false;
		utorid.style.backgroundColor = "lightgreen";
		lab.style.backgroundColor = "lightgreen";
		a1.style.backgroundColor = "lightgreen";
		a2.style.backgroundColor = "lightgreen";
		a3.style.backgroundColor = "lightgreen";
		midterm.style.backgroundColor = "lightgreen";
		final.style.backgroundColor = "lightgreen";
	}

}