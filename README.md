# Phonetic_AlgorithmRu

Phonetic algorithm for Russian

Фонетический алгоритм представляет собой алгоритм сравнения слов на основании их произношения.

### Необходимые пакеты для работы программы

Необходимы пакеты Numpy и Pandas

### Установка

Пакет можно скачать при помочь команды pip или pip3
```
pip install phonetic-algorithmRu
```

## Функции модуля transcription

### transcription(word, stress=False, next_word=False, separate=True, stop=False, vcd=False)
Осуществляет создание фонетической транскрипции для слова с заданным пользователем ударением
(номер гласного с конца слова). 
Требование указания слога с конца слова обусловлено тем, что функция обходит строку с конца.
Если аргумент ударения не заполнен, программа автоматически ставит ударение на слог по формуле

$$
\frac{Nvowls}{2} + 1
$$

#### Аргументы
word - слово на русском языке 
stress - номер слога с конца слова, на который должно падать ударение
separate - представление результата в виде массива фонетических представлений. При separate=False, программа вернет строку.
stop - при значении True ударение на слово не ставится
vcd - позволяет озвончить последний гласный

## Импортирование пакета

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
