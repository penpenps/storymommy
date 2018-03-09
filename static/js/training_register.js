$(document).ready(function(){
//    $("#dataTable").DataTable();
    load_group_select();
    $('#volunteer-select').multiselect({
            maxHeight: 600,
            enableFiltering: true,
            includeSelectAllOption: true,
            selectAllText: '全选',
            buttonWidth: '300px',
            disableIfEmpty: true,
            disabledText: '暂无'
       });
    $('.table-remove-btn').click(function(){
        var row_item = {};
        var param = $(this).attr('param');
        $(this).closest('tr').find('td').each(function(){
            var attr = $(this).attr('label');
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

    $('#training-register-form').submit(function (e) {
        e.preventDefault();
        var submit_btn = $(this).find('button[type="submit"]');
        submit_btn.prop( "disabled", true );
        var data = {
            "training_id": $('#table-panel').attr('training_id'),
            "volun_list": $('#volunteer-select').val().join(","),
            "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
        };
        $.post($(this).attr("action"), data, function(res){
            submit_btn.prop( "disabled", false );
            $("#training-register-modal").modal('hide');
            $("#training-register-result-modal").modal();
            if(res["success"] > 0){
                $("#success-info").show();
                $("#success-info").html("成功注册"+res["success"]+"人。");
            }
            else{
                $("#success-info").hide();
            }
            if(res["failed"] > 0){
                $("#error-info").show();
                $("#error-info").html(res["failed"]+"人注册失败, 原因如下: <br/>");
                $.each(res["msg"], function(v_id, msg){
                    $("#error-info").append($('#volunteer-select option[value='+v_id+']').text()+":"+msg+"<br/>");
                });
            }
            else{
                $("#error-info").hide();
            }
        });
    });

});



