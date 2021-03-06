function validate_username() {
    var $username_field = $('#id_ocf_login_name'),
        $username_feedback = $('#username-feedback');
    $.ajax({
         type: 'GET',
         url: 'validate',
         data: {'username': $username_field.val(),
                'real_name': $('#real-name').text()},
         success: function(data) {
             if(data.is_valid) {
                $username_field.parent().removeClass('has-error')
                               .addClass('has-success');
                $username_feedback.removeClass('alert-danger')
                                  .addClass('alert-success');
             } else {
                $username_field.parent().removeClass('has-success')
                               .addClass('has-error');
                $username_feedback.removeClass('alert-sucess')
                                  .addClass('alert-danger');
             }
             $username_feedback.show().text(data.msg);
         }
     });
 }

function recommend() {
    $.ajax({
         type: 'GET',
         url: 'recommend',
         data: {'real_name': $('#real-name').text()},
         success: function(data) {
             $('#recommendations').empty();
             var recommendations = data['recommendations'];
             for (var i in recommendations) {
                 var recommendation = recommendations[i];
                 $('#recommendations').append(
                     $('<button>', {
                         type: 'button',
                         class: 'list-group-item list-group-item-action list-group-item-success recommendation',
                         onclick: '$("#id_ocf_login_name").val("' + recommendation + '").trigger("keyup");',
                         text: recommendation,
                     })
                 );
             }
         }
     });
}


$(document).ready(function() {
    // Quick validation of username field
    var finTypingCountdown = 250; // 250 milliseconds
    var typingTimer;
    var $input = $('#id_ocf_login_name');

    // On keyup, start countdown
    $input.keyup(function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(validate_username, finTypingCountdown);
    });

    // On keydown, clear countdown
    $input.keydown(function() {
        clearTimeout(typingTimer);
    });

    // Load in recommendations
    recommend();
});
