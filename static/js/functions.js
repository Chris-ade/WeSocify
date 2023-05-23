const MAT_INIT = {}

'use strict'

function startLoadingBar() {
$('#loading-bar').show().width((50 + Math.random() * 30) + '%');
}

function stopLoadingBar() {
$('#loading-bar').width('101%').delay(200).fadeOut(400, function () {
    $(this).width('0')
});
}

/* ----------------------------
   * Start * Preloader Service
* ----------------------------- */
$(document).ready(function () {
  startLoadingBar();
  stopLoadingBar();
});

/* -----------------------
   * Start * Toast Service
* --------------------- */
function showMessage(text) {
  iziToast.show({
    maxWidth: '280px',
    class: 'success-toast',
    icon: 'fas fa-check-circle',
    title: '',
    message: text,
    titleColor: '#fff',
    messageColor: '#fff',
    iconColor: '#fff',
    backgroundColor: '#3d70b2',
    progressBarColor: '#fafafa',
    position: 'bottomRight',
    transitionIn: 'fadeInUp',
    close: false,
    timeout: 1800,
    zindex: 99999
  });
}

function showError(text) {
  iziToast.show({
    maxWidth: '280px',
    class: 'error-toast',
    icon: 'far fa-ban',
    title: '',
    message: text,
    titleColor: '#fff',
    messageColor: '#fff',
    iconColor: '#fff',
    backgroundColor: '#ff533d',
    progressBarColor: '#fff',
    position: 'bottomRight',
    transitionIn: 'fadeInUp',
    close: false,
    timeout: 1800,
    zindex: 99999
  });
}
/* -----------------------
   * End * Toast Service
* --------------------- */

/* --------------------------
   * Start * UI Tabs Service
* --------------------------- */
$(document).ready(function () {
$(".uk-tab").find("li").click(function() {
  $(".uk-tab").find("li").removeClass("uk-active");
  $(this).addClass("uk-active");
});
});

/* --------------------------
   * Start * Publish Feed
* --------------------------- */
$(document).ready(function () {
$('main#content').on('click', '#publish', function () {
    $('#app-overlay').addClass('is-active').fadeIn();
    $('.is-new-content').addClass('is-highlighted');
    $('#close-publish').removeClass('is-hidden');
});

$('main#content').on('click', '#close-publish', function () {
  $('#app-overlay').removeClass('is-active').hide();
  $('.is-new-content, #feed-preview').removeClass('is-highlighted');
  $('#close-publish').addClass('is-hidden');
});

$('main#content').on('click', '.add-option-item.add-image', function () {
  $('#feed_image').trigger('click');
});

$('main#content').on('click', '.add-option-item.add-poll, .create-poll-footer .remove', () => {
  $('.create-poll-wrapper').toggleClass('is-active');
  if ($('.create-poll-wrapper').hasClass('is-active')) {
    $('#feed_text').attr('placeholder', 'Ask a question...');
  } else {
    $('#feed_text').attr('placeholder', 'What\'s new?');
  }
});

$('main#content').on('click', '.poll-add-field', function () {
  $('.create-poll-content .poll-field.optional-fields').toggleClass('is-active');
});

$("#compose_form").submit(function(event) {
    event.preventDefault();
    const data = new FormData(this);
    const token = $('meta[name="token"]').attr('content');
    let action = $(this).attr("action");
    data.append('action', 1);
    if($('.create-poll-wrapper').hasClass('is-active') && $('#id_form-0-choice_text, #id_form-1-choice_text, #id_form-2-choice_text, #id_form-3-choice_text').val()) {
      data.append('poll', 1);
    }
    const headers = {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': token};
    fetch(action, {
        method: 'POST',
        body: data,
        credentials: 'same-origin',
        headers: headers
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response.statusText);
        }
    })
    .then(json => {
        if (json.status === 200) {
            $(this)[0].reset();
            $("#queued-files").html("");
            showMessage(json.message);
        } else {
            throw new Error("An error occurred!");
        }
    })
    .catch(error => {
        console.error(error);
        alert("An error occurred while connecting to the server!");
    });
});

});
/* --------------------------
   * End * Publish Feed
* --------------------------- */
/* ----------------------------------
   * Start * Preview Settings Images
* ----------------------------------- */
$(document).on('change', '#profile_picture_field', function () {
  if (this.files.length > 0) {
    for (let i = 0; i < this.files.length; i++) {
      if (this.files[i]) {
        var reader = new FileReader()
        reader.onload = function (e) {
          $('#profile_picture').html('<img src="'+ e.target.result +'">')
        }
        reader.readAsDataURL(this.files[i])
      }
    }
  }
});

$(document).on('change', '#cover_picture_field', function () {
  if (this.files.length > 0) {
    for (let i = 0; i < this.files.length; i++) {
      if (this.files[i]) {
        var reader = new FileReader()
        reader.onload = function (e) {
          $('#cover_picture').find('img').replaceWith('<img src="'+ e.target.result +'">')
        }
        reader.readAsDataURL(this.files[i])
      }
    }
  }
});

$(document).ready(function () {
$('main#content').on('click', '#change_avatar', function () {
  $('#profile_picture_field').trigger('click');
});
$('main#content').on('click', '#change_cover', function () {
  $('#cover_picture_field').trigger('click');
});
});
/* --------------------------
   * End * Preview Images
* --------------------------- */

/* -----------------------
   * Start * UI Modals
* ------------------------ */
function showModal(modal) {
$(document).find(modal).removeClass('is-hidden');
$('#app-overlay').addClass('is-active').fadeIn();
}

function closeModal(modal) {
$(document).find(modal).addClass('is-hidden');
$('#app-overlay').removeClass('is-active').fadeOut();
}

htmx.on('htmx:afterSettle', (e) => {
  e.preventDefault();
  if (e.detail.target.id == 'feed-menu-modal') {
    showModal('#feed-menu-modal');
  }
});

$(document).ready(function () {
if ($('.modal-trigger').length) {
$('main#content').on('click', '.modal-trigger', function () {
  let modalID = $(this).attr('data-modal');
  $(`#${modalID}`).removeClass('is-hidden');
  $('#app-overlay').addClass('is-active');
});
}

$('main#content').on('click', '.ui-modal-close', function () {
let modalContainer = $(this).closest('.ui-modal-container');
modalContainer.addClass('is-hidden');
$('#app-overlay').removeClass('is-active');
});

});
/* -----------------------
   * End * UI Modals
* ------------------------ */

/* --------------------------
   * Start * Password Toggle
* --------------------------- */
$(document).ready(function () {
const togglePassword = $("#toggle-password");
const input = $("#password");
if (togglePassword.length && input.length) {
  togglePassword.click(function(){
  if (input.attr("type") === "password") {
    input.attr("type", "text");
    togglePassword.html('<svg class="icon icon--20" width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20 9C20 9 19.6797 9.66735 19 10.5144M12 14C10.392 14 9.04786 13.5878 7.94861 13M12 14C13.608 14 14.9521 13.5878 16.0514 13M12 14V17.5M4 9C4 9 4.35367 9.73682 5.10628 10.6448M7.94861 13L5 16M7.94861 13C6.6892 12.3266 5.75124 11.4228 5.10628 10.6448M16.0514 13L18.5 16M16.0514 13C17.3818 12.2887 18.3535 11.3202 19 10.5144M5.10628 10.6448L2 12M19 10.5144L22 12"></path></svg>');
  } else {
    input.attr("type", "password");
    togglePassword.html('<svg class="icon icon--20" viewBox="0 0 24 24"><path d="M22 12C22 12 19 18 12 18C5 18 2 12 2 12C2 12 5 6 12 6C19 6 22 12 22 12Z"></path><circle cx="12" cy="12" r="3"></circle></svg>');
        }
    });
  }
});
/* --------------------------
   * End * Password Toggle
* --------------------------- */

/* --------------------------
   * Start * Parallax Layers
* --------------------------- */
$(document).ready(function () {
if ($('#particles-js').length) {
    particlesJS('particles-js', {
      particles: {
        number: {
          value: 50,
          density: {
            enable: true,
            value_area: 1000
          }
        },
        color: {
          value: ['#5596e6']
        },
        shape: {
          type: 'circle',
          stroke: {
            width: 5,
            color: '#5596e6'
          },
          fill: {
            color: '#5596e6'
          },
          polygon: {
            nb_sides: 5
          },
          image: {
            src: 'img/github.svg',
            width: 100,
            height: 100
          }
        },
        opacity: {
          value: 0.6,
          random: false,
          anim: {
            enable: false,
            speed: 1,
            opacity_min: 0.1,
            sync: false
          }
        },
        size: {
          value: 4,
          random: true,
          anim: {
            enable: false,
            speed: 40,
            size_min: 0.1,
            sync: false
          }
        },
        line_linked: {
          enable: false,
          distance: 120,
          color: '#1a72ff',
          opacity: 0.2,
          width: 1.6
        },
        move: {
          enable: true,
          speed: 3,
          direction: 'top',
          random: false,
          straight: false,
          out_mode: 'out',
          bounce: false,
          attract: {
            enable: false,
            rotateX: 600,
            rotateY: 1200
          }
        }
      },
      interactivity: {
        detect_on: 'canvas',
        events: {
          onhover: {
            enable: true,
            mode: 'grab'
          },
          onclick: {
            enable: false
          },
          resize: true
        },
        modes: {
          grab: {
            distance: 140,
            line_linked: {
              opacity: 1
            }
          },
          bubble: {
            distance: 400,
            size: 40,
            duration: 2,
            opacity: 8,
            speed: 3
          },
          repulse: {
            distance: 200,
            duration: 0.4
          },
          push: {
            particles_nb: 4
          },
          remove: {
            particles_nb: 2
          }
        }
      },
      retina_detect: true
    })
  }
});
/* --------------------------
   * End * Parallax Layers
* --------------------------- */

/* -----------------------------
  * Materialize
* --------------------------- */
MAT_INIT.Materialize = function () {
$.material.init();
$('.checkbox > label').on('click', function () {
  $(this).closest('.checkbox').addClass('clicked');
});
}

$(document).ready(function () {  
MAT_INIT.Materialize();
});
/* -------------------------
   * End * Init Materialize
* -------------------------- */

/* --------------------------
   * Start * Preview Images
* --------------------------- */
$(document).ready(function() {
  const feedImage = $("#feed_image");
  const queuedFiles = $("#queued-files");
  const selectedFiles = $(".selected-files");
  if(feedImage.length && queuedFiles.length && selectedFiles.length) {
    feedImage.on("change", async () => {
      if (feedImage[0].files.length > 0) {
        queuedFiles.html("");
        selectedFiles.show();
  
        for (const file of feedImage[0].files) {
          const url = URL.createObjectURL(file);
          const img = $("<img>", {src: url});
  
          // create a "remove" button for the image
          const removeButton = $("<button>", {html: `<svg role="img" class="icon icon--20" width="24" height="24" viewBox="0 0 24 24"><path d="M6.34314575 6.34314575L17.6568542 17.6568542M6.34314575 17.6568542L17.6568542 6.34314575"></path></svg>`});
          removeButton.addClass("button-close");
          removeButton.click(function(){
            $(this).closest('.si-box').remove();
            // check if there are no more images left, if yes hide the selected-files element
            if (queuedFiles.children().length === 0) {
              selectedFiles.hide();
            }
          });
          
          //create a div with class 'si-box'
          const siBox = $("<div>").addClass("si-box");
          
          //create a child div with class 'si-box-inner'
          const siBoxInner = $("<div>").addClass("si-box-inner").css("background-image", `url(${url})`);
  
          siBox.append(siBoxInner);
          siBox.append(removeButton);
          queuedFiles.append(siBox);
        }
      } else {
        queuedFiles.html("");
        selectedFiles.hide();
      }
    });
  }
});
/* --------------------------
   * End * Preview Images
* --------------------------- */

/* --------------------------
   * Start * Repost Feed
* --------------------------- */
$(document).ready(function() {
$('main#content').on('click', '.repost-feed', function(event) {
    event.preventDefault();
    const target = $(this).data('id');
    const token = $('meta[name="token"]').attr('content');
    const headers = { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': token };
    const data = { target };
    fetch(`/feed/repost/`, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: headers
    })
    .then(response => {
      if (response.status === 200) {
        return response.json();
    } else {
        throw new Error(response.statusText);
      }
    })
    .then(jsonResponse => {
      if(jsonResponse.status === 200) {
        $(`#feed-container`).prepend(jsonResponse.feed);
        showMessage(jsonResponse.message);
      }
      else if (jsonResponse.status === 201) {
        $(`#feed${target}`).fadeOut();
      }
      else {
        showError('An error occurred!');
      }
    })
    .catch(error => {
      console.error(error);
      showError('An error occurred!')
    });
  });
});

/* --------------------------
   * Start * Like Feed
* --------------------------- */
$(document).ready(function() {
$('main#content').on('click', '.like-button, #like-button', function(event) {
    event.preventDefault();
    alert("Hi");
    const target = $(this).data('id');
    const token = $('meta[name="token"]').attr('content');
    const headers = { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': token };
    const data = { target };
    fetch(`/feed/like/`, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: headers
    })
    .then(response => {
      if (response.status === 200) {
        return response.json();
    } else {
        throw new Error(response.statusText);
      }
    })
    .then(jsonResponse => {
      if(jsonResponse.status === 200) {
        $(`#feed${target}`).replaceWith(jsonResponse.feed);
      }
      else {
        showError('An error occurred!');
      }
    })
    .catch(error => {
      console.error(error);
      showError('An error occurred!')
    });
  });
});

/* --------------------------
   * Start * Delete Feed
* --------------------------- */
$(document).ready(function() {
$('main#content').on('click', '.delete-feed', function(event) {
    event.preventDefault();
    const target = $(this).data('id');
    const token = $('meta[name="token"]').attr('content');
    const headers = { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': token };
    fetch(`/feed/delete/${target}/`, {
      method: 'DELETE',
      headers: headers
    })
    .then(response => {
    if (response.status === 200) {
        return response.json();
    } else {
        throw new Error(response.statusText);
      }
    })
    .then(jsonResponse => {
      $(`#feed${target}`).fadeOut();
      $('#app-overlay').removeClass('is-active').hide();
      showMessage(jsonResponse.message);
    })
    .catch(error => {
      console.error(error);
      showError('An error occurred!');
    });
  });
});

$(document).ready(function() {
$('main#content').on('click', '#more_button', function(event) {
    event.preventDefault();
    const target = $(this).data('id');
    const token = $('meta[name="token"]').attr('content');
    const headers = { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': token };
    const data = new FormData();
    data.append('page', target);
    fetch(`/feed/more/`, {
        method: 'POST',
        body: data,
        credentials: 'same-origin',
        headers: headers
    })
    .then(response => {
      if (response.status === 200) {
        return response.json();
    } else {
        throw new Error(response.statusText);
    }
    })
    .then(jsonResponse => {
      $('#feed-container').append(jsonResponse.feeds);
    })
    .catch(error => {
      console.error(error);
      showError('An error occurred!')
    });
 });
});

/* --------------------------
   * Start * Misc Services
* --------------------------- */
$(document).ready(function() {
/* --------------------------
   * Start * Tokenization :)
* --------------------------- */
$('body').on('htmx:configRequest', function (e) {
  const token = $('meta[name="token"]').attr('content');
  e.detail.headers['X-CSRFToken'] = token;
});

/* --------------------------
   * Start * Load More Feed
* --------------------------- */
$('main#content').on('click', '#load-more', function (e) {
    e.preventDefault();
    const loadMoreBtn = $(this);
    loadMoreBtn.addClass('loading');
    const target = loadMoreBtn.data('id');
    setTimeout(function () {
      loadMoreBtn.removeClass('loading');
      $('.no_data').hide();
      $('.no_data').remove();
    }, 3500);
});

/* --------------------------
   * Start * Preview Feed
* --------------------------- */
// Preview text input
const feedText = document.getElementById('feed_text');
  if(feedText) {
  feedText.addEventListener('input', function() {
    const text = this.value;
    const feedTextPreview = document.getElementById('feed-text-preview');
    feedTextPreview.textContent = text;
  });
}
  // Preview image input
  const feedImage = document.getElementById('feed_image');
  if (feedImage) {
  feedImage.addEventListener('change', function() {
    const target = this;
    if (target.files.length > 0) {
      const feedImagePreview = document.getElementById('feed-image-preview');
      feedImagePreview.innerHTML = '';
      const files = Array.from(target.files);
      const previews = files.map(file => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        return new Promise(resolve => {
          reader.onload = event => {
            resolve(event.target.result);
          }
        });
      });
      Promise.all(previews).then(images => {
        let html = '';
        if (images.length === 1) {
          html = `<div class="feed-image"><a class="feed-image-item" style="background-image: url(${images[0]});"></a></div>`;
        } else if (images.length === 2) {
          html = `<div class="feed-image">
            <div class="feed-image-column">
              ${images.map(img => `<a class="feed-image-item" style="background-image: url(${img});"></a>`).join('')}
            </div>
          </div>`;
        } else if (images.length === 3) {
          html = `<div class="feed-masonry-grid">
            <div class="feed-masonry-column">
              <a style="background-image: url(${images[0]});"></a>
            </div>
            <div class="feed-masonry-columns">
              ${images.slice(1).map(img => `<a style="background-image: url(${img});"></a>`).join('')}
            </div>
          </div>`;
        } else if (images.length === 4) {
          html = `<div class="feed-masonry-grid">
            <div class="feed-masonry-column">
              <a style="background-image: url(${images[0]});"></a>
            </div>
            <div class="feed-masonry-columns">
              ${images.slice(1, 4).map(img => `<a style="background-image: url(${img});"></a>`).join('')}
            </div>
          </div>`;
        } else if (images.length > 4) {
        html = `<div class="feed-masonry-grid">
            <div class="feed-masonry-column">
              <a style="background-image: url(${images[0]});"></a>
            </div>
            <div class="feed-masonry-columns">
              ${images.slice(1, 4).map(img => `<a style="background-image: url(${img});"></a>`).join('')}
              ${images.map(img => `<span class="bg-gray-900 bg-opacity-30">+${images.length - 4} more</span>`).join('')}
            </div>
          </div>`;
        }
        feedImagePreview.innerHTML = html;
      });
    }
  });
}

/* --------------------------
  * Start * Update Feed
* --------------------------- */
$('main#content').on('click', '.update-feed', function(e) {
  e.preventDefault();
  try {
    const target = $(this).data('id');
    const content = $(`#feed-text${target}`).text();
    $('#feed-menu-modal').hide();
    $('#update-modal').removeClass('is-hidden');
    $('#update_form').find('textarea').val(content);
    $('#update_form').data('id', target);
  } catch (err) {
    console.error(err);
  }
});

$('main#content').on('submit', '#update_form', function(e) {
  e.preventDefault();
  const target = $(this).data('id');
  const content = $(this).find('textarea').val();
  const token = $('meta[name="token"]').attr('content');
  const data = { id: target, content };
  const headers = { 'Content-Type': 'application/json', 'X-CSRFToken': token };
  fetch('/feed/edit/', {
    method: 'PATCH',
    body: JSON.stringify(data),
    credentials: 'same-origin',
    headers: headers
  })
    .then(response => {
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        return response.json();
    })
    .then(jsonResponse => {
      const feedContainer = $('.feed-container');
      const feed = feedContainer.find(`#feed${target}`);
      feed.replaceWith(jsonResponse.feed);
      showMessage(jsonResponse.message);
      closeModal('#update-modal');
    })
    .catch(error => {
      console.error(error);
      showError(`An error occurred while connecting to the server!`);
    });
});

/* --------------------------
   * Start * Comment
* --------------------------- */
$('main#content').on('submit', 'form.comment_form', function(e) {
    e.preventDefault();
    const form = $(this);
    const target = form.data('id');
    const token = $('meta[name="token"]').attr('content');
    const action = form.attr('action');
    const data = new FormData(form[0]);
    const options = {
        method: 'POST',
        body: data,
        headers: {
            "X-CSRFToken": token
        }
    };
    fetch(action, options)
        .then(response => {
            if (response.ok) {
              return response.json();
            } else {
                throw new Error(response.data.message);
            }
        })
        .then(response => {
            form[0].reset();
            const comments = $(`#comments${target}`);
            comments.append(response.comment);
            showMessage(response.message);
        })
        .catch(err => {
          console.error(err);
            alert(`An error occurred while connecting to the server!`);
        });
});
/* --------------------------
   * Start * Feed Poll Voting
* --------------------------- */
$('main#content').on('click', '.ui-poll-wrapper a', function(e) {
    e.preventDefault();
    const target = $(this);
    const choice = target.data('choice');
    const feed = target.closest('.ui-poll-wrapper').data('feed');
    const id = target.closest('.ui-poll-wrapper').data('poll');
    const data = { choice, feed, poll: id };
    const token = $('meta[name="token"]').attr('content');
    const headers = { "Content-Type": "application/json", "X-CSRFToken": token };
    fetch('/feed/poll/vote/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: headers
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response.statusText);
        }
    })
    .then(jsonResponse => {
        $(`#ui-poll${id}`).replaceWith(jsonResponse.response);
    })
    .catch(error => {
        console.error(error);
        showError('An error occurred while connecting to the server!')
    });
});

});
/* --------------------------
   * End * Misc Services
* --------------------------- */