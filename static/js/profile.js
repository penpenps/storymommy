$(document).ready(function(){
    $('#edit-profile-form').submit(function (e) {
        e.preventDefault();
        var submit_btn = $(this).find('button[type="submit"]');
        submit_btn.prop( "disabled", true );
        var label = $(this).attr('label');
        $(this).find('.error-box').hide();
        if(!$(this).checkFormInputs(this)){
            submit_btn.prop( "disabled", false );
            return;
        }
        var data = $(this).serializeFormJSON();
        $.post($(this).attr('action'), data, function(res){
            submit_btn.prop( "disabled", false );
            if(res['code'] == 1){
                $('#edit-profile-modal').find('.error-box').show();
                $('#edit-profile-modal').find('.error-msg').text(res['msg']);
                return;
            }
            $('#edit-profile-modal').modal('hide');
            $('.profile-item[name="name"]').text(res['name']);
            $('.profile-item[name="phone"]').text(res['phone']);
            $('.profile-item[name="email"]').text(res['email']);
            $('#success-alert').alert();
            $('#success-alert').show();

        });
    });

    $('#update-password-form').submit(function (e) {
        e.preventDefault();
        var submit_btn = $(this).find('button[type="submit"]');
        submit_btn.prop( "disabled", true );
        var label = $(this).attr('label');
        $(this).find('.error-box').hide();
        if(!$(this).checkFormInputs(this)){
            return;
        }
        if($('#password').val().length == 0){
            submit_btn.prop( "disabled", false );
            $('#update-password-modal').find('.error-box').show();
            $('#update-password-modal').find('.error-msg').text("密码不能为空");
            return;
        }
        if($('#password').val() != $('#confirm-password').val()){
            submit_btn.prop( "disabled", false );
            $('#update-password-modal').find('.error-box').show();
            $('#update-password-modal').find('.error-msg').text("两次输入密码不一致");
            return;
        }
        var data = $(this).serializeFormJSON();
        $.post($(this).attr('action'), data, function(res){
            submit_btn.prop( "disabled", false );
            if(res['code'] == 1){
                $('#update-password-modal').find('.error-box').show();
                $('#update-password-modal').find('.error-msg').text(res['msg']);
                return;
            }
            $('#update-password-modal').modal('hide');
            $('#success-alert').alert();
            $('#success-alert').show();

        });
    });
});


