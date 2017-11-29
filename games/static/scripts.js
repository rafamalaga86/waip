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

  $('.grid').imagesLoaded(function() {
    $grid.masonry();
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

  function mcScoreToColour(score) {
    red = '#f00';
    yellow = '#fc3';
    green = '#6c3';
    score = parseInt(score);

    if (score && score >= 75) {
      return green;
    } else if (score && score >= 50) {
      return yellow;
    }

    return red;
  }

  function paintScore(div) {
      score = div.find('span').text().trim();
      div.css('background-color', mcScoreToColour(score));
  }

  $('.score-metacriticScore').each(function() {
    paintScore($(this));
  });



  // General AJAX requests
  // =======================================================

  // $("#form-login").ajaxForm({url: '/users/login/', type: 'POST'})



// =========================================================
// ================== SPECIFIC VIEWS =======================
// =========================================================


  // Game Grid
  // =======================================================

  //-- Set a game as finished
  $('.card').on('click', '.btn-finished', function(){
    var btn = $(this);
    var id = btn.parents('.card').attr('data-game-id');
    jQuery.ajax({
      method: 'PATCH',
      url: '/ajax/games/' + id + '/finish'
    })
    .done(function(){
      console.log('card-' + id);

      $grid.masonry('remove', $('.card-' + id)).masonry();
    });
  });

// -- IMPLEMENTAR EL MASONRY.REMOVE ARRIBA EN VEZ DEL FADEOUT
  // $('.card').on('click', '.btn-delete', function(){
  //   var btn = $(this);
  //   var id = btn.parents('.card').attr('data-contact-id');
  //   jQuery.ajax({
  //     method: 'DELETE',
  //     url: '/contacts/' + id
  //   })
  //   .done(function(){
  //     $grid.masonry('remove', $('.card-' + id)).masonry('layout');
  //   });
  // });




  // Add a note to a game
  // - Open modal
  $('.card').on('click', '.btn-add-note', function(){
    var btn = $(this);
    var id = btn.parents('.card').attr('data-game-id');
    var name = btn.parents('.card-content').children('.card-gameTitle').text();
    $('#modal-note textarea').val('');
    $('#modal-note').attr('data-game-id', id);
    $('#modal-note').modal('toggle');
    $('#modal-note h5.modal-title span').text(name);
  });

  // - Send note data
  $('#modal-note').on('click', '.btn-save-note', function(){
    var id = $('#modal-note').attr('data-game-id');
    var noteText = $('#modal-note textarea').val();
    jQuery.ajax({
      method: 'POST',
      data: {'text': noteText},
      url: '/ajax/games/' + id + '/add-note'
    })
    .done(function(){
      $('#modal-note').modal('toggle');
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