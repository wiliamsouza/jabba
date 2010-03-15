$(document).ready(function(){

  $('.draggable').draggable({
    revert: 'invalid',
    activeClass: 'dragg-highlight',
  });

  $('.droppable').droppable({
    accept: '.draggable',
    activeClass: 'ui-state-highlight',
    drop: function(event, ui) {
      updateTask(ui.draggable, $(this));
    }
  });

  function updateTask($task, $team) {
    var $task_id = $task.find('span#task_id').text();
    var $team_id = $team.find('li#team_id').text();
    var $team_count = $team.find('li#task_count');
    var t_count = parseInt($team_count.text());
    t_count++;
    $team_count.text(t_count + ' Tasks');
    $.post('/task/' + $task_id + '/change/team/' + $team_id + '/');
    $task.fadeOut();
  }

  $('#id_show_from').datepicker();

  $('#id_due').datepicker();

  $('#priority-form').dialog({
    autoOpen: false,
    width: 330,
    height: 150,
    modal: true,
  });

  $('#change-priority').click(function() {
    $('#priority-form').dialog('open');
    return false;
  });

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

  $('#team-form').dialog({
    autoOpen: false,
    width: 330,
    height: 150,
    modal: true,
  });

  $('#change-team').click(function() {
    $('#team-form').dialog('open');
    return false;
  });

  $('#context-form').dialog({
    autoOpen: false,
    width: 330,
    height: 150,
    modal: true,
  });

  $('#change-context').click(function() {
    $('#context-form').dialog('open');
    return false;
  });
});