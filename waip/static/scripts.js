$(document).ready(function(){

  // Initialise the Mansonry Grid
  // =======================================================
  var $grid = $('.grid').masonry({
    itemSelector: '.card',
    fitWidth: true,
    gutter: 20.5,
  });

  $('.grid').imagesLoaded(function() {
    $grid.masonry();
  });


  // Initialise Tooltips
  // =======================================================
  $(function() {
    $('[data-toggle="tooltip"]').tooltip();
  });


  // Smooth scrolling for anchor links
  // =======================================================
  $('a[href^="#"]').click(function () {
    $('html, body').animate({
        scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top
    }, 500);

    return false;
  });

  // Start the Intro
  // =======================================================
  if ($('.trigger-intro').length > 0) {    
    startIntro();
  }
  function startIntro() {
    introJs().start();
  }
  $('.start-intro').on('click', startIntro);


  // Reduce font-size the titles of the cards if overflow
  // =======================================================
  $('.card').each(function() {
    var title = $(this).find('.card-gameTitle span');
    var container = $(this).find('.card-content');
    var minSize = 24;
    // var minSize = parseInt($('body').css('font-size'));
    var fontSize = 28;

    while (title.width() > container.width() && fontSize > minSize) {
      title.css('font-size', fontSize -= 0.5);
    }
    if (fontSize === minSize) {
      title.css('white-space', 'normal');
    }
    title.css('display', 'inline-block');
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
          if ($('#form-scrap').length > 0 && $('.pac-man').length === 0) {
            $('.pac-man-container').append('<div class="pac-man">');
          }
      }
  });

  $(document).ajaxStop(function() {
    if ($('.pac-man').length > 0) {
      $('.pac-man').remove();
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


  function openModal(title, textarea, gameId, noteId, success_callback) {
    if (gameId) {
      $('#modal-general').attr('data-game-id', gameId);
    }
    if (noteId) {
      $('#modal-general').attr('data-note-id', noteId);
    }
    modal_success_callback = success_callback;
    $('#modal-general h5.modal-title').text(title);
    $('#modal-general textarea').val(textarea);
    $('#modal-general').modal('show');
  }

  function closeModal() {
    $('#modal-general').modal('hide');
    if (modal_success_callback) {
      modal_success_callback();
    }
    modal_success_callback = null;
  }

  $('.modal').on('shown.bs.modal', function() {
    $(this).find('.modal-autofocus').focus();
  });

// =========================================================
// ==================     ACTIONS     ======================
// =========================================================

  // Globals
  var modal_action = null;
  var modal_success_callback = null;

  // Game Grid
  // =======================================================

  // Set a game as beaten. Stopped date and beaten True
  $('.card').on('click', '.action-finish-game', function(event){
    $('.action-finish-game').tooltip('hide');
    var gameId = $(this).parents('.card').attr('data-game-id');
    var beaten = $(this).attr('data-beaten');
    jQuery.ajax({
      method: 'PATCH',
      url: '/ajax/games/' + gameId + '/finish',
      data: {beaten: beaten},
    })
    .done(function(){
      $grid.masonry('remove', $('.card-' + gameId)).masonry();
    });
  });


  // Add a note to a game in game Grid
  // - Open modal
  $('.card').on('click', '.action-add-note', function(){
    var gameId = $(this).parents('.card').attr('data-game-id');
    var name = $(this).parents('.card').attr('data-game-name');
    modal_action = 'add-note';
    openModal('Add a note to ' + name, '', gameId, null, function() {
      location.reload();
    });
  });


  // New Game View
  // =======================================================

  $('.page-add-game #form-scrap').on('submit', function(){
    // Get metacritic information
    jQuery.get(
      '/ajax/games/scrap-metacritic',
      {metacritic_url: $('#id_metacriticUrl').val()},
      function(jsonResponse) {
        for (var key in jsonResponse) {
          if (jsonResponse.hasOwnProperty(key)) {
            var input = $('#' + 'id_' + key);
            input.val(jsonResponse[key]);
            input.addClass('success');
          }
        }
      }, 'json'
    )
    .fail(function() {
      $('.form-group.scrap-metacritic > small').text('There was a problem scrapping this url.');
    });

    // Get HLTB information
    jQuery.get(
      '/ajax/games/scrap-hltb',
      {hltb_url: $('#id_hltbUrl').val()},
      function(jsonResponse) {
        for (var key in jsonResponse) {
          if (jsonResponse.hasOwnProperty(key)) {
            var input = $('#' + 'id_' + key);
            input.val(jsonResponse[key]);
            input.addClass('success');
          }
        }
      }, 'json'
    )
    .fail(function() {
      $('.form-group.scrap-hltb > small').text('There was a problem scrapping this url.');
    });
  });

  // Today date for default value of startedAt
  // $('.form-add-game').submit(function(e){
  //   var today = new Date().toJSON().slice(0,10); 
  //   var started_at = $('#id_startedAt').val() || today;
  //   $('#id_startedAt').val(started_at);
  // });


  // Modify Game View
  // =======================================================

  // Add a note, open a modal
  $('.page-modify-game .note-list').on('click', '.action-add-note', function(){
    modal_action = 'add-note';
    var gameId = $(this).parents('.page-modify-game').attr('data-game-id');
    openModal('Add new note', '', gameId, null, function() {
      location.reload();
    });
  });


  // Edit a note, open a modal
  $('.page-modify-game .note').on('click', '.action-edit-note', function(){
    modal_action = 'edit-note';
    var gameId = $(this).parents('.note').attr('data-game-id');
    var noteId = $(this).parents('.note').attr('data-note-id');
    var note_text = $(this).parents('.note').text().trim();
    openModal('Edit note', note_text, gameId, noteId, function() {
      location.reload();
    });
  });


  // Delete a note
  $('.page-modify-game .note').on('click', '.action-delete-note', function(){
    var note = $(this).parents('.note');
    var noteId = note.data('note-id');
    var gameId = note.data('game-id');

    jQuery.ajax({
      method: 'DELETE',
      url: '/ajax/games/' + gameId + '/notes/' + noteId
    })
    .done(function(){
      note.fadeOut();
    });
  });



  // General
  // =======================================================
  // - Do modal action
  $('#modal-general').on('click', '#action-trigger-modal-action', function() {
    var gameId, nodeId, nodeText;

    switch (modal_action){
      case 'add-note':
        gameId = $('#modal-general').attr('data-game-id');
        noteText = $('#modal-general textarea').val();
        jQuery.ajax({
          method: 'POST',
          data: {'text': noteText},
          url: '/ajax/games/' + gameId + '/add-note'
        })
        .done(function() {
          closeModal();
        });
      break;

      case 'edit-note':
        gameId = $('#modal-general').attr('data-game-id');
        noteId = $('#modal-general').attr('data-note-id');
        noteText = $('#modal-general textarea').val();
        jQuery.ajax({
          method: 'PUT',
          data: {'text': noteText},
          url: '/ajax/games/' + gameId + '/notes/' + noteId
        })
        .done(function(){
          closeModal();
        });
      break;
    }
  });

});