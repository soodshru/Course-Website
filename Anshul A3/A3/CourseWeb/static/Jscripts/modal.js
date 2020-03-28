const modalBttn = document.getElementById("remarkRequest");
const closeBttn = document.getElementById("closebttn");
const modalWindow = document.getElementById("modalWindow");

modalBttn.addEventListener("click", showModal);

closebttn.addEventListener("click", hideModal);

function showModal(){
    
    modalWindow.style.display ="block";
}

function hideModal(){
    
    modalWindow.style.display = "none";
}