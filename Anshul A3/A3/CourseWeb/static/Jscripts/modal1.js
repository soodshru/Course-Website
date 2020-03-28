const closeBttn = document.getElementById("closebttn");
const closeBttn1 = document.getElementById("closebttn1");
const closeBttn2 = document.getElementById("closebttn2");
const newentryform = document.getElementById("newentryform");
const viewremarkrequest = document.getElementById("viewremarkrequest");
const changegradeform = document.getElementById("changegradeform");
const newEntrymodalWindow = document.getElementById("NewEntrymodalWindow");
const remarkmodalWindow = document.getElementById("RemarkModalWindow");
const changeGradeModal = document.getElementById("changeGradeModalWindow");
var SectionCollapsible = document.getElementsByClassName("SectionCollapsible");
var i;

newentryform.addEventListener("click", shownewEntryModal);
viewremarkrequest.addEventListener("click", showRemarkModal);
changegradeform.addEventListener('click', showchangeGradeModal);
closeBttn.addEventListener("click", hideModal);
closeBttn1.addEventListener("click", hideModal1);
closeBttn2.addEventListener("click", hideModal2);

function shownewEntryModal(){
    
    NewEntrymodalWindow.style.display ="block";
}

function showRemarkModal(){
    
    remarkmodalWindow.style.display ="block";
}

function showchangeGradeModal(){

	changeGradeModalWindow.style.display = "block";
}

function hideModal(){
    
    NewEntrymodalWindow.style.display = "none";
}

function hideModal1(){

    changeGradeModalWindow.style.display = "none";
}

function hideModal2(){

	remarkmodalWindow.style.display = "none";
}



for (i = 0; i < SectionCollapsible.length; i++) {
	SectionCollapsible[i].addEventListener("click", 
	function() {
  	this.classList.toggle("active");
  	var SectionContent = this.nextElementSibling;
  	if (SectionContent.style.display === "inline-block") {
    	SectionContent.style.display = "none";} 

    else {
    SectionContent.style.display = "inline-block";}
	});
}