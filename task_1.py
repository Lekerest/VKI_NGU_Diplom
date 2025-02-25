times = '1h 45m,360s,25m,30m 120s,2h 60s' # Строка со временем
times = times.replace(' ', ',')
times = times.split(',') # На этом этапе получаем готовую строку 1 индекс - 1 время

#minutes = [] # В этом списке сохраним все значения переведенные в минуты

result_time_in_minutes = 0 # Переменная на вывод суммы минут

for time in times:
    if 'h' in time:
        #minutes.append(int(time.replace('h', '')) * 60)
        result_time_in_minutes += (int(time.replace('h', ''))*60)
    elif 'm' in time:
        #minutes.append(int(time.replace('m', '')))
        result_time_in_minutes += (int(time.replace('m', '')))
    else:
        #minutes.append(int(int(time.replace('s', ''))/60))
        result_time_in_minutes += (int(int(time.replace('s', ''))/60))

print('Всего', result_time_in_minutes, 'минут')


#                     Вопрос по такой проверке, на сколько она нужна?
#----------------------------------------------------------------------------------------------------------------------
# check_result_minutes = 0 # Переменная для проверки
#
# for minute in minutes:
#     check_result_minutes += minute # Подсчет минут из массива minutes
#
# if result_time_in_minutes == check_result_minutes:
#     print('Всего', result_time_in_minutes, 'минут')
#
# print(times)
# print(minutes)
