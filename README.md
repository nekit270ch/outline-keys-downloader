# Outline Keys Downloader
Скрипт для скачивания ключей Outline с сайта https://outlinekeys.com

## Запуск
Для работы скрипта необходим Python версии 3.10 и выше.

### Windows
```
python download_keys.py
```
### Linux/macOS
```
python3 download_keys.py
```

## Аргументы командной строки
```
download_keys.py [--out-file <путь к файлу (по умолчанию keys.txt)>]
                 [--format <txt|csv (по умолчанию txt)>]
                 [--count <количество ключей>]
                 [--country <название страны>]
                 [--delim <разделитель полей в CSV (по умолчанию ";")>]
```

Название страны можно получить из URL, например `https://outlinekeys.com/country/usa/ ==> usa`
