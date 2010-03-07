$(document).ready(function(){


  $('#attachment-form').dialog({
    autoOpen: false,
    width: 330,
    height: 150,
    modal: true,
  });


  $('#new-attachment').click(function() {
    $('#attachment-form').dialog('open');
    return false;
  });

});