$(document).ready(function() {

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
    });

    $("#input-products").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/getProducts",
                data: {
                    query : $("#input-products").val()
                },
                success: function (data) {

                    $("#products").html(data);
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {
        }
    });
    
    $("#change-product").click(function () {
        var productId = $("div#products input[name='products']:checked").val();
        $("#modalEditOrder").modal('hide');
        console.log(productId);
    })

});

function showModalRemoveOrder(id, name) {
    $("#order_name").html(name);
    $("#order_line_id").val(id);
    $("#modalRemoveOrder").modal('show');
}

function acceptDelete(){

    odoo.define('custom_sales.AcceptDelete', function(require) {
        'use strict';
        var ajax = require('web.ajax');
        var olId = $("#order_line_id").val();
        ajax.jsonRpc("/addOLtoRM", 'call', {'olId':olId}).then(function(data) {
            $("#modalRemoveOrder").modal('hide');
            $("#order-"+olId).hide('slow')
            var total = parseFloat($("span[data-id='total_amount'] .oe_currency_value").html().replace(',', ''));
            var amount = parseFloat($("tr#order-" + olId +" span[data-oe-field='price_subtotal'] > span.oe_currency_value").html().replace(',', ''));
            $("span[data-id='total_amount'] .oe_currency_value").html(total - amount);
        }, function () {
            // an error occured during during call
        });
    });

}

function loadProducts(){

    odoo.define('custom_sales.LoadProduct', function(require) {
        'use strict';
        var ajax = require('web.ajax');
        var query = $("#input-products").val();
        ajax.jsonRpc("/getProducts", 'call', {'query': query}).then(function(data) {
            $("#products").html(data);
        }, function () {
            // an error occured during during call
        });
    });

}

