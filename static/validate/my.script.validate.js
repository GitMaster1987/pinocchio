// Добавление пользовательского валидатора для номера телефона
$.validator.addMethod("phoneFormat", function(value, element) {
    return this.optional(element) || /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(value);
}, "Пожалуйста, введите номер телефона в формате +7 (***) ***-**-**");

// Добавление пользовательского валидатора для проверки сложности пароля
$.validator.addMethod("strongPassword", function(value, element) {
    return this.optional(element) || /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(value);
}, "Пароль должен содержать минимум 8 символов, одну заглавную букву, одну строчную букву, одну цифру и один специальный символ.");

$(document).ready(function () {
    $("#registrationForm").validate({
        rules: {
            username: {
                required: true,
                maxlength: 35
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
                email: true
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
                maxlength: "Логин не может превышать 35 символов"
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
                email: "Пожалуйста, введите правильный email адрес"
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

