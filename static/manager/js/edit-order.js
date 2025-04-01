$(document).ready(function () {

    /** === Изменяем кол-во товаров в заказе === */
    // Ловим событие клика по кнопке decrement
    $(document).on("click", ".decrement", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("order-change-url");

        // Берем id заказа из атрибута data-order-id
        var orderID = $(this).data("order-id");

        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.align-items-center').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        if (currentValue > 1) {
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateOrder(orderID, currentValue - 1, -1, url);
        }
    });

    // Ловим событие клика по кнопке increment
    $(document).on("click", ".increment", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("order-change-url");

        // Берем id заказа из атрибута data-order-id
        var orderID = $(this).data("order-id");

        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.align-items-center').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        if (currentValue > 0) {
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateOrder(orderID, currentValue + 1, 1, url);
        }
    });

    function updateOrder(orderID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                order_id: orderID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                location.reload();               
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }


    // Удаление товара из ордера-заказа пользователя
    $('.remove_order_cart').click(function () {
        // Берем ссылку на контроллер django из атрибута data-remove-change-url
        var url = $(this).data("remove-change-url");
        // Берем id заказа из атрибута data-order-id
        var orderID = $(this).data("remove-id");

        Swal.fire({
            title: 'Вы уверенны?',
            text: "Удалить данный товар!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Да, удалить!',
            cancelButtonText: 'Нет, я передумал!',
            confirmButtonClass: 'btn btn-success mt-2',
            cancelButtonClass: 'btn btn-danger ml-2 mt-2',
            buttonsStyling: false
        }).then(function (result) {
            if (result.value) {                
                
                $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        order_id: orderID,
                        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                    },
                    success: function (data) {
                        location.reload();               
                    },
                    error: function (data) {
                        console.log("Ошибка при удалении товара");
                    },
                });                
                Swal.fire({                
                title: 'Удалено!',
                text: 'Товар был успешно удален.',
                type: 'success'
                })
            } else if (
                // Read more about handling dismissals
                result.dismiss === Swal.DismissReason.cancel
            ) {
                Swal.fire({
                title: 'Отмена удаления',
                text: 'Товар не был удален',
                type: 'error'
                })
            }
        });
    });
      
});

