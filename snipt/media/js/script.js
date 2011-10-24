(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  $(__bind(function() {
    $(document).bind('keyup', '/', function() {
      return $('input#search-query').focus();
    });
    $('div.infield label').inFieldLabels();
    $('section.code a.expand').click(function() {
      var el;
      el = $(this).parent();
      el.toggleClass('expanded');
      if (el.hasClass('expanded')) {
        el.css('height', 'auto');
        $(this).text('Collapse');
      } else {
        el.css('height', '200px');
        $(this).text('Expand');
      }
      return false;
    });
    return false;
  }, this));
}).call(this);
