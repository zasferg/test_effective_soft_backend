Данный проект был выполнен в рамках тестового задания.<br>
Для его запуска вам понадобится установленный docker, python3.11, pip <br>

Запуск приложения:
1. При помощи git clone склонируйте себе это репозиторий.<br>
2. На своем компьютере перейдите в папку app/ данного  репозитория.<br>
3. При помощи комманды в терминале docker compose up --build запустите контейнер.<br>

Автоматически установится база данных, приложение, установятся миграции, запустится приложение.<br>
Что бы создать суперпольтзователя нужно для начала в терминале ввести комманду docker exec -it app-api-1 /bin/sh .<br>
Далее при помощи python manage.py createsuperuser создаете суперпользователя.

Для запуска тестов так же при помощи комманды в терминале docker exec -it app-api-1 /bin/sh <br>
входим в контейнер. Далее при посощи комманды cd tests/orders переходим в папку с тестами. <br>
Для запуска тестов ввести pytest .

Если у вас етсь docker desktop , выполнять docker exec -it app-api-1 /bin/sh не нужно.<br>
Просто перейдите в контейнер с приложением и кликните на вкладку exec. Вам откроется терминал<br>
контейнера.



