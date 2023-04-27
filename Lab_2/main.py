from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Parser import parse


def sort_drugs(drugs):
    sorted_drugs = drugs.copy()

    for i in range(len(sorted_drugs) - 1):
        for j in range(len(sorted_drugs) - i - 1):
            if float(sorted_drugs[j]["Цена"]) > float(sorted_drugs[j + 1]["Цена"]):
                sorted_drugs[j], sorted_drugs[j + 1] = sorted_drugs[j + 1], sorted_drugs[j]
    return sorted_drugs


def get_drugs(drug_name):
    url = "https://аптека-омск.рф/search?q=" + drug_name
    found_drugs = parse(url)
    return sort_drugs(found_drugs)


TOKEN_API = "6076130719:AAH5iEs1nRCyflCpk9Y7iMg5hj_zw_MK8AQ"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
drugs = []
current_drug = 0


async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    global drugs
    global current_drug
    drugs = []
    current_drug = 0

    await message.answer("Привет, я бот - поисковик лекарств. Введите название лекарства для поиска.")


async def send_drug_info(index, id):
    global drugs
    # Извлечение информации о лекарстве из переданного списка
    if len(drugs) == 0:
        await bot.send_message(chat_id=id, text="Не удалось найти лекарство(")
        return
    else:
        drug_data = drugs[index]

        name = drug_data["Название"]
        price = drug_data["Цена"]
        quantity = drug_data["Количество"]
        form = drug_data["Форма"]
        link = drug_data["Ссылка"]

        # Формирование текстового сообщения
        info_text = f"Название: {name}\nЦена: {price} руб.\nФорма: {form}\nКоличество: {quantity}"

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
    global drugs
    global current_drug

    if callback.data == "prev" and current_drug > 0:
        current_drug -= 1
        await send_drug_info(current_drug, callback.from_user.id)
        await callback.message.delete()
    elif callback.data == "next" and current_drug < len(drugs) - 1:
        current_drug += 1
        await send_drug_info(current_drug, callback.from_user.id)
        await callback.message.delete()
    elif callback.data == "back":
        drugs = []
        current_drug = 0
        await bot.send_message(chat_id=callback.from_user.id, text="Введите название для поиска.")
        await callback.message.delete()


@dp.message_handler()
async def find_by_name(message: types.Message):
    global drugs
    global current_drug

    if len(drugs) == 0:
        drug_name = message.text.title()

        drugs = get_drugs(drug_name)

        current_drug = 0

        await send_drug_info(current_drug, message.from_user.id)

    else:
        await bot.send_message(chat_id=message.from_user.id, text="Сначала вернитесь в меню или отправьте /start!")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
