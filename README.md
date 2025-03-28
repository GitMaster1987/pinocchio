# pinocchio
##### Миграции:
Создание миграции:
-- python manage.py makemigrations <br>
Применение миграции:
-- python manage.py migrate

##### Фикстуры:
Создание фикстуры:
-- python -Xutf8 manage.py dumpdata
Применение фикстуры:
-- python -Xutf8 manage.py loaddata fixtures/main/

##### Новое приложение:
-- python manage.py startapp