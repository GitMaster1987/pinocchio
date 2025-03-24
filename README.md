# pinocchio
##### Миграции:
Создание мыграции:
-- python manage.py makemigrations
Применение миграции:
-- python manage.py migrate

##### Фикстуры:
Создание фикстуры:
-- python -Xutf8 manage.py dumpdata
Применение фикстуры:
-- python -Xutf8 manage.py loaddata fixtures/main/

##### Новое приложение:
-- python manage.py startapp