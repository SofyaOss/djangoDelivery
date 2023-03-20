$(document).ready(function() {
    var form = $('#buy-product');
    function basketUpdating(product_id, num, form_id, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.num = num;
        data.is_delete = is_delete;
        var csrf_token = $(form_id + ' [name="csrfmiddlewaretoken"]').val();
        console.log(csrf_token);
        data["csrfmiddlewaretoken"] = csrf_token; 
        var url = '/delivery/basket_adding/';
        console.log(form_id, url);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                console.log('ok');
                console.log(data.products_total_num);
                if (data.products_total_num || data.products_total_num == 0) {
                    $('#basket_total_num').text('(' + data.products_total_num + ')');
                }
            },
            error: function() {
                console.log('error');
            }
        });
    };
    form.on('submit', function(e) {
        e.preventDefault();
        var num = $('#number').val();
        var submit_btn = $('#submit-btn');
        var product_id = submit_btn.data('product_id');
        
        basketUpdating(product_id, num, '#buy-product', is_delete=false);
    });

    $(document).on('click', '.detail-submit', function(e) {
        e.preventDefault();
        var product_id = $(this).data('product_id');
        var num = $(this).data('num');
        basketUpdating(product_id, num, '#detail-form', is_delete=false);
    });

    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault();
        product_id = $(this).data('product_id');
        num = 0;
        basket_form = $('#delete-form');
        console.log(111, basket_form);
        var url = basket_form.attr('action');
        console.log(222, url);
        basketUpdating(product_id, num, '#delete-form', is_delete=true);
    });

    function calcBasketAmount() {
        var total_order_amount = 0;
        $('.total_prod_amount').each(function() {
            total_order_amount += parseInt($(this).text());
        });
        $('#total_order_amount').text(total_order_amount + ' руб.');
    };
    calcBasketAmount();
})