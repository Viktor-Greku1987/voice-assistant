# voice_assistant.1
В голосовом помощнике реализованы следующие функции:
  1)	Приветствие пользователя
  2)	Поиск файлов на ПК
  3)	Поиск информации в поисковой системе google
  4)	Прогноз погоды на 1 и 5 дней в разрезе трех часов и среднесуточных данных. Результат прогноза записывается в тектсовый файл в папку "Погода"
  5)	Выключение компьютера в установленное время 
Предварительная настойка:
В функции weather в стоке ity_ru_1 = open("C:/Python_work/voice-assistant/City_RU.txt") необходимо укзать обсалютную адресацию файла City_RU.txt на вашем ПК
В тоойже функци weather в строке with open('C:/Python_work/voice-assistant/Погода/Погода ' + text_city+ " "  + current_date +'.txt', 'w') as file: также необходимо указать  обсалютную адресацию папки "Погода" 

Иструкция пользования:
При запуске программы необходимо представиться, тем самым обозначив имя пользователя.
Голосовй помошник сам будет говорить когда нужно будет произносить фразу.
Любая команда начинается с имени голосового помошника "Максим"
Для получения информации из Google необходимо казать слово "онлайн" далее идет ваш запрос. 
Прогноз погоды можно получить на 1 или 5 дней в сокращенном или полном формате у казазав во фразе "подробно" или "кратко".

