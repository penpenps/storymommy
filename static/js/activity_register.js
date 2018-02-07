$(document).ready(function(){
//    $("#dataTable").DataTable();
    load_group_select();
    $('#volunteer-select').multiselect({
            enableFiltering: true,
            includeSelectAllOption: true,
            selectAllText: '全选',
            buttonWidth: '300px',
            disableIfEmpty: true,
            disabledText: '暂无'
       });
    load_activity_register_list();

    $("input[type=radio][name=register-type]").change(function(){
        var val = $("input[type=radio][name=register-type]:checked").val();
        if(val == "single"){
            $('#training-list-group').hide();
        }
        else{
            $('#training-list-group').show();
        }
    });

    $('#activity-register-form').submit(function (e) {
        e.preventDefault();
        var data = {
            "activity_id": $('#table-panel').attr('activity_id'),
            "volun_list": $('#volunteer-select').val().join(","),
            "type": $("input[type=radio][name=register-type]:checked").val(),
            "ta_id": $('#training-select').val(),
            "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
        };
        $.post($(this).attr("action"), data, function(res){
            $("#activity-register-modal").modal('hide');
            $("#activity-register-result-modal").modal();
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

function load_activity_register_list(){
    var activityId = $('#table-panel').attr('activity_id');
    load_table_content('/activity/load_register_list/'+activityId, '#table-panel', "#activityRegisterTable");
}



