var elems = document.getElementsByClassName('skill-img');
var divs = document.getElementsByClassName('skill-bl');
for(let z=0;z<divs.length;z++){divs[z].style.display = "none";};
for(let i=0;i<elems.length;i++){
    elems[i].onmouseover = function (c) {
        for(let z=0;z<divs.length;z++){
            divs[z].style.display = "none";
        };
        divs[i].style.display = "block";
    };
};
function act(elem) {
    // get all 'a' elements
    var a = document.getElementsByClassName('act');
    // loop through all 'a' elements
    for (i = 0; i < a.length; i++) {
        // Remove the class 'active' if it exists
        a[i].classList.remove('actives')
    };
    // add 'active' classs to the element that was clicked
    elem.classList.add('actives');
};
window.onscroll = function() {
    var scrolled = window.pageYOffset || document.documentElement.scrollTop; // Получаем положение скролла
        if (scrolled >= 80) {
          document.querySelector('.sec-2').classList.remove('hidden');
          document.querySelector('.sec-2').classList.add('animated', 'fadeInUp');
        }

};
$(document).ready(function() {
    $("#act-b-1").click(function() { // задаем функцию при нажатиии на элемент <div>
        $("#act-b-1b").toggle();
        $("#act-b-2b").hide();
        $("#act-b-3b").hide(); // отображаем, или скрываем элемент
    });
});
$(document).ready(function() {
    $("#act-b-2").click(function() { // задаем функцию при нажатиии на элемент <div>
        $("#act-b-2b").toggle();
        $("#act-b-1b").hide();
        $("#act-b-3b").hide(); // отображаем, или скрываем элемент
    });
});
$(document).ready(function() {
    $("#act-b-3").click(function() { // задаем функцию при нажатиии на элемент <div>
        $("#act-b-3b").toggle();
        $("#act-b-1b").hide();
        $("#act-b-2b").hide(); // отображаем, или скрываем элемент
    });
});
