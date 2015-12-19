// https://github.com/ghiculescu/jekyll-table-of-contents
(function($) {
  $.fn.toc = function(options) {
    var defaults = {
        noBackToTopLinks: true,
        title: '',
        minimumHeaders: 3,
        headers: 'h1, h2, h3',
        container: 'div.canvas',
        listType: 'ol', // values: [ol|ul]
        showEffect: 'show', // values: [show|slideDown|fadeIn|none]
        showSpeed: 'slow' // set to 0 to deactivate effect
      },
      settings = $.extend(defaults, options);

    function fixedEncodeURIComponent(str) {
      return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
        return '%' + c.charCodeAt(0).toString(16);
      });
    }

    selector = settings.container + ' ' + settings.headers

    var headers = $(selector).filter(function() {
        // get all headers with an ID
        // FIXME don't understand yet
        var previousSiblingName = $(this).prev().attr("name");
        if (!this.id && previousSiblingName) {
          this.id = $(this).attr("id", previousSiblingName.replace(/\./g, "-"));
        }
        return this.id;
      }),
      output = $(this);

    if (!headers.length || headers.length < settings.minimumHeaders || !output.length) {
      $(this).hide();
      return;
    }

    if (0 === settings.showSpeed) {
      settings.showEffect = 'none';
    }

    var render = {
      show: function() {
        output.hide().html(html).show(settings.showSpeed);
      },
      slideDown: function() {
        output.hide().html(html).slideDown(settings.showSpeed);
      },
      fadeIn: function() {
        output.hide().html(html).fadeIn(settings.showSpeed);
      },
      none: function() {
        output.html(html);
      }
    };

    var get_level = function(ele) {
      return parseInt(ele.nodeName.replace("H", ""), 10);
    }

    var highest_level = headers.map(function(_, ele) {
      return get_level(ele);
    }).get().sort()[0];

    var return_to_top = '<i class="arrow up icon .back-to-top"></i>';

    var level = get_level(headers[0]),
      this_level,
      html = settings.title + " <" + settings.listType + ">";

    headers.on('click', function() {
        if (!settings.noBackToTopLinks) {
          window.location.hash = this.id;
        }
      })
      .addClass('clickable-header')
      .each(function(_, header) {
        this_level = get_level(header);

        // make it a semantic-ui header :)
        if (this_level === highest_level) {
          $(header).addClass('ui header');
        }

        if (this_level === level) {
          // same level as before; same indenting
          html += "<li><a href='#" + fixedEncodeURIComponent(header.id) + "'>" + header.innerHTML + "</a>";
        }
        else if (this_level <= level) {
          // higher level than before; end parent ol
          for (i = this_level; i < level; i++) {
            html += "</li></" + settings.listType + ">"
          }
          html += "<li><a href='#" + fixedEncodeURIComponent(header.id) + "'>" + header.innerHTML + "</a>";
        }
        else if (this_level > level) {
          // lower level than before; expand the previous to contain a ol
          for (i = this_level; i > level; i--) {
            html += "<" + settings.listType + "><li>"
          }
          html += "<a href='#" + fixedEncodeURIComponent(header.id) + "'>" + header.innerHTML + "</a>";
        }
        level = this_level; // update for the next one
      });

    html += "</" + settings.listType + ">";

    // show()
    render[settings.showEffect]();
  };
})(jQuery);
