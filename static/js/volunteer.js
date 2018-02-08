$(document).ready(function(){
//    $("#dataTable").DataTable();

    load_volunteer_list();

    add_form_event(load_volunteer_list);
    $('#qrcode-btn').click(function(e){
        e.preventDefault();
        $.get("/volunteer/get_qrcode/", {
            "type": "register"
        }, function(res){
            $('#qrcode-modal').modal();
            $('#qrcode-error').hide();

            if(res.code == 1){
                $('#qrcode-img').show();
                $('#qrcode-error').html(res.msg);
                return;
            }
            $('#qrcode-img').html(res.documentElement);

        });
    });

});

function load_volunteer_list(){
    load_table_content('/volunteer/load_volunteer_list', '#table-panel', "#groupTable");
}


