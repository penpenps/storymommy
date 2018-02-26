$(document).ready(function(){
    $('.add-form').submit(function (e) {
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
            if(res['code'] == 0){
                $('#'+label+'-add-modal').modal('hide');
                callback();
            }
            else{
                $('.add-form').find('.error-box').show();
                $('.add-form').find('.error-msg').text(res['msg']);
                return;
            }
        });

    });
});