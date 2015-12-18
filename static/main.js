$(function(){
  $('.message .close')
    .on('click', function() {
      $(this)
        .closest('.message')
        .transition('fade')
      ;
    });

  // $('#top-message').delay(2000).fadeOut();
});
