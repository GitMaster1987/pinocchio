$(document).ready(function () {
    // Перехват события отправки формы
    $("form").on("submit", function (event) {
        // Получаем значение поля даты
        const dateValue = $("#dateOrder").val();
        const selectedDate = new Date(dateValue); // Преобразуем значение в объект Date
        const currentDate = new Date(); // Получаем текущую дату и время
        
        // Проверяем, заполнено ли поле
        if (!dateValue) {
            Swal.fire({
                type: 'error',
                title: 'Ошибка...',
                text: 'Пожалуйста, укажите дату выполнения заказа!',
                confirmButtonClass: 'btn btn-confirm mt-2',
            })
            event.preventDefault(); // Останавливаем отправку формы
            return;
        }

        // Дополнительная проверка формата, если требуется
        // Например: yyyy-MM-ddTHH:mm
        const dateRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
        if (!dateRegex.test(dateValue)) {
            Swal.fire({
                type: 'error',
                title: 'Ошибка...',
                text: 'Неверный формат даты. Пожалуйста, укажите корректную дату!',
                confirmButtonClass: 'btn btn-confirm mt-2',
            })
            event.preventDefault(); // Останавливаем отправку формы
            return;
        }

        // Проверка, чтобы выбранная дата не была раньше текущей
        if (selectedDate < currentDate) {
            Swal.fire({
                type: 'error',
                title: 'Ошибка...',
                text: 'Дата выполнения заказа не может быть раньше текущего времени!',
                confirmButtonClass: 'btn btn-confirm mt-2',
            })
            event.preventDefault(); // Останавливаем отправку формы
            return;
        }

        // Проверка на попадание в рабочий график (с 9:00 до 19:00)
        const selectedHour = selectedDate.getHours();
        if (selectedHour < 9 || selectedHour > 19) {
            Swal.fire({
                type: 'error',
                title: 'Ошибка...',
                text: 'Время выполнения заказа должно быть в рабочем графике предприятия: с 9:00 до 19:00!',
                confirmButtonClass: 'btn btn-confirm mt-2',
            })
            event.preventDefault();
            return;
        }
        // Если всё корректно, форма отправляется
    });
});
