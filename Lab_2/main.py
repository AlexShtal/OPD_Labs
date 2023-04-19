from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton
from aiogram.dispatcher.filters import Text
import csv


def read_csv():
    try:
        with open("drugs.csv", encoding='utf-8') as r_file:

            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.DictReader(r_file, delimiter=",")

            # Счетчик для подсчета количества строк и вывода заголовков столбцов
            count = 0

            # Считывание данных из CSV файла

            data = []
            for row in file_reader:
                info = {}
                if count == 0:
                    # Вывод строки, содержащей заголовки для столбцов
                    headers = row
                    count += 1
                else:
                    # Вывод строк

                    info["Категория"] = row["Категория"]
                    info["Название"] = row["Название"]
                    info["Полное название"] = row["Полное название"]
                    info["Ссылка"] = row["Ссылка"]

                    data.append(info)
    except FileNotFoundError as ex:
        print(ex)
    return data


TOKEN_API = "6076130719:AAH5iEs1nRCyflCpk9Y7iMg5hj_zw_MK8AQ"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

drugs = read_csv()
found_drugs = []
current_drug = 0


async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Привет, я бот - поисковик лекарств. Введите название лекарства для поиска.")


async def send_drug_info(index, id):
    # Извлечение информации о лекарстве из переданного словаря
    category = found_drugs[index].get('Категория')
    drug_name = found_drugs[index].get('Название')
    full_name = found_drugs[index].get('Полное название')
    link = found_drugs[index].get('Ссылка')

    # Формирование текстового сообщения
    info_text = f"Категория: {category}\nНазвание: {drug_name}\nПолное название: {full_name}"

    # Создание inline-клавиатуры с кнопками навигации
    ikb = InlineKeyboardMarkup(row_width=3)
    prev_button = InlineKeyboardButton('<<', callback_data='prev')
    next_button = InlineKeyboardButton('>>', callback_data='next')
    back_button = InlineKeyboardButton('В меню', callback_data='back')
    url_button = InlineKeyboardButton('Подробнее', url=link)
    ikb.add(prev_button, next_button, url_button).add(back_button)

    # Отправка сообщения пользователю с информацией о лекарстве и inline-клавиатурой
    await bot.send_message(chat_id=id, text=info_text, reply_markup=ikb)


@dp.callback_query_handler()
async def navigate(callback: types.CallbackQuery):
    global current_drug

    if callback.data == "prev" and current_drug > 0:
        current_drug -= 1
        await send_drug_info(current_drug, callback.from_user.id)
        await callback.message.delete()
    elif callback.data == "next" and current_drug < len(found_drugs) - 1:
        current_drug += 1
        await send_drug_info(current_drug, callback.from_user.id)
        await callback.message.delete()
    elif callback.data == "back":
        await bot.send_message(chat_id=callback.from_user.id, text="Введите название для поиска.")
        await callback.message.delete()



@dp.message_handler()
async def find_by_name(message: types.Message):
    drug_name = message.text.title()
    found_drugs.clear()
    current_drug = 0
    found = False

    for drug in drugs:
        if drug["Название"] == drug_name:
            found_drugs.append(drug)
            found = True
    if found:
        await send_drug_info(current_drug, message.from_user.id)
    else:
        await message.answer("Не удалось найти(")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
