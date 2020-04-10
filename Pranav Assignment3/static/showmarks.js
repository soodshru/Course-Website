		function resetform() {
document.getElementById("myform").reset();
}

function validate() {
	
	var utorid = document.getElementById("utor");
	var txtarea = document.getElementById("txtarea");
	var bt = document.getElementById("mybtn");

	if(utorid.value =="" || txtarea.value=="")
	{
		utorid.style.backgroundColor = "orange";
		txtarea.style.backgroundColor = "orange";
		alert(" Utorid / Reason Not Provided. Please Provide Reason to Continue.");
	}
	else
	{
		bt.disabled = false;
		utorid.style.backgroundColor = "grey";
		txtarea.style.backgroundColor = "grey";
	}

}