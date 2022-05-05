/*Redigerad och anpassad kod från w3School*/

function dropFunction_players() {
  down()
  document.getElementById("hockey_players").classList.toggle("show");
}

function dropFunction_matches() {
  down()
  document.getElementById("matches").classList.toggle("show");
}
  
function dropFunction_posts() {
  down()
  document.getElementById("posts").classList.toggle("show");
}

function dropFunction_mobile() {
  down()
  document.getElementById("mobile_content").classList.toggle("show");
}
  
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
    down()
  }
}
    
function down(){
  var myDropdown = document.getElementsByClassName("dropdown_content");
  for (var i = 0; i < myDropdown.length; i++) {
    if (myDropdown[i].classList.contains('show')) {
      myDropdown[i].classList.remove('show');
    }
  }
}
/*Kod från en labb i introduktion till webbutveckling*/
$(document).ready(function() {
  // Kod inne i denna funktionen körs när sidan har laddats klart

  /*
      Döljer alla element (utom "<header>") i alla element av typen
      "<article>" med klassen "foldable"
  */
  $("article.foldable > *:not(header)").hide();

  /*
      När man klickar på ett "<header>"-element i ett "<article>"-
      element med klassen "foldable" så döljs/visas alla element
      som ligger efter "<header>"-elementet som användaren klickade på
  */
  $("article.foldable header").on("click", function() {
      $(this).nextAll("*").slideToggle();
  });
});

/* 
slideshow. 
HTML - en div med klassen one_time. Där i läggs divar som ska finnas i slideshowen.
*/
$(document).ready(function(){
  
  $('.one_time').slick({
    dots: false,
    infinite: true,
    speed: 300,
    slidesToShow: 5,
    slidesToScroll: 1,
    accessibility:true,
    variableWidth:false,
    arrows:true,
    prevArrow:'<button type="button" data-role="none" class="prev_arrow "><</button>',
    nextArrow:'<button type="button" data-role="none" class="next_arrow">></button>',
    
    responsive: [
      {
        breakpoint: 1900,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 1,
          infinite: true,
          dots: false
        }
      },
      {
        breakpoint: 1525,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 1160,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 670,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
    ]
  }); 

  /*Kod för att vända på korten*/
  const card = document.querySelectorAll(".card__inner");

  function flipCard() {
    this.classList.toggle('is-flipped');
  }
  card.forEach((card) => card.addEventListener("click", flipCard));
});