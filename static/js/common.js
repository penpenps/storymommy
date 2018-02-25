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
        if($(element).val().length <= 0 || $(element).val() == "" || $(element).val() == undefined){
            $(element).closest('.form-group').addClass("has-danger");
            $(element).closest('form').find('button[type="submit"]').prop( "disabled", true );
            $(element).addClass('is-invalid');
            $(element).attr("placeholder", "该字段不能为空");
            return false;
        }
        return true;
    };

    $('input[type="text"], input[type="email"], input[type="number"]').focusout(function(){
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
          var submit_btn = $(this).find('button[type="submit"]');
          submit_btn.prop( "disabled", true );
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
//                    console.log(res['msg']);
                    submit_btn.prop( "disabled", false );
                    $('#'+label+"-upload-modal").modal('hide');
                    $('#'+label+"-upload-callback-modal").modal();
                    $('#'+label+"-upload-callback-msg").text(res['msg']);
              }
          });
      });

    $(".form_datetime").datetimepicker({format: 'yyyy/mm/dd hh:ii'});

})(jQuery);

function add_form_event(callback){
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
        var table = $(table_id).DataTable();

        $(".form_datetime").datetimepicker({format: 'yyyy/mm/dd hh:ii'});

        table.on( 'draw', function () {
            $('.table-edit-btn').click(function(e){
                e.preventDefault();
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

            $('.table-remove-btn').click(function(e){
                e.preventDefault();
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
            var submit_btn = $(this).find('button[type="submit"]');
            submit_btn.prop( "disabled", true );
            $(this).find('.error-box').hide();
            if(!$(this).checkFormInputs(this)){
                return;
            }
            var data = $(this).serializeFormJSON();
            var label = $(this).attr('label');
            $.post($(this).attr('action'), data, function(res){
                submit_btn.prop( "disabled", false );
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


function load_group_select(){
    $.get("/group/get_group_list", {}, function(group_list){
        $.each(group_list, function(i, item){
            $('#group-select').append("<option value=\""+ item["value"] + "\">" + item["text"] + "</option>");
        });
        $('#group-select').multiselect({
            enableFiltering: true,
            includeSelectAllOption: true,
            selectAllText: '全选',
            buttonWidth: '300px',
            disableIfEmpty: true,
            disabledText: '暂无',
            onDropdownHide: function(event) {
                load_volunteer_select($('#group-select').val());
            }
        });
    });
}

function load_volunteer_select(group_list){
    var exist_group_list = [];
    $('#volunteer-select option').each(function(){
        if($.inArray($(this).attr('group'), exist_group_list) < 0){
            exist_group_list.push($(this).attr('group'));
        }
    });
    var remove_group_list = $.map(exist_group_list, function(elem){
        return $.inArray(elem, group_list) < 0 ? elem : null;
    });

    group_list = $.map(group_list, function(elem){
         return $.inArray(elem, exist_group_list) < 0 ? elem : null;
     });
    if(group_list.length > 0){
        $.post("/volunteer/get_volunteer_list", {
            "group_list": group_list.join(","),
            "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
            }, function(res){
                $.each(res, function(group, v_list){
                    $.each(v_list, function(i, item){
                        $('#volunteer-select').append("<option group=\""+ group +"\" value=\""+ item["value"] + "\">" + item["text"] + "</option>");
                    });
                });
                $.each(remove_group_list, function(i, group){
                    $('option[group="'+group+'"]', $('#volunteer-select')).remove();
                });
                $('#volunteer-select').multiselect('rebuild');
        });
    }
    else{
        $.each(remove_group_list, function(i, group){
            $('option[group="'+group+'"]', $('#volunteer-select')).remove();
        });
        $('#volunteer-select').multiselect('rebuild');
    }

}
