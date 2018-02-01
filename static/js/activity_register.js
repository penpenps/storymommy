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

    $('#activity-register-form').submit(function (e) {
        e.preventDefault();
        var data = {
            "activity_id": $('#table-panel').attr('activity_id'),
            "volun_list": $('#volunteer-select').val().join(","),
            "type": $("input[type=radio][name=register-type]:checked").val(),
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

