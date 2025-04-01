/** === DATA TABLE === */
$(document).ready(function() {
    $('#views-products-datatable').DataTable({
        "lengthMenu": [[10, 20, 30, 40, -1], [10, 20, 30, 40, "All"]],
       
        "columnDefs": [{
            "targets": [1, 2, ], // The columns to disable sorting (0-index based)
            "orderable": false
        }],
        "columns": [
            { "width": "15%" },
            { "width": "15%" },
            { "width": "20%" },
            { "width": "15%" },
            { "width": "15%" },
            { "width": "8%" },
            { "width": "12%" },               
        ],
        language: {
            "zeroRecords":    "Не найдено подходящих записей!",
            "search":         "Поиск:",
            "infoPostFix":    "",
            "info":      "",
            lengthMenu: '_MENU_ Количество записей',
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Следующая",
                "previous": "Предыдущая"
            },
        },
        "order": [[5, 'asc'], [3, 'asc']],
        // buttons: [ 'copy', 'excel', 'pdf', 'print'],
    });
  });

  $(document).ready(function () {

    //Обрабатываем нажатие ссылки на удаление заказа
    $(document).on("click", "#add_stop_list", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        const productId = $(this).data("stop-list-id");
        const url = $(this).data("stop-list-url");
        Swal.fire({
            title: "Вы уверенны?",
            text: "Перенести блюдо в стоп-лист!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Да, перенести!"
          }).then(function (result) {
            if (result.value) {
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {
                        product_id: productId,
                        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function (response) {
                        if (response.message) {
                            
                            setTimeout(function () {
                                location.reload(); // Перезагрузка текущей страницы
                            }, 1000); // Задержка в 1 секунду (1000 миллисекунд)
                        }
                    },
                    error: function (xhr) {
                        if (xhr.responseJSON && xhr.responseJSON.error) {
                            alert(`Ошибка: ${xhr.responseJSON.error}`); // Error from server
                        } else {
                            alert("Произошла ошибка. Попробуйте снова."); // General error
                        }
                    },
                });
                Swal.fire("Успешно!", "Блюдо перенесено в стоп-лист.", "success");  
            }
        });
        
    });
});