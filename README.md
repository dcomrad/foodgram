# Проект Foodgram (Продуктовый помощник)
```Дипломный проект по специальности "Python-разработчик" на обучающей платформе Яндекс.Практикум```

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Стек технологий
- Django
- Django Rest Framework
- REST API
- Djoser

# Примеры API запросов:
- [POST] /api/users/ - _Зарегистрировать нового пользователя_
- [GET] /api/users/1/ - _Получить информацию о пользователе с id=1_
- [POST] /api/auth/token/login/ - _Получить Authtoken для входа в личный кабинет_
- [GET] /api/ingredients/?name=молоко - _Получить список ингредиентов с поиском по имени_
- [GET] /api/recipes/?page=1&limit=3&is_favorited=1 - _Получить все рецепты, добавленные в избранное. Разбить выдачу по 3 рецепта на странице, отобразить страницу 1_
- [GET] /api/recipes/?author=1&tags=dinner&tags=lunch - _Получить все рецепты, которые созданы пользователем с id=1, и помеченные один из тегов: dinner, lunch_
- [DELETE] /api/users/{id}/subscribe/ - _Отписаться от пользователя с заданным id_
- [POST] /api/recipes/{id}/shopping_cart/ - _Добавить рецепт с заданным id в корзину_


# Пользовательский функционал

### Что могут делать неавторизованные пользователи
- Создать аккаунт
- Просматривать рецепты на главной
- Просматривать отдельные страницы рецептов
- Просматривать страницы пользователей
- Фильтровать рецепты по тегам
- 
### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем
- Выходить из системы (разлогиниваться)
- Менять свой пароль
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной
- Просматривать страницы пользователей
- Просматривать отдельные страницы рецептов
- Фильтровать рецепты по тегам
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок

### Что может делать администратор
- Администратор обладает всеми правами авторизованного пользователя
- Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.


_Для наполнения БД предустановленными ингредиентами и тегами, выполните команды:_
```
python3 manage.py load_ingredients
python3 manage.py load_tags
```
 
# Авторы
Александр Бондаренко