# coding=utf8
# библиотека для преобразования текста в аудио и его воспроизведение
import pyttsx3
# библиотека для снятия горлоса с микрофона и распознания
import speech_recognition
# работа со временем
import time
# выбор случайного ответа на фразу
import random
# сбора данных из сети
import requests
# работа с пайлами ПК, команда на выкл ПК
import os
import psutil
# парсинг. Для опораса гугла
from bs4 import BeautifulSoup
# открытие браузера
import webbrowser
# работа со временм
from datetime import datetime
# работа с потоками
import threading
# подключение гуглпереводчика
from googletrans import Translator
from translate import Translator
# собственная библиотека по преобразовании команды на квлючение ПК через какое-то или в какое-то время
import converter_text
# библиотека проверки имени
import check_name
# библиотека нахожения\проверки наличия в списке радиостанций
import chek_radio
import recognition
import camera
# бибилиотека городов. Применяется при поределении города в котором нужно сделать прогноз погоды
import geonamescache
# библиотека по получению нормальной (начальной формы) слова
import pymorphy2
# модуль, подключающий запись видео
import video_recording
# модуль, подключающий скрытую запись видео
import hidden_shooting
from radio_onlane import radio
from PyQt5 import QtWidgets  # все графи ческие элементы
import sys

name_user = ''
path_weather_save = ''
app = None
app_radio = None

answer = ''

# recognition.recognition_un()
# Вижу вас как на яву! Мое имя Максим. Я голосовой помошник.
greeting_BM = '  Давайте познакомимся. Как вас зовут?'
print(greeting_BM)
engin = recognition.init_engine()
recognition.sound(engin, greeting_BM)
time.sleep(2)
text_name = recognition.recognition_un()
name_user = check_name.check_name(text_name)
print("name_user : ", name_user)

# список для хранения найденых файлов при выполнения функции поиска файлов
list_file = list()

# инициализация интрументов распознания и ввода речи
recognizer = speech_recognition.Recognizer()
microphon = speech_recognition.Microphone()


# функция создает обект библиотеки pyttsx3 для воспроизведения ГОЛОСА , делает начальные настройки (из функции возвращщаем сам объект)
def init_engine():
    # созжаем объект для воспроизведения речи
    # global engin
    engin = pyttsx3.init('sapi5')  # sapi5 - это настройки голосового движка от майкрасовт
    # из движка получаем все голоса
    voices = engin.getProperty('voices')

    # for i in voices:
    # print(i)

    # настраиваем голос на русский женский Татьяна
    engin.setProperty('voice', voices[3].id)
    # настроим громкость воспроизведения
    # volume = engin.getProperty('volume')
    # print(volume)
    engin.setProperty('volume', 0.8)
    # настройка скорости воспроизведения звука
    rate = engin.getProperty('rate')
    # print(rate)
    engin.setProperty('rate', 185)
    # help(engin)
    return engin


# функция озвучки нужного тектса на вход принимает два параметра: настоенный голос и текст , который нужнго озвучить
def sound(engin, text):
    # вызываем функцию синтеза тектста в речь
    engin.say(text)
    # воспроизводим полученное аудио
    engin.runAndWait()


def first_hi(text):
    global name_user

    first_greeting = ['вижу вас, как на яву']

    first_greeting_1 = first_greeting
    print(first_greeting)
    engin = init_engine()
    sound(engin, first_greeting_1)

    greeting_BM = 'Мое имя, Максим . Я голосовой помошник. Как вас зовут?'
    print(greeting_BM)
    engin = init_engine()
    sound(engin, greeting_BM)
    time.sleep(2)
    text_name = recognition.recognition_un()
    name_user = check_name.check_name(text_name)
    print("name_user : ", name_user)
    return True


# ф-ция на наличе приветввия или прощания
def hi_goodby(text):
    global answer
    # global name_user
    morning = ['привет', 'доброго утра', 'хорошего утра']
    day = ['привет', 'добрый день', 'хорошего дня']
    evening = ['привет', 'добрый вечер', 'хорошего вечера']
    night = ['привет', 'доброй ночи', 'хорошей ночи']
    goodbye = ['досвидания', 'всего вам хорошего', 'всего хорошего', 'пока', 'до скорого', 'прощайте']

    answer = ''

    if text in morning or text in day or text in evening or text in night:
        # получаем текущее время на компьтере
        t = time.localtime()
        # извлечем из полученных данны кокретное время (часы)
        curent_time = int(time.strftime('%H', t))
        if curent_time >= 0 and curent_time <= 6:
            answer = night[random.randint(0, len(night) - 1)] + ',' + name_user

        elif curent_time > 6 and curent_time <= 12:
            answer = morning[random.randint(0, len(morning) - 1)] + ',' + name_user
        elif curent_time > 12 and curent_time <= 18:
            answer = day[random.randint(0, len(day) - 1)] + ',' + name_user
        elif curent_time > 18 and curent_time < 24:
            answer = evening[random.randint(0, len(evening) - 1)] + ',' + name_user

    elif text in goodbye:
        answer = goodbye[random.randint(0, len(goodbye) - 1)]

    # необходимо добавть elif  к внешенму if и проверить текст на прощание

    return answer != ""


# функция выдает погоду на день по городу Москва
def current_weather(appid, s_city='Moscow,RU', Ru_siti=''):
    city_id = 0
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:

        return 'данный город не известен'

    # получение текущей температуры по городу

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        # print(res)
        result = "Погода по городу " + Ru_siti + ' температура :' + str(data['main']['temp']) \
                 + ' максимальная температура :' + str(data['main']['temp_max']) \
                 + ' минммальная температура :' + str(data['main']['temp_min']) \
                 + ' осодки :' + str(data['weather'][0]['description'])
    except Exception as e:
        print('Ошибка (поиска):', e)
    return result


# получение температуры по городу на 5 дней
def weather_on_5_day(appid, s_city='Moscow,RU', Ru_siti=''):
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        return 'данный город не известен'

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric', 'long': 'ru', 'APPID': appid})
        data = res.json()

        result = "Погода по городу " + Ru_siti + ' температура :'
        for i in data['list']:
            result += i['dt_txt'] + ' Температура: {0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0][
                'description'] + "\n"

    except Exception as e:
        print('Ошибка (поиска):', e)
    return result


# погода на 5 дней краткая
def weather_on_5_day_briefly(appid, s_city='Moscow,RU', Ru_siti=''):
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        return 'данный город не известен'

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        count = 0
        summ = 0
        result = "Погода по городу " + Ru_siti + ' температура :'
        count_1 = True
        for i in data['list']:
            tame = i['dt_txt'].split()

            if tame[1] == '00:00:00':
                if count_1 == True:
                    tame_1 = tame[0]

                summ = summ / count
                result += tame_1 + ' Температура: {0:+3.0f}'.format(summ) + ' ' + i['weather'][0][
                    'description'] + "\n"
                count = 0
                summ = 0
            summ += i['main']['temp']
            count += 1
            tame_1 = tame[0]
            count_1 = False

    except Exception as e:
        print('Ошибка (поиска):', e)
    return result


# погода на один день расширенная(каждые 3 часа)
def weather_on_1_day_extended(appid, s_city='Moscow,RU', Ru_siti=''):
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        return 'данный город не известен'

    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric', 'long': 'ru', 'APPID': appid})
        data = res.json()

        result = "Погода по городу " + Ru_siti + ' температура :'
        for i in data['list']:
            tame = i['dt_txt'].split()[1]
            if tame == '00:00:00':
                break
            result += i['dt_txt'] + ' Температура: {0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0][
                'description'] + "\n"

    except Exception as e:
        print('Ошибка (поиска):', e)
    return result


def weather(text):
    global answer

    answer = ''
    text = text.split()
    print("text", text)
    pogoda = ["погода", "погоды", "погоду", "прогноз"]
    # text[1]= text[1][0].upper()+text[1][1::]
    check_pogoda = list(set(pogoda) & set(text))
    print("check_pogoda:", check_pogoda)
    if check_pogoda == []:
        return False

    # указать полученый API-ключ от сайта
    appid = 'ecf8f7c99b22ef5a327aa9d6f296cc4c'
    # new_taxt = ' '.join(text[2::])

    city_ru_1 = open("C:/Python_work/voice-assistant/City_RU.txt")
    city_lst_ru = []
    city_ist_list = []
    for carent_city in city_ru_1:
        city_lst_ru.append(carent_city.lower())

    for i in range(0, len(city_lst_ru)):
        if city_lst_ru[i][-1] == "\n":
            city_lst_ru[i] = city_lst_ru[i][0:-1]

    for city_ist in city_lst_ru:
        city_ist_list.append(city_ist)

    city_ist_list = ' '.join(city_ist_list[0:len(city_ist_list)])
    city_ist_list = city_ist_list.split()
    morph = pymorphy2.MorphAnalyzer()
    elem_lst = []
    # text = text.split()
    word_list = []
    result_list = []
    for i in text:
        word_list.append(i)
    for ii in word_list:
        p = morph.parse(ii)[0]
        res = p.normal_form
        result_list.append(res)
    for elem in result_list:
        elem_lst.append(elem)

    elem_lst = ' '.join(elem_lst[0: len(elem_lst)])
    elem_lst = elem_lst.split()

    lst_carent_city = list(set(city_ist_list) & set(elem_lst))
    print("lst_carent_city : ", lst_carent_city)
    if lst_carent_city:
        text_city = lst_carent_city[0]

    print(text_city)
    # text_city = ' '.join(text_city[0:len(text_city)])

    # создадим объект для переводчка
    trans = Translator(from_lang="ru", to_lang="en")
    name_syti = trans.translate(text_city)
    name_syti = ''.join(name_syti[0:len(name_syti)])
    print(name_syti)
    text = ' '.join(text[0:len(text)])
    print("text : ", text)
    one_day = '1 день'  # условие получения погоды на 1 день
    one_day1 = 'один день'
    five_day = 'на 5 дней'
    one_day_detail = 'на 1 день подробно'
    five_day_brief = 'на 5 дней кратко'
    if one_day or one_day1 in text:
        answer = current_weather(appid, name_syti + ',RU', text_city)
        print("answer : ", answer)
    elif five_day in text:
        answer = weather_on_5_day(appid, name_syti + ',RU', text_city)
    elif one_day_detail in text:
        answer = weather_on_1_day_extended(appid, name_syti + ',RU', text_city)
    elif five_day_brief in text:
        answer = weather_on_5_day_briefly(appid, name_syti + ',RU', text_city)
    current_date = datetime.now()
    current_date = str(current_date).split('.')[0]
    current_date = current_date.replace(':', '_')
    # запишем данные в файл (параметр 'w' указывает на перезщапись файла, если паратмтер 'a' - дозапись файла(добавление новой записи в документ))
    with open(path_weather_save + text_city + " " + current_date + '.txt', 'w') as file:
        file.write(answer)
    return answer != ''


# weather('прогноз погоды в москве на 1 день кратко ') # проверка работы функции

def calling_converter(text):
    text_1 = text.split()
    potok_list = []
    for u in text_1:
        potok_list.append(u)
    lst_chek = ["выключи", "выключение"]
    lst_rezult_chek = list(set(lst_chek) & set(potok_list))
    if lst_rezult_chek != []:
        text = text.split()
        text = ' '.join(text)

        text_2 = text.split('+')
        print("text", text)

        potok = threading.Thread(target=converter_text.clock_1, args=text_2)
        potok.start()

        return True
    else:
        return False


def calling_camera(text):
    text_1 = text.split()
    potok_list = []
    for u in text_1:
        potok_list.append(u)
    lst_chek = ["включи", "включите", "запусти", "запустите"]
    lst_chek_2 = ["вебку", "вебкамеру", "видео", "видеофиксацию", "видеонаблюдение", "веб-камеру", "камеру"]
    lst_chek_3_record = ['видезапись', "запись", "видефиксацию"]
    lst_chek_4_hidden_shooting = ['скрытая', 'скрытую', "видеосъемку"]
    lst_rezult_chek = list(set(lst_chek) & set(potok_list))
    lst_rezult_chek_2 = list(set(lst_chek_2) & set(potok_list))
    lst_rezult_record_3 = list(set(lst_chek_3_record) & set(potok_list))
    lst_rezult_hidden_shooting_4 = list(set(lst_chek_4_hidden_shooting) & set(potok_list))
    if lst_rezult_chek != []:
        if lst_rezult_chek_2 != []:
            potok_3 = threading.Thread(target=camera.VideoCap)
            potok_3.start()
            return True
        elif lst_rezult_record_3 != []:
            potok_4 = threading.Thread(target=video_recording.record_video)
            potok_4.start()
            return True
        elif lst_rezult_hidden_shooting_4 != []:
            potok_5 = threading.Thread(target=hidden_shooting.record_hidden)
            potok_5.start()
            return True
        else:
            return False


    else:
        return False


# ф-ция включения радио
def radiо_on(text):
    global app_radio
    global app
    global name_radio
    '''
    text = text.split()
    text = ' '.join(text)

    text_2 = text.split('+')
    potok_1 = threading.Thread(target=radiо_on, args=text_2)
    potok_1.start()
    '''
    chek_on_radio = ['радио']
    print("!!!!")
    text_1 = text.split()
    chek_list_on_radio = list(set(text_1) & set(chek_on_radio))
    if chek_list_on_radio != []:
        name_radio = chek_radio.chek_radiost(text)
        print("name_radio___", name_radio)
        if name_radio != '':

            name_radio = name_radio.split()
            print('name_radio_1', name_radio)
            name_radio = ' '.join(name_radio)

            name_radio = name_radio.split('+')
            print('name_radio----', name_radio)
            if app_radio == None:
                potok_1 = threading.Thread(target=potok_radio_on, args=name_radio)
                potok_1.start()
            else:
                print("^^^^")
                app_radio.radio_stop()
                print('sdsfjkhkfhg')
                #sys.exit(app.exec())
                print('chjdfkjjl')
                potok_1 = threading.Thread(target=potok_radio_on, args=name_radio)
                potok_1.start()
            """
            if app_radio == None:

                app = QtWidgets.QApplication([])
                app_radio = radio(name_radio)  # создаем объект класса. Вызов метода init  что выполянет созадние объекта класса.
                print(app_radio)
            else:
                app_radio.radio_stop()
                sys.exit(app.exec())
                app = QtWidgets.QApplication([])
                app_radio = radio(name_radio)
            """
        else:
            # команда не на включение радио
            return False
        return True
# функция запускает в потоке радио
def potok_radio_on(name_radio):
    global app_radio
    print("!")
    global app
    if app_radio == None:

        app = QtWidgets.QApplication([])
        print("name_radio::::",name_radio)
        app_radio = radio(name_radio)  # создаем объект класса. Вызов метода init  что выполянет созадние объекта класса.
        print(app_radio)
    else:
        app_radio.radio_stop()
        #sys.exit(app.exec())
        app = QtWidgets.QApplication([])
        app_radio = radio(name_radio)


#radiо_on('Викторию, включи радио европы плюсы') # проверка на пработоспособность ф-ции вклбчения радио
#  функция выключения радио
def radio_off(text):
    global app_radio
    global app
    if text == "выключи радио":
        if app_radio != None:
            app_radio.radio_stop()
            sys.exit(app.exec())
            app = None
            app_radio = None
        return True
    else:
        return False


# ф-ция обработки текста и выделения из них команд
def comands(text):
    if name_user == '':
        first_hi(text)
    else:
        if hi_goodby(text) or weather(text) or play_file(text) or goole_search(text) \
                or calling_converter(text) or calling_camera(text) or radiо_on(text) or radio_off(text):
            print(answer)
            engin = init_engine()
            sound(engin, answer)

        else:
            print(" я вас не поняла ")


# ф-ция нахожения файла по имени с возможностью указать расширение файла. На входе подставляем имя файла,
# при необходимости его расширение и диск на котором нужно искать файл

def file_search(my_path, name_file, expansion):
    # ф-ция walk находит все файлы по указанному пути
    for root_dir, dirs, files in os.walk(my_path):
        for file in files:
            # выражение разбивает название файла на имя файла и его расширение с помощью функци split
            file = file.lower()
            if file.split('.')[-1] == expansion:
                # ф-ция join  из модуля os.path объединят путь к папке и имя файла в полноценный путь
                name = os.path.join(root_dir, file)
                # производим поиск  искомого файла после фльтрации по расширению из оставшихся файлов одного расширения
                new_file = file.lower()
                if new_file.find(name_file) > -1:
                    list_file.append(name)


# ф-ция нахождения всех файлов по запросу на ПК и отображения результатов пользовотилю
def play_file(text):
    # команда для поиска файлов: файл,вид документа,название документа
    list_data = text.split()
    if list_data[0] != 'файл':
        return False
    list_disk = list()
    disks = psutil.disk_partitions()
    global list_file
    for i in disks:
        list_disk.append(i[0])
    if list_data[1] == 'музыка':
        list_file = list()
        name_file = ' '.join(list_data[2:len(list_data)])
        for disk in list_disk:
            file_search(disk, name_file, 'mp3')
    elif list_data[1] == 'текст':
        list_file = list()
        name_file = ' '.join(list_data[2:len(list_data)])
        for disk in list_disk:
            file_search(disk, name_file, 'docx')

    #  дополнить разилчными поисковыми запросами. возможно добаваить неограниченное коилчество запросов на поиск данных
    global answer
    answer = ''
    if len(list_file) > 0:
        for file in list_file:
            print(file)
        answer = 'файлы найдены'
        # запустим первый найденый файл в роднм приложении
        os.startfile(list_file[0])
        """
        # запустими все найденные файлы
        for i in range(len(list_file)):
            os.startfile(list_file[i])
        """
    else:
        answer = 'файлы не найдены'
    return True


def goole_search(name_search=''):
    #print(name_search)
    name_search = name_search.split()
    #print(name_search)
    if name_search[0] != 'онлайн':
        return False
    name_search = ' '.join(name_search[1:len(name_search)])
    #print(name_search)
    name_search = name_search.replace(" ", "+")
    url = f"http://www.google.com/search?q={name_search}"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intell Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    page = requests.get(url, headers=headers)
    # print(page)
    result = BeautifulSoup(page.content, "html.parser")
    # print(result)
    result_url = []
    # print(result.find_all("div", class_="g"))
    for g in result.find_all("div", class_="g"):
        anchors = g.find_all("a")
        if anchors:
            link = anchors[0]["href"]
            title = g.find("h3").text
            item = {"title": title, "link": link}
            result_url.append(item)
    # откроем первую из найденных ссылок в браузере
    # print(len(result_url))
    print("полученные результаты запроса")
    for data_link in result_url:
        print(data_link.get('title'))
        print(data_link.get('link'))
        print('_________')
    global answer
    answer = 'по вашему запросу найдены ' + str(len(result_url)) + 'ссылок'
    engin = init_engine()
    sound(engin, answer)
    inf_open = 'открою для Вас первую из них'
    engin = init_engine()
    sound(engin, inf_open)
    url = result_url[0].get('link')
    webbrowser.open(url)
    engine = init_engine()
    sound(engine, 'результаты запроса сохраним для вас в фа́йл: гугл')
    n = 0
    p = ''
    for data_resul in result_url:
        n += 1
        p += str(n) + ') ' + data_resul.get('title') + '\n' + data_resul.get('link') + '\n'

    with open(path_google + 'googl.txt', 'w') as file:
        file.write(p)
    return True


# функция распозания речи
def recognize_speech():
    audio = 'я Вас не поняла'
    while True:
        with microphon:
            data = ''
            # регулировка окружаюещго шума
            recognizer.adjust_for_ambient_noise(microphon, duration=2)
            try:
                comad = name_user + "," 'задайте команду '
                engin = init_engine()
                sound(engin, comad)
                print(comad)
                # получим данные с миукрофона ввиде аудиопересменной
                audio = recognizer.listen(microphon)
            except Exception as ex:
                print('Я вас не расслышал. Посторите : ', ex)
                return ''
            except Exception as ex:
                print('ошибка : ', ex)
                return ''
            #global data
            try:

                # распознание аудио онлайн через гугл
                data = recognizer.recognize_google(audio, language='ru')
            except Exception as ex:
                continue
            return data.lower()


# weather('погода Билибино на пять дней кратко' )
# print(answer)
# goole_search('онлайн Дом')
# print(answer)
"""
file = open('config.txt','r')
for line in file:
    print(line)

    if line == '':
        line = 'C:'
    elif line[-1] == '\n':
        line = line[:len(line)-1]

line = line.split(";")
if line[0] == "path_weather":
    path_weather_save = line[1]
    print("погода", path_weather_save)
    
if line[0] == 'path_google':
    path_google = line[1]
    print('google:', path_google)
"""
# if line == '':
# line = 'C:'
with open('config.txt', 'r') as file:
    while True:

        line = file.readline()

        if line == '':
            break
        if line[-1] == '\n':
            line = line[:len(line) - 1]
        line = line.split(";")
        #print("line: ", line)

        if len(line) == 2:
            if line[0] == "path_weather":
                path_weather_save = line[1]
                #print("погода", path_weather_save)

            elif line[0] == 'path_google':
                path_google = line[1]
                #print('google:', path_google)

# exit(0)

while True:
    text = recognize_speech()
    if "максим" in text:
        text = text.split()
        for mks, id_mks in enumerate(text):
            if id_mks == "максим":
                text = ' '.join(text[mks + 1:len(text)])
                print(text)
                comands(text)

# play_file('файл текст виктор')
# print(list_file)
# file_search('C:\Python_version2\independent_work_2','2','py')
# print('вы сказади :', recognize_speech())
# init_engine()
'''
with open('Погода/TTTT.txt', 'w') as file:
    file.write("answer")
'''
