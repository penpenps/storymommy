$(document).ready(function() {
    $('#login-form').submit(function(){
        event.preventDefault();
        if(!$(this).checkFormInputs(this)){
                    return;
                }
        $('#sign-in-error-box').hide();
        $( "#sign-in-button" ).prop( "disabled", true );
        $( "#sign-in-button" ).html("登录中……");
        $.post('/backend/auth', {
            $(this).serializeFormJSON()
        }, function(message){

            if(message['code'] == 0){
                window.location.href = "/backend/index/";
            }
            else{
                $('#sign-in-error-box').show();
                $('#sign-in-error-msg').text(message['msg']);
                $( "#sign-in-button" ).prop( "disabled", false );
                $( "#sign-in-button" ).html("登录");
            }
        });
    });
});