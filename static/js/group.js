$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_group_list();

    add_form_event(load_group_list);


});

function load_group_list(){
    load_table_content('/group/load_group_list', '#table-panel', "#groupTable");
}

