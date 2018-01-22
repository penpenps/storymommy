$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_admin_list();

    $('#add-admin-form').submit(function (e) {
        e.preventDefault();
        $('#add-admin-error-box').hide();
        if(!$(this).checkFormInputs(this)){
            return;
        }
        var data = $(this).serializeFormJSON();
//        console.log(data);
        $.post('/backend/create_admin', data, function(res){
            if(res['code'] == 0){
                $('#admin-modal').modal('hide');
                load_admin_list();
            }
            else{
                $('#add-admin-error-box').show();
                $('#add-admin-error-msg').text(res['msg']);
                return;
            }
        });

    });


});

function load_admin_list(){
    load_table_content('/backend/load_admin_list', '#table-panel', "#adminTable");
}

