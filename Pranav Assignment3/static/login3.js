 function manage(txt) {
        var bt = document.getElementById('submit');
        if (txt.value != '') {
            bt.disabled = false;
        }
        else {
            bt.disabled = true;
        }
    }    