# 📍 Система управления шаговыми двигателями листогибочного станка: Описание и документация
### Перечень оборудования которое было использовано
1. [***Arduino Uno***(ATmega)](https://arduino.ru/Hardware/ArduinoBoardUno)
<details>
  <summary>Показать изображение</summary>
  <img src="Image/uno_front.jpg" alt="Описание изображения">
</details>

2. [3 Шаговых двигателя ***Nema 17, 48mm, 42BYGH***](https://aliexpress.ru/item/32572890101.html?sku_id=12000045321628203&spm=a2g2w.productlist.search_results.0.2ea22371Z6YOiB)
<details>
  <summary>Показать изображение</summary>
  <img src="Image/nema.jpg" alt="Описание изображения">
</details>

3. [3 Драйвера для ***ШД DM542***](https://aliexpress.ru/item/1005005264850020.html?sku_id=12000032911624793&spm=a2g2w.productlist.search_results.2.fa701b2bq0H6ed)
<details>
  <summary>Показать изображение</summary>
  <img src="Image/Sd6065d17531b4bbda5b66bc2c6317f6cQ 1.jpg" alt="Описание изображения">
</details>

4. [Ультразвуковой датчик ***RCWL-1670***](https://amperkot.ru/msk/catalog/datchik_urovnya_vodyi_rcwl1670_ultrazvukovoy_335v_15_mka-40125591.html?srsltid=AfmBOop5HNY47JB7gNTX6L6XEZXqf481btrm2yCJ1y2oIrMoWw0PExUi)
<details>
  <summary>Показать изображение</summary>
  <img src="Image/rcwl.jpg" alt="Описание изображения">
</details>

<br>

## ℹ️ Описание
В современном производстве автоматизация играет ключевую роль в повышении эффективности и снижении затрат. Разработка системы управления шаговыми двигателями для листогибочного станка представляет собой актуальную задачу, направленную на автоматизацию процесса гибки листового металла, повышение точности и скорости операций, а также снижение влияния человеческого фактора. Внедрение такой системы позволит предприятиям оптимизировать производственный цикл и повысить конкурентоспособность.

<br>

## ⚙️Основные задачи
1. Подключение нескольких шаговых двигателей
2. Подключение датчика
3. Проектирование структурной схемы подключения
4. Сборка и подключение всех элементов
5. Тестирование готового стенда
6. Создание пользовательского интерфейса

<br>

## 📋 Структурная схема подключения

Схема довольно простая, думаю у вас не возникнет проблем с её чтением😄

![Alt text](Image/diagram.png)

<br>

## 🔞Подключение и запуск оборудования
### Нам понадобится
1. Компьютер
2. Провода для подключения
3. Макетная плата
4. Паяльная станция(Опционально)
### Подключение
1. Подключение Arduino UNO
   1. Для подключения Arduino UNO к компьютеру нужен кабель Тип A - USB 2.0 Тип B. На компьютер нужно установить Arduino IDE.

2. Подключение Ультразвукового датчика RCWL-1670
   1. Датчик имеет 4 выхода VCC ECHO TRIG GND. 
   2. VCC подключаем к 5V Arduino. 
   3. GND подключаем к GND на макетную плату, землю на макетную плату подводим с порта GND на Arduino. 
   4. Порты ECHO и TRIG втыкаем в любые 2 цифровых порта на Arduino 2-13, например 2 и 3.

3. Подключение Драйвера DM542 к Arduino Uno
   1.  PUL+ - Пульс для вращения ШД
   2. DIR+ - Направление вращение ШД
   3. ENA+ - Разрешение на работу ШД
   4. DIR и ENA являются не обязательным для работы ШД, но желательный для написания более сложной логики.
   5. PUL+, DIR+, ENA+ подключаем к цифровым портам Arduino 2-13, например 3, 4, 5.
   6. PUL-, DIR-, ENA- подключаем к GND на макетной плате.
   7. Все это повторяем на всех трёх драйверах ШД.

4. Подключение Шагового двигателя к Драйверу DM542
   1. На драйвере есть обозначение выходов A-. A+, B-. B+
   2. Нужно посмотреть в DataSheet нашего ШД что чему соответствует. Изучив DataSheet цвета проводов должны подключаться следующим образом. 
   3. BLK (черный) - A+
   4. GRN (зеленый) - A-
   5. RED (красный) - B+
   6. BLU (синий) - B-
   7. Повторяем на всех трёх ШД

5. Подключение питания
   1. На наших драйверах есть VCC и GND
   2. На нашем блоке питания 3шт V+ и 3шт V-
   3. Подключаем каждый V- к GND
   4. Подключаем Каждый V+ к VCC

<br>

### ❗ Проверим ❗
1. Arduino подключено к компьютеру - ✔️
2. RCWL-1670 подключен к питанию, а также в порты 2 и 3 - ✔️
3. Шаговые двигатели подключены правильно, PUL+, DIR+, ENA+ подключены в цифровые порты DM542(1)(4, 5,6); DM542(2)(7, 8,9); DM542(3)(10, 11,12) - ✔️
4. V+ и V- на БП подключены в нужные пины на каждом DM542 - ✔️
5. A-. A+, B-. B+ на DM542 подключены к нужным проводам ШД - ✔️

<br>

### 🆗 Если все верно, то можно подавать питание и включать.

<br>

##  💖Arduino UNO должна включиться и замигать светодиод на ней, БП должен начать работать, это можно заметить по жужжанию БП. На DM542 загорится лампочка. Если все получилось то поздравляю можно писать скетч в Arduino IDE.

<br>

## 🚪 Также на фреймворке Flet для Python был написан пользовательский интерфейс для работы с кодом.
##### Ознакомиться с описанием GUI можно по [этой ссылке](https://github.com/Lekerest/VKI_NGU_Diplom/blob/main/Python_GUI/README_GUI.md#%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D1%84%D1%80%D0%B5%D0%B9%D0%BC%D0%B2%D0%BE%D1%80%D0%BA%D0%B0-flet)
   <details>
    <summary>Выглядит как-то так(нажать надо)</summary>
    <img src="Image/gui.jpg" alt="Описание изображения">
  </details>

<br>

## 📸 Небольшой альбом, опционально к ознакомлению
<details>
    <summary>Выглядит как-то так(нажать надо)</summary>
    <img src="Image/albom_diplom_1.jpg" alt="Описание изображения">
    <img src="Image/albom_diplom_2.jpg" alt="Описание изображения">
    <img src="Image/albom_diplom_3.jpg" alt="Описание изображения">
    <img src="Image/albom_diplom_4.jpg" alt="Описание изображения">
    <img src="Image/albom_diplom_5.jpg" alt="Описание изображения">
    <img src="Image/albom_diplom_6.jpg" alt="Описание изображения">
    <img src="Image/albom_diplom_7.jpg" alt="Описание изображения">
</details>

<br>

>Этот файл был синхронизирован с Obsidian
>[Инструкция как сделать также](https://habr.com/ru/articles/843288/)
