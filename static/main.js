$(document).ready(function(){
  $('.scroll').on('click', function(e) {
  	e.preventDefault();
  	var target = $(this).attr('href');
  	var offset = 60;
    $(window).scrollTo($(target), 300, { offset: -offset });
  });

  $('.scrolltop').on('click', function(e) {
    e.preventDefault();
    $(window).scrollTo(0, 300);
  });

  $('.ui.dropdown').dropdown();
});
