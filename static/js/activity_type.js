$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_activity_type_list();

    add_form_event(load_activity_type_list);


});

function load_activity_type_list(){
    load_table_content('/activity_type/load_activity_type_list', '#table-panel', "#activityTypeTable");
}

