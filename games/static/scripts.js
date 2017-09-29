$(document).ready(function(){


  // Template 'engine' to populate json responses with html
  // Given a string, populates substrings found in it that 
  // follows pattern /(\$\d+)/, any '$' followed of integer
  // =======================================================
  String.prototype.template = String.prototype.template ||
    function (){
      var  args = Array.prototype.slice.call(arguments);
      var str = this;
      var i=0;
          
      function replacer(a){
          var aa = parseInt(a.substr(1),10)-1;
          return args[aa];
      }
      return  str.replace(/(\$\d+)/gm,replacer);
  };


  // Initialise the Mansonry Grid
  // =======================================================
  var $grid = $('.grid').masonry({
    itemSelector: '.card',
    fitWidth: true,
    gutter: 20
    // columnWidth: 50
  });


  // Setting CSRF token in every AJAX request
  // =======================================================
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
              xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
          }
      }
  });



  // General AJAX requests
  // =======================================================

  // $("#form-login").ajaxForm({url: '/users/login/', type: 'POST'})



// =========================================================
// ================== SPECIFIC VIEWS =======================
// =========================================================


  // Home View
  // =======================================================

  // Fetch games from server
  $('.card').each(function(index, element) {
    var id = $(this).data('game-id');
    $(this).load('/ajax/games/' + id, null, function(){
      setTimeout(function(){
        $grid.masonry();
      }, 500);
    });
  });

  // Set a game as finished
  $('.card').on('click', '.btn-finished', function(){
    var now = new Date();
    var btn = $(this);
    var id = btn.data('game-id');
    jQuery.ajax({
      method: 'PATCH',
      url: '/ajax/games/' + id + '/finish/',
      data: {
        'finishedAt': now.toISOString().slice(0,10)
      }
    })
    .done(function(){
      btn.parent().fadeOut('400', function(){
        $grid.masonry();
      });
    });
  });


  // New Game View
  // =======================================================

  $('#form-scrap').on('submit', function(){
    // Get metacritic information
    jQuery.get(
      '/ajax/games/scrap-metacritic',
      {metacritic_url: $('#id_metacriticUrl').val()},
      function(jsonResponse){
        for (var key in jsonResponse) {
          if (jsonResponse.hasOwnProperty(key)) {
            $('#' + 'id_' + key).val(jsonResponse[key]);
          }
        }
    }, 'json');

    // Get HLTB information
    jQuery.get(
      '/ajax/games/scrap-hltb',
      {hltb_url: $('#id_hltbUrl').val()},
      function(jsonResponse){
        for (var key in jsonResponse) {
          if (jsonResponse.hasOwnProperty(key)) {
            $('#' + 'id_' + key).val(jsonResponse[key]);
          }
        }
    }, 'json');
  });


});