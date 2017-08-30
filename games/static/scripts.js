$(document).ready(function(){

  // Grid and Masonry
  // =========================================
  var $grid = $('.grid').masonry({
    itemSelector: '.card',
    fitWidth: true,
    gutter: 20
    // columnWidth: 50
  });


  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
      }
  });

  $(".card").each(function(index, el) {
    var id = $(this).data("game-id");
    $(this).load("/games/" + id, null, function(){
      $grid.masonry();
    });
  });

  // $.ajax({
  //   method: "POST",
  //   url: "games/1",
  //   data: { name: "John", location: "Boston" }
  // })
  // .done(function(msg) {
  //   alert( "Data Saved: " + msg );
  // });
});