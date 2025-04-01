$(document).ready(function () {

    //Обрабатываем нажатие ссылки на удаление заказа
    $(document).on("click", "#order_delete", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем ссылку на контроллер django из атрибута data-order-delete-url
        var url = $(this).data("order-delete-url");

        // Берем id заказа из атрибута data-order-delete-id
        var orderID = $(this).data("order-delete-id");

        Swal.fire({
            title: "Вы уверенны?",
            text: "Удалить существующий заказ!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Да, удалить!"
          }).then(function (result) {
            if (result.value) {
                $.ajax({
                    url: url, // Отправка запроса на указанный URL
                    type: "POST",
                    data: {
                        order_id: orderID, // Передаём ID заказа
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() // CSRF-токен
                    },
                    success: function(response) {
                        setTimeout(function () {
                            location.reload(); // Перезагрузка текущей страницы
                        }, 1000); // Задержка в 1 секунду (1000 миллисекунд)
                    },
                    error: function(xhr) {
                        alert("Ошибка: " + (xhr.responseJSON ? xhr.responseJSON.error : "Не удалось удалить заказ"));
                    }
                });  
              Swal.fire("Удалено!", "Заказ успешно удален.", "success");
            }
        });
    });
});