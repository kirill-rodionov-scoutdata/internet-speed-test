# internet-speed-test

Тестовое задание для Ad Robot. 
Замеряет скорость интернета: делает 10 последовательных HTTP-запросов к указанному адресу (по умолчанию — изображение [image.jpg](image.jpg) из этого репозитория), дожидаясь каждого ответа, и печатает время и скорость каждого запроса, а также среднюю скорость по всем 10.

## Требования

- Python 3.10+
- Для запуска самого скрипта зависимости не нужны (только стандартная библиотека)
- `pytest` нужен только для тестов

## Запуск

```bash
python3 speedtest.py
```

Без аргументов уже всё по дефолту: встроенный URL (картинка [image.jpg](image.jpg) из этого репозитория) и 10 запросов. Параметры нужны только если хочешь что-то поменять — свой адрес и/или количество запросов:

```bash
python3 speedtest.py https://upload.wikimedia.org/wikipedia/commons/0/00/Crab_Nebula.jpg -n 5
```

## Пример вывода

```
request 1/10: 0.26s, 13.84 MB, 53.46 MB/s
request 2/10: 0.21s, 13.84 MB, 65.20 MB/s
request 3/10: 0.20s, 13.84 MB, 70.26 MB/s
request 4/10: 0.14s, 13.84 MB, 95.54 MB/s
request 5/10: 0.15s, 13.84 MB, 94.07 MB/s
request 6/10: 0.15s, 13.84 MB, 94.73 MB/s
request 7/10: 0.15s, 13.84 MB, 89.89 MB/s
request 8/10: 0.16s, 13.84 MB, 83.97 MB/s
request 9/10: 0.17s, 13.84 MB, 81.56 MB/s
request 10/10: 0.14s, 13.84 MB, 98.88 MB/s
summary: 10/10 succeeded
avg time: 0.17s
total downloaded: 138.37 MB
avg speed: 79.78 MB/s
```

## Тесты

```bash
pip install pytest
pytest tests.py
```
