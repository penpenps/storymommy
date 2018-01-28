$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_volunteer_list();

    add_form_event(load_volunteer_list);


});

function load_volunteer_list(){
    load_table_content('/volunteer/load_volunteer_list', '#table-panel', "#groupTable");
}

