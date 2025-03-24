// Добавление пользовательского валидатора для номера телефона
$.validator.addMethod("phoneFormat", function(value, element) {
    return this.optional(element) || /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(value);
}, "Пожалуйста, введите номер телефона в формате +7 (***) ***-**-**");

// Добавление пользовательского валидатора для проверки сложности пароля
$.validator.addMethod("strongPassword", function(value, element) {
    return this.optional(element) || /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(value);
}, "Пароль должен содержать минимум 8 символов, одну заглавную букву, одну строчную букву, одну цифру и один специальный символ.");

// Метод для проверки уникальности поля USERNAME
$.validator.addMethod("usernameUnique", function(value, element) {
    let isUnique = false;
    $.ajax({
        url: "/user/check_username/", // URL для проверки на сервере
        type: "POST",
        async: false, // Синхронный запрос для корректной работы валидации
        data: {
            username: value,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function(response) {
            isUnique = response.is_unique; // Сервер возвращает true, если username уникален
        },
        error: function() {
            isUnique = false; // В случае ошибки считаем, что username не уникален
        }
    });
    return isUnique;
}, "Этот логин уже зарегистрирован. Пожалуйста, выберите другой.");

// Метод для проверки уникальности Email адреса
$.validator.addMethod("emailUnique", function(value, element) {
    let isUnique = false;
    $.ajax({
        url: "/user/check_email/", // URL для проверки на сервере
        type: "POST",
        async: false, // Синхронный запрос (нужно для валидации)
        data: {
            email: value,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function(response) {
            isUnique = response.is_unique; // Сервер вернёт, уникален ли email
        },
        error: function() {
            isUnique = false; // В случае ошибки считаем, что email не уникален
        }
    });
    return isUnique;
}, "Этот email уже зарегистрирован. Пожалуйста, выберите другой.");


$(document).ready(function () {
    $("#registrationForm").validate({
        rules: {
            username: {
                required: true,
                maxlength: 35,
                usernameUnique: true // Использование нового пользовательского валидатора
            },
            first_name: {
                required: true,
                maxlength: 35
            },
            last_name: {
                required: true,
                maxlength: 35
            },
            email: {
                required: true,
                email: true,
                emailUnique: true // Использование пользовательского валидатора
            },
            phone_number: {
                required: true,
                phoneFormat: true // Использование пользовательского валидатора
            },
            password1: {
                required: true,
                minlength: 8,
                strongPassword: true // Использование пользовательского валидатора сложности пароля
            },
            password2: {
                required: true,
                minlength: 8,
                equalTo: "#id_password1"
            }
        },
        messages: {
            username: {
                required: "Пожалуйста, введите логин",
                maxlength: "Логин не может превышать 35 символов",
                usernameUnique: "Этот логин уже зарегистрирован. Пожалуйста, выберите другой"
            },
            first_name: {
                required: "Пожалуйста, введите Имя",
                maxlength: "Поле не может превышать 35 символов"
            },
            last_name: {
                required: "Пожалуйста, введите Фамилию",
                maxlength: "Поле не может превышать 35 символов"
            },
            email: {
                required: "Пожалуйста, введите email",
                email: "Пожалуйста, введите правильный email адрес",
                emailUnique: "Этот email уже зарегистрирован. Пожалуйста, выберите другой"
            },
            phone_number: {
                required: "Пожалуйста, введите номер телефона",
                phoneFormat: "Пожалуйста, введите номер телефона в формате +7 (***) ***-**-**"
            },
            password1: {
                required: "Пожалуйста, введите пароль",
                minlength: "Пароль должен содержать минимум 8 символов"
            },
            password2: {
                required: "Пожалуйста, введите подтверждение пароля",
                minlength: "Пароль должен содержать минимум 8 символов",
                equalTo: "Пароли не совпадают"
            }
        },
        errorClass: "error",
        errorElement: "div"
    });
});

