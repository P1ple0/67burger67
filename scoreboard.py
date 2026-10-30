import pyxel
import getpass
import requests
import datetime

# Страничка ручного редактирования:
# https://www.plainraw.com/edit/394a5c9527c9/d6919dc7d9724e2687ab3881697dd18a


def save(level, score):
    """ Сохраняем статистику
    :param level: уровень игрока
    :param score: очки """

    # Вычитываем старые данные
    text = read_api()

    # Сохраняем старые и новые данные
    score_new = f'{getpass.getuser()}|{datetime.datetime.now().replace(microsecond=0)}|{level}|{score}'
    if score_new not in text:  # не сохраняем дубликаты
        text = f'{getpass.getuser()}|{datetime.datetime.now().replace(microsecond=0)}|{level}|{score}\n{text}'
        send_api(text)

    # Формируем табличку
    results = []
    colors = {}
    iterator = iter([pyxel.COLOR_PEACH, pyxel.COLOR_PINK, pyxel.COLOR_YELLOW, pyxel.COLOR_ORANGE])
    items = text.split('\n')
    current = {}
    for i, item in enumerate(items):
        name, date, level, score = item.split('|')

        # Специально для Елисея
        if name == 'USER':
            name = 'Elisey'

        # Выбираем цвета текста в зависимости от имени пользователя
        if i == 0:
            color = pyxel.COLOR_RED
        elif colors.get(name):
            color = colors[name]
        else:
            color = next(iterator)
            colors[name] = color

        score = int(score)
        results.append({'name': name, 'date': date, 'level': level, 'score': score, 'color': color})
        if i == 0:
            current = {'name': name, 'date': date, 'level': level, 'score': score, 'color': color}
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    current_index = results.index(current)
    current['index'] = current_index
    results = results[:10]
    return {'results': results, 'current': current}


def send_api(text):
    """ Save text at PlainRaw site """
    requests.post('https://api.plainraw.com/api/update',
                  json={"uuid": "394a5c9527c9",
                        "editKey": "d6919dc7d9724e2687ab3881697dd18a",
                        "content": text})


def read_api():
    """Read score from PlainRaw site """
    r = requests.get('https://plainraw.com/raw/394a5c9527c9')
    return r.text


if __name__ == "__main__":
    send_api("SCORE 999")
