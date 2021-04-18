$(document).on('submit', '#question-like', function (e) {
    e.preventDefault();

    $.ajax({
      type: 'POST',
      url: '/likeAjax',
      data: {
        questionID: $('#id').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },
      success: alert('Like number will be updated after you refresh the page')
    })
  })