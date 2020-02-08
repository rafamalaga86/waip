


// Detect broken images
// =======================================================
const image_repo = 'http://images.waip.rafaelgarciadoblas.com';

$('img').on('error', function() { // Event on image broken
  const src = $(this).attr('src');
  $(this).parent().addClass('card-bg-3'); // Mark as image not found

  if (!src.includes(image_repo)) { // Prevent a loop if the image doesnt exist in image_repo
    const file_name = src.substring(src.lastIndexOf('/') + 1);
    const username  = $('body').data('user-username');
    const own_url   = image_repo + '/' + username + '/' + file_name;
    $(this).attr('src', own_url);
  } else {
    $(this).data('old-src', own_url);
    $(this).attr('src', '/static/404.jpg');
  }
});


$(document).ready(function() {

  // Initialise the Mansonry Grid
  // =======================================================
  const $grid = $('.grid').masonry({
    itemSelector: '.card',
    fitWidth: true,
    gutter: 20.5,
  });

  $('.grid').imagesLoaded(function() {
    setTimeout(() => { $grid.masonry(); }, 500);
  });

  // Initialise Tooltips
  // =======================================================
  $(function() {
    $('[data-toggle="tooltip"]').tooltip();
  });


  // Side menu
  // =======================================================

  $('.navbar-toggler-2').on('click', function () {
     $('#sidebar').toggleClass('active');
     $(this).toggleClass('active');
  });
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#dismiss, .overlay').on('click', function () {
        $('#sidebar').removeClass('active');
        $('.overlay').fadeOut();
    });

    $('.navbar-toggler').on('click', function () {
        $('#sidebar').addClass('active');
        $('.overlay').fadeIn();
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
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

  $('.score-metacritic_score').each(function() {
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

  // Set a game as stopped_playing
  $('.card').on('click', '.action-finish-game', function(event){
    $('.action-finish-game').tooltip('hide');
    var gameId = $(this).parents('.card').attr('data-game-id');
    var beaten = $(this).attr('data-beaten');
    jQuery.ajax({
      method: 'PATCH',
      url: '/ajax/games/' + gameId + '/finish',
      data: {beaten: beaten},
    })
    .done(function() {
      $grid.masonry('remove', $('.card-' + gameId)).masonry();
    });
  });


  // Redirect people to login view
  $('.card').on('click', '.action-go-login-page', function() {
    location.href = "/login";
  });


  // Add a note to a game in game Grid
  // - Open modal
  $('.card').on('click', '.action-add-note', function() {
    var gameId = $(this).parents('.card').attr('data-game-id');
    var name = $(this).parents('.card').attr('data-game-name');
    modal_action = 'add-note';
    openModal('Add a note to ' + name, '', gameId, null, function() {
      location.reload();
    });
  });


  // New Game View
  // =======================================================

  $('.page-add-game #form-scrap').on('submit', function() {
    // Get metacritic information
    jQuery.get(
      '/ajax/games/scrap-metacritic',
      {metacritic_url: $('#id_metacriticUrl').val()},
      function(jsonResponse) {
        $('.form-group.scrap-metacritic > small').text('');
        for (var key in jsonResponse) {
          if (jsonResponse.hasOwnProperty(key)) {
            var input = $('#' + 'id_' + key);
            input.val(jsonResponse[key]);
            input.addClass('success');
          }
        }
      }, 'json'
    )
    .fail(function(jqxhr) {
      $('.form-group.scrap-metacritic > small').text(jqxhr.responseText);
    });

    // Get HLTB information
    jQuery.get(
      '/ajax/games/scrap-hltb',
      {hltb_url: $('#id_hltbUrl').val()},
      function(jsonResponse) {
        $('.form-group.scrap-hltb > small').text('');
        for (var key in jsonResponse) {
          if (jsonResponse.hasOwnProperty(key)) {
            var input = $('#' + 'id_' + key);
            input.val(jsonResponse[key]);
            input.addClass('success');
          }
        }
      }, 'json'
    )
    .fail(function(jqxhr) {
      $('.form-group.scrap-hltb > small').text(jqxhr.responseText);
    });
  });

  // Put today's day when someone click in Today's button
  $('.put-todays-date').on('click', function() {
    $(this).parent().parent().find('.get-todays-date').val(new Date().toJSON().slice(0,10));
    return false;
  });


  // Modify Game View
  // =======================================================

  // Add a played
  $('.action-add-played').on('click', function() {
    $('.played-list').append(
      `<div class="mb-30 played appended" data-id="-1">
        <div>
          <div class="mb-0">
            <a href="" class="field-info put-todays-date"><small>Today</small></a>
            <input value="" class="form-control get-todays-date" type="date" name="stopped_playing_at" id="id_stopped_playing_at">
          </div>
          <div class="btn-toolbar mb-0">

            <div class="checkbox-wrapper">
              <label class="checkbox-fancy-label">
                <i class="fa fa-check"></i>
                <input name="beaten" type="checkbox" {{ played.beaten|yesno:'checked,' }}>
              </label>
              <label>Beaten?</label>
            </div>

            <div class="btn-margin-left">
              <button class="save-played btn btn-primary ml-10 not-saved">
                <div class="icon-container">
                  <i class="fa fa-save"></i>
                </div>
              </button>

              <button class="delete-played btn btn-danger ml-10">
                <div class="icon-container">
                  <i class="fa fa-trash"></i>
                  </div>
              </button>
            </div>

          </div>
        </div>
      </div>`
    );
    $('.played-list').children().last().slideDown();
  });

  // Detects changes in inputs or selects of playeds
  $('.played-list').on('change', ':input', function() {
    var save_button = $(this).closest('.played').find('.save-played');
    save_button.addClass('not-saved');
  });

  var spinner_loader = '<div class="loader"></div>';
  var trash          = '<div><i class="fa fa-trash"></i></div>';
  var check          = '<div><i class="fa fa-check"></i></div>';
  var save           = '<div><i class="fa fa-save"></i></div>';


  // Save Played
  $('.played-list').on('click', '.save-played', function() {
    var entry          = $(this).closest('.played');
    var save_button    = entry.find('.save-played');
    var game_id        = $('.data-game-id').data('game-id');
    var id             = entry.data('id');
    var icon_container = $(this).children();
    var is_put         = id !== -1; // If ID is not -1 it means is an existing record and we have to PUT it

    icon_container.html(spinner_loader); // Put the spinner
    $('.field-errors.playeds').text('');

    $.ajax({
      type: is_put ? 'PUT' : 'POST',
      url: is_put ? '/ajax/games/' + game_id + '/playeds/' + id : '/ajax/games/' + game_id + '/add-played',
      data: entry.find(':input').serialize(),

      success: function(response) {
        save_button.removeClass('not-saved');
        icon_container.html(check); // Put the check icon

        entry.data('id', response.id); // Put the ID in the entry so next time this entry is modified the app sends a PUT instead of a POST
        setTimeout(function() {
            icon_container.html(save);
        }, 1000);
      },

      error: function(response) {
        $('.field-errors.playeds').text(response.responseText);
        entry.find('.invalid').removeClass('invalid'); // If any input had border reds for errors, restore

        // Put back the Save icon
        icon_container.html(save);
      },
    });
  });


  // Delete Played
  $('.played-list').on('click', '.delete-played', function() {
    var entry          = $(this).closest('.played');
    var game_id        = $('.data-game-id').data('game-id');
    var id             = entry.data('id');
    var icon_container = $(this).children();

    if (id === -1) { // This is a just created entry and it is not in the DB yet
      entry.slideUp(400, function(){
        $(this).remove(); // After sliding up, remove the element
      });
    } else { // This is an entry that is already in the DB and we have to delete it
      $(this).children().html(spinner_loader); // Put the spinner loader

      $.ajax({
        type: 'DELETE',
        url: '/ajax/games/' + game_id + '/playeds/' + id,

        success: function() {
            entry.slideUp(400, function() {
                $(this).remove(); // After sliding up, remove the element
            });
        },

        error: function(response) {
          $('.field-errors.playeds').text(response.responseText);
        },

        complete: function() {
            icon_container.html(trash); // Back the trash icon
        }
      });
    }
  });


  // Add a note, open a modal
  $('.page-modify-game .note-list').on('click', '.action-add-note', function() {
    modal_action = 'add-note';
    var gameId = $(this).parents('.page-modify-game').attr('data-game-id');
    openModal('Add new note', '', gameId, null, function() {
      location.reload();
    });
  });


  // Edit a note, open a modal
  $('.page-modify-game .note').on('click', '.action-edit-note', function() {
    modal_action = 'edit-note';
    var gameId = $(this).parents('.note').attr('data-game-id');
    var noteId = $(this).parents('.note').attr('data-note-id');
    var note_text = $(this).parents('.note').text().trim();
    openModal('Edit note', note_text, gameId, noteId, function() {
      location.reload();
    });
  });


  // Delete a note
  $('.page-modify-game .note').on('click', '.action-delete-note', function() {
    var note = $(this).parents('.note');
    var noteId = note.data('note-id');
    var gameId = note.data('game-id');

    jQuery.ajax({
      method: 'DELETE',
      url: '/ajax/games/' + gameId + '/notes/' + noteId
    })
    .done(function() {
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
        .done(function() {
          closeModal();
        });
      break;
    }
  });


  // 'Read more' and 'Show less' functionality
  // =======================================================

  var maxChar = 800;  // How many characters are shown by default
  var ellipsesText = '...';
  var moretext = '> Show more';
  var lesstext = '< Show less';
  var contentStorage = [];
  var contentReducedStorage = [];

  $('.card-text.notes').each(function() {
    var cardId = $(this).parents('.card').attr('data-game-id');
    var content = $(this);

    // Trim notes while they exceed maxChar and leave at least one
    if (getText(content).length > maxChar ) {

      var contentReduced = $(this).clone();
      contentReduced.find('p.note').last().addClass('trim');

      var contentReducedTrimmed = $(this).clone();
      contentReducedTrimmed.find('p.note').last().remove();

      while (
        getText(contentReduced).length > maxChar &&
        getText(contentReducedTrimmed).length > maxChar &&
        contentReduced.children('p.note').length > 1
      ) {
        contentReducedTrimmed.find('p.note').last().addClass('trim');
        contentReduced = contentReducedTrimmed.clone();
        contentReducedTrimmed.find('p.note.trim').remove();
      }

      // Count characters to substract
      var maxCharParagraph = maxChar - countCharacters(contentReducedTrimmed);

      // Go to the paragraph where goes the "read more" and trim it
      var tagToTrim = contentReduced.find('p.note.trim');
      var tagToTrimText = getText(tagToTrim);
      if (tagToTrimText.length > maxCharParagraph) {
        var html = tagToTrimText.substr(0, maxCharParagraph) +
          '<span class="more-ellipses">' + ellipsesText + '&nbsp;</span>';
        tagToTrim.html(html);
      }

      content.append('<a href="" class="more-link less">' + lesstext + '</a>');
      contentReduced.append('<a href="" class="more-link">' + moretext + '</a>');

      // Save contents
      contentStorage[cardId] = content;
      contentReducedStorage[cardId] = contentReduced;


      content.replaceWith(contentReduced);
    }
  });

  $('.card').on('click', '.more-link', function() {
    var currentContent = $(this).parents('.card-text.notes');
    var cardId = $(this).parents('.card').attr('data-game-id');
    var contentReduced = contentReducedStorage[cardId];
    var content = contentStorage[cardId];

    currentContent.replaceWith($(this).hasClass('less') ? contentReduced : content);

    $grid.masonry(); // Order the Masonry again
    return false;
  });

  function getText(domTag) {
    return domTag.text().replace(/\s\s+/g, ' ');
  }

  // Count characters in an group of jquery dom elements
  function countCharacters(group) {
    var count = 0;
    group.each(function() {
      count += $(this).text().replace(/\s\s+/g, ' ').length;
    });
    return count;
  }


});