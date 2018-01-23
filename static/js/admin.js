$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_admin_list();

    add_form_event(load_admin_list);


});

function load_admin_list(){
    load_table_content('/backend/load_admin_list', '#table-panel', "#adminTable");
}

