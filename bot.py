import requests
from random import choice


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


bot = BotHandler('454279758:AAFwAo5Te7YFOV_ZtO5u7V3FpXGUzGn7ePQ')


def main():
    new_offset = None
    last_msg = None
    while True:
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']  # текст сообщения пользователя
        last_chat_id = last_update['message']['chat']['id']  # id пользователя
        last_chat_name = last_update['message']['chat']['first_name']  # никнейм пользователя

        # handling
        if last_chat_text == '/start':
            bot.send_message(last_chat_id, 'Чего стоим? Сели! Урок начался.')
        else:
            if last_msg == 'Ты. К доске!':
                msg = "Кто ты сегодня?"
            else:
                msg = choice('Ты. К доске!', 'Помолчи! Я не твоя собственность.')
                last_msg = msg
                bot.send_message(last_chat_id, msg)
        # /handling

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
