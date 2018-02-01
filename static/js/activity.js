$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_activity_list();

    add_form_event(load_activity_list);


});

function load_activity_list(){
    load_table_content('/activity/load_activity_list', '#table-panel', "#activityTable");
}

