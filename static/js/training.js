$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_training_list();

    bind_submit_event('#training-add-form');
});

function add_at_select(form){
    var new_item = $(form.find('.list-group-template').html());
    var ta_list_group = form.find('.ta-list-group');
    var idx = ta_list_group.children('li').length;
    new_item.find('input[name=ta_order]').attr('id', 'ta_order_'+idx);
    new_item.find('input[name=ta_order]').val(idx);
    new_item.find('select[name=ta_type]').attr('id', 'ta_type_'+idx);
    ta_list_group.append(new_item);
    new_item.find('.ta-delete-btn').click(function(){
        form.find('.error-box').hide();
        if(form.find('.ta-list-group .list-group-item').length <= 1){
            form.find('.error-box').show();
            form.find('.error-msg').html("至少需要指定一个活动类型");
            return;
        }
        $(this).closest('.list-group-item').remove();
    });

    return new_item;
}

function bind_submit_event(id){
    $(id).find(".training-add-type-btn").click(function(e){
        e.preventDefault();
        var form = $(this).closest('form');
        add_at_select(form);
    });

    $(id).find('.ta-delete-btn').click(function(e){
        e.preventDefault();
        var form = $(this).closest('form');
        form.find('.error-box').hide();
        if(form.find('.ta-list-group .list-group-item').length <= 1){
            form.find('.error-box').show();
            form.find('.error-msg').html("至少需要指定一个活动类型");
            return;
        }
        $(this).closest('.list-group-item').remove();
    });
    $(id).submit(function(e){
        e.preventDefault();
        var label = $(this).attr('label');
        $(this).find('.error-box').hide();
        if(!$(this).checkFormInputs(this)){
            return;
        }
        var order_list = [];
        var ta_list = [];
        var ta_ids = [];
        var empty_id = 0;
        $(this).find('.ta-list-group .list-group-item').each(function(){
            order_list.push($(this).find('input[name=ta_order]').val());
            ta_list.push($(this).find('select[name=ta_type]').val());

            ta_ids.push($(this).attr("ta_id") ? $(this).attr("ta_id"): "_"+empty_id++);

        });
        var data = {
            "training_id": $(this).attr("training_id"),
            "name": $(this).find('input[name=name]').val(),
            "group_id": $(this).find('select[name=group_id]').val(),
            "is_private": $(this).find('select[name=is_private]').val(),
            "order_list": order_list.join(","),
            "ta_list": ta_list.join(","),
            "ta_ids": ta_ids.join(","),
            "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
        };

        $.post($(this).attr("action"), data, function(res){
            if(res.code == 0){
                location.reload();
            }
            else{
                $('#training-'+label+'-modal').find('.error-box').show();
                $('#training-'+label+'-modal').find('.error-msg').html(res.msg);
            }
        });
    });
}

function load_training_list(){
    $.get("/training/load_training_list", {}, function(tableHtml){
        $("#table-panel").html(tableHtml);
        $("#training-table").DataTable();
        bind_submit_event('#training-edit-form');

        $('.table-edit-btn').click(function(e){
            e.preventDefault();
            var row_item = {};
            $(this).closest('tr').find('td').each(function(){
                var attr = $(this).attr('label');
                if(typeof attr !== typeof undefined && attr !== false){
                    if(attr=="at_list"){
                        row_item[attr] = {};
                        $(this).find("ul li").each(function(){
                            var temp = {
                                "at_id": $(this).attr("at_id"),
                                "order": $(this).attr("order")
                            };
                            row_item[attr][$(this).attr("value")] = temp;
                        });
                    }
                    else{
                        row_item[attr] = $(this).attr('value');
                    }
                }
            });
            var form = $('#training-edit-form');
            form.attr("training_id", $(this).closest('tr').attr("training_id"));
            form.find('input[name=name]').val(row_item["name"]);
            form.find('select[name=group_id]').val(row_item["group_id"]);
            form.find('select[name=is_private]').val(row_item["is_private"]);
            form.find('.ta-list-group .list-group-item').each(function(){
                $(this).remove();
            });
            $.each(row_item["at_list"], function(id, item){
                new_select = add_at_select(form);
                new_select.find('input[name=ta_order]').val(item["order"]);
                new_select.find('select[name=ta_type]').val(item["at_id"]);
                new_select.attr("ta_id", id);
            });

            $('#training-edit-modal').modal();
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
    });
}

