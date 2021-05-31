
function clickBtn(i) {

    const p2 = document.getElementById(i);

    if (p2.style.visibility == "visible") {
        // hiddenで非表示
        p2.style.visibility = "hidden";
    } else {
        // visibleで表示
        p2.style.visibility = "visible";
    }
}


// function pronounce() {

//     let word = document.getElementById('word').value;
//     let u = new SpeechSynthesisUtterance();
//     u.lang = 'en-US';
//     u.text = word;
//     speechSynthesis.speak(u);

// }
