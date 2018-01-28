(function ($) {
    $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    $.fn.checkInput = function (element){
        if($(element).val().length <= 0){
            $(element).closest('.form-group').addClass("has-danger");
            $(element).closest('form').find('button[type="submit"]').prop( "disabled", true );
            $(element).addClass('is-invalid');
            $(element).attr("placeholder", "该字段不能为空");
            return false;
        }
        return true;
    };

    $('input[type="text"], input[type="email"]').focusout(function(){
        $(this).checkInput(this);
    });
    $.fn.checkFormInputs = function(form){
        var res = true;
        $(form).find('input[type="text"], input[type="email"]').each(function(){
            res = res && $(this).checkInput(this);
        });
        return res;
    }


    $('input[type="text"], input[type="email"]').focusin(function(){
        if($(this).closest('.form-group').hasClass("has-danger")){
            $(this).closest('.form-group').removeClass("has-danger");
            $(this).closest('form').find('button[type="submit"]').prop( "disabled", false );
            $(this).removeClass('is-invalid');
            $(this).attr("placeholder", "");
        }
    });

    $('.upload-modal-form').submit(function (e) {
          e.preventDefault();
          var data = new FormData(this);
          var label = $(this).attr('label');
          $.ajax({
              url: $(this).attr('action'),
              type: $(this).attr("method"),
              dataType: "JSON",
              data: new FormData(this),
              processData: false,
              contentType: false,
              success: function (res, status){
                    console.log(res['msg']);
                    $('#'+label+"-upload-modal").modal('hide');
                    $('#'+label+"-upload-callback-modal").modal();
                    $('#'+label+"-upload-callback-msg").text(res['msg']);
              }
          });
      });


})(jQuery);

function add_form_event(callback){
    $('.add-form').submit(function (e) {
        e.preventDefault();
        var label = $(this).attr('label');
        $(this).find('.error-box').hide();
        if(!$(this).checkFormInputs(this)){
            return;
        }
        var data = $(this).serializeFormJSON();
        $.post($(this).attr('action'), data, function(res){
            if(res['code'] == 0){
                $('#'+label+'-add-modal').modal('hide');
                callback();
            }
            else{
                $('#'+label+'-add-modal').find('.error-box').show();
                $('#'+label+'-add-modal').find('.error-msg').text(res['msg']);
                return;
            }
        });

    });
}

function load_table_content(load_url, table_panel_id, table_id){
    $.get(load_url, {}, function(tableHtml){
        $(table_panel_id).html(tableHtml);
        $(table_id).DataTable();

        $('.table-edit-btn').click(function(){
            var row_item = {};
            $(this).closest('tr').find('td').each(function(){
                var attr = $(this).attr('name');
                if(typeof attr !== typeof undefined && attr !== false){
                    row_item[attr] = $(this).attr('value');
                }
            });
            var form = $($(this).attr("data-target")).find('form');
            form.find('input,select').each(function(){
                if($(this).attr('name') in row_item){
                    $(this).val(row_item[$(this).attr('name')]);
                }
            });
        });

        $('.table-remove-btn').click(function(){
            var row_item = {};
            var param = $(this).attr('param');
            $(this).closest('tr').find('td').each(function(){
                var attr = $(this).attr('name');
                if(typeof attr !== typeof undefined && attr !== false){
                    row_item[attr] = $(this).attr('value');
                }
            });
            var label = $('#remove-modal-content').attr('label');
            $('#remove-modal-content').text(row_item[label]);

            $('#remove-confirm-btn').attr('key', row_item[param]);

        });

        $('#remove-confirm-btn').click(function(){
            var url = $(this).attr('link') + $(this).attr('key')+"/";
            $.post(url, {
                "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
            }, function(res){
                if(res['code'] == 0){
                    location.reload();
                }
                else{
                    alert(res['msg']);
                    return;
                }
            });
        });

        $('.edit-form').submit(function (e) {
            e.preventDefault();
            $(this).find('.error-box').hide();
            var data = $(this).serializeFormJSON();
            var label = $(this).attr('label');
            $.post($(this).attr('action'), data, function(res){
                if(res['code'] == 0){
                    location.reload();
                }
                else{
                    $('#'+label+'-edit-modal').find('.error-box').show();
                    $('#'+label+'-edit-modal').find('.error-msg').text(res['msg']);
                    return;
                }
            });
        });
    });
}
