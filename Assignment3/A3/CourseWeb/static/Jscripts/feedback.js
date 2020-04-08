document.getElementById("displayQ1").addEventListener("click", function(){DisplayA("displayA1");});
document.getElementById("displayQ2").addEventListener("click", function(){DisplayA("displayA2");});
document.getElementById("displayQ3").addEventListener("click", function(){DisplayA("displayA3");});
document.getElementById("displayQ4").addEventListener("click", function(){DisplayA("displayA4");});

function DisplayA(DisplayAID){
    if (document.getElementById(DisplayAID).style.display === "block"){

        document.getElementById(DisplayAID).style.display = "none"
        }
    else{

        document.getElementById(DisplayAID).style.display="block";
        }

}/* end of display function*/