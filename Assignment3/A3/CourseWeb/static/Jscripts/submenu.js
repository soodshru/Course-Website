document.getElementById("opensidebttn").addEventListener("click", open);
function open() {
    document.getElementById("sideNav").style.visibility = "visible";
    document.getElementById("opensidebttn").style.id = "closesidebttn";
    document.getElementById("main").style.marginLeft = "20vw";
    

}

document.getElementById("closesidebttn").addEventListener("click", close);
function close() {
  document.getElementById("sideNav").style.visibility = "hidden";
document.getElementById("closesidebttn").style.id = "opensidebttn";
    document.getElementById("main").style.marginLeft = "0vw";
}