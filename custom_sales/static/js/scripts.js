
$(document).ready(function() {

    function showModalRemoveOrder(id, name) {
        $("#order_name").html(name);
        $("#order_line_id").val(id);
        $("#modalRemoveOrder").modal();
    }

    $("#accept-delete").click(function () {
        var olId = $("#order_line_id").val();
        $.post('/addOLtoRM/',
            {'olId':olId,'csrf_token':$("input[name=csrf_token]").val()},
            function(data){
                $("#order-"+olId).hide('slow');
            }
        )
    })

    $("#save-changes").click(function () {
        $.post('/acepted-edit/',
            {'csrf_token':$("input[name=csrf_token]").val()},
            function(data){
                if (data.success){
                    $(location).attr('href', $("#no-changes").attr('href'))
                } else {
                    /*
                    * Show an error message
                    * */
                }
            }, 'json'
        )
    })

});
