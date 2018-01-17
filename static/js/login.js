$(document).ready(function() {
    $('#login-form').submit(function(){
        event.preventDefault();
        $('#sign-in-error-box').hide();
        $( "#sign-in-button" ).prop( "disabled", true );
        $( "#sign-in-button" ).html("登录中……");
        $.post('/backend/auth', {
            "username": $('#username').val(),
            "password": $('#password').val(),
            "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
        }, function(message){

            if(message['status'] == 0){
                window.location.href = "/backend/index/";
            }
            else{
                $('#sign-in-error-box').show();
                $('#sign-in-error-msg').text(message['info']);
                $( "#sign-in-button" ).prop( "disabled", false );
                $( "#sign-in-button" ).html("登录");
            }
        });
    });
});