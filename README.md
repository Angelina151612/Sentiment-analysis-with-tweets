# Приложение для анализа твитов пользователя

**Цель**: создать приложение для анализа твитов заданного пользователя. Приложение должно предоставлять некоторую статистику постов пользователя за 2020-й год.

**Данные для обучения:** [kaggle](https://www.kaggle.com/kazanova/sentiment140) 

**Данный для анализа в готовом приложении:** [twitter](https://twitter.com/) 

**Этапы разработки**: 
1. Обработка исходных данных
2. Создание словаря для обучения нейронной сети
3. Построение и обучение нейронной сети
4. Создание веб-приложения 

## Обработка данных и создание словаря
Для обработки тектовых данных использовались следующие технологии:
* Pandas - библиотека для анализа данных. Использовалась для работы с твитами (загрузка, сохрание).
* NLTK - пакет библиотек и программ для обработки естественного языка.

На данном этапе тестовые данные были очищены от шума (пунктуация, ссылки, местоимения и др.) и сохранены в файл .сsv. Далее на основе этих данных был создан словарь для обучения нейронной сети. Ключом занного словаря является слово, значением - порядковый номер в словаре. Значения были отсортированы от самых часто встречающихся до самых редких. 

## Построение и обучение нейронной сети
Технологии, которые использовались для построения нейронной сети:
* TensorFlow  - библиотека для машинного обучения, разработанная Google.
* Numpy - библиотека для работы с массивами. Использовалась для работы с метками.
* Seaborn - библиотека для визуализации данных. Использовалась для построения графиков обучения нейронной сети.

В результате была построены рекуррентная нейронная сеть для определения настроения твитов пользователя. Для обучения использовались следующие параметры:

- Функция активации на последнем слое: сигмоида(sigmoid). Является стандартной функцией активации на последнем слое в задачах бинарной классификации.

- Функция потерь: бинарная перекрёстная энтропия (binary crossentropy). Является стандарной функцией потерь в задачах бинарной классификации.

- Оптимизатор: Адам (Adam) - один из самых новых и популярных оптимизаторов.

- Метрика качества обучения: точность (accuracy). Подходит для задач классификации.


Графки обучения представлены ниже.

|График точности | График ошибки|
|:-------------------------: | :-------------------------:|
|![acc](https://github.com/Angelina151612/Sentiment-analysis-with-tweets/blob/master/img/acc.png)| ![loss](https://github.com/Angelina151612/Sentiment-analysis-with-tweets/blob/master/img/loss.png)|

Обученная нейронная сеть классифицирует данные с точностью 0.91 на обучеющем наборе и  0.89 на тестовом.

## Создание веб-приложения
В ходе работы использовались следующие технологии:
* Django - веб-фреймворк.
* Sqlite - CУБД, использовалась для хранения пользователей, для которых уже есть построенные графики. 
* Celery - асинхронная очередь задач.
* Redis - СУБД, использвалась в качестве брокера задач.
* Pandas - данная библиотека исользовалась для отрисовки графиков.
* Twint - инструмент для загрузки твитов без официального API. 

В ходе работы было создано приложение для анализа твитов пользователя. Скриншоты представлены ниже.

Домашняя страница:
![Home](https://github.com/Angelina151612/Sentiment-analysis-with-tweets/blob/master/img/home)

Страница пользователя со статистикой:
![user](https://github.com/Angelina151612/Sentiment-analysis-with-tweets/blob/master/img/user)

Страница с профилями, которые уже есть в баззе данных.
![profiles](https://github.com/Angelina151612/Sentiment-analysis-with-tweets/blob/master/img/profiles)

Страница с ошибкой при вводе несуществующего имени пользователя.
![Error](https://github.com/Angelina151612/Sentiment-analysis-with-tweets/blob/master/img/error)


## Трудности
В ходе работы возникли следующие трудности:

* Загрузка данных из twitter.

Т.к. twitter не представляет API в открытом доступе, возникли трудности с получнием данных пользователя. Для решения данной проблемы изпользовался twint. Данный инструмент позволяет загрузить как все твиты пользователя, так и за определенный период.


* Обаботка слов с ошибками.

Т.к. твиты представляют собой естественный язык, то в них содержатся ошибки и опечатки. Основной идеей было воспользоваться функцией для исправления правописания, однако осуществить данную задумку не удалось, т.к. вычислительной мощности компьютера не хватило на обработку всего датасета (900 000 твитов, каждый из которых состоит их нескольких десятков слов). 


* Ожидание во время обрботки данных пользователя.

Обработка данных пользователя требует некоторого времни. Т.к. django синхронный веб-фреймворк, то он способен выполнять только одну задачу, поэтому попытка обновить страницу во время ожидания или сделать какие-либо другие действия на странцие приводила к тому, что приложение падало. Данная проблема была решена с помощью Celery. При вводе нового пользователя, все задачи по обработке твитов (очистка текста, получение предсказаний от сети, создание графиков) передаются для выполнения Сelery. Благодаря этому приложение все еще доступно пользователю, даже если процесс обработки долгий.

## Ссылка на проект

https://github.com/Angelina151612/Sentiment-analysis-with-tweets
