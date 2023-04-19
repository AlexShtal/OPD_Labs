from bs4 import BeautifulSoup
import requests
import csv


def save_to_csv(data):
    with open("drugs.csv", mode="a+", newline='', encoding='utf-8') as w_file:
        names = ["Категория", "Название", "Полное название", "Ссылка"]
        file_writer = csv.DictWriter(w_file, delimiter=",",
                                     lineterminator="\n", fieldnames=names)
        for item in data:
            file_writer.writerow(item)


def parse():
    urls = {
        "Антисептики и дезинфекторы": "https://аптека-омск.рф/catalog/antiseptiki-i-dezinficiruyuschie-sredstva",
        "Глазные мази, гели и капли": "https://аптека-омск.рф/catalog/glaznye-mazi-geli-i-kapli",
        "Противопростудные комплексы": "https://аптека-омск.рф/catalog/protivoprostudnye-kompleksy",
        "Лечение некотиновой зависимости": "https://аптека-омск.рф/catalog/lechenie-nikotinovoy-zavisimosti",
        "Нервная система": "https://аптека-омск.рф/catalog/nervnaya-sistema",
        "От кашля": "https://аптека-омск.рф/catalog/preparaty-ot-kashlya",
        "От боли в горле": "https://аптека-омск.рф/catalog/sredstva-ot-boli-v-gorle",
        "Противовирусные": "https://аптека-омск.рф/catalog/protivovirusnye-preparaty",
        "От насморка": "https://аптека-омск.рф/catalog/sredstva-ot-nasmorka",
        "Дерматология": "https://аптека-омск.рф/catalog/dermatologiya",
        "Гомеопатические": "https://аптека-омск.рф/catalog/gomeopaticheskie-sredstva",
        "Контрацептивы": "https://аптека-омск.рф/catalog/kontraceptivnoe-sredstvo-dlya-mestnogo-primeneniya",
        "Лечение сахарного диабета": "https://аптека-омск.рф/catalog/preparaty-dlya-lecheniya-sakharnogo-diabeta",
        "Противогеморроидальные": "https://аптека-омск.рф/catalog/protivogemorroidalnye-preparaty",
        "Противогрибковые": "https://аптека-омск.рф/catalog/protivogribkovye-sredstva",
        "Иммуномодулирующее и иммуностимулирующее действие": "https://аптека-омск.рф/catalog/immunomoduliruyuschee-i-immunostimuliruyuschee-deystvie",
        "Против аллергии": "https://аптека-омск.рф/catalog/protivoalergicheskie-sredstva",
        "Травы, сборы, чаи": "https://аптека-омск.рф/catalog/travy-sbory-chai-0",
        "Ушные капли": "https://аптека-омск.рф/catalog/ushnye-kapli",
        "Витамины": "https://аптека-омск.рф/catalog/vitaminy",
        "Мочеполовая система и половые гормоны": "https://аптека-омск.рф/catalog/mochepolovaya-sistema-i-polovye-gormony",
        "Кроветворение и кровь": "https://аптека-омск.рф/catalog/krovetvorenie-i-krov",
        "Костно-мышечная система": "https://аптека-омск.рф/catalog/kostno-myshechnaya-sistema",
        "Дыхательная система": "https://аптека-омск.рф/catalog/dykhatelnaya-sistema",
        "Гормоны для системного применения (исключая половые гормоны и инсулин)": "https://аптека-омск.рф/catalog/gormony-dlya-sistemnogo-primeneniya-isklyuchaya-polovye-gormony-i-insulin",
        "Пищеварительный тракт и обмен веществ": "https://аптека-омск.рф/catalog/pischevaritelnyy-trakt-i-obmen-veschestv",
        "Противомикробные (системный приём)": "https://аптека-омск.рф/catalog/protivomikrobnye-preparaty-dlya-sistemnogo-primeneniya",
        "Противоопухолевые и иммуномодуляторы": "https://аптека-омск.рф/catalog/protivoopukholevye-preparaty-i-immunomodulyatory",
        "Сердечно-сосудистая система": "https://аптека-омск.рф/catalog/serdechno-sosudistaya-sistema",
        "Противопаразитарные, инсектициды и репелленты": "https://аптека-омск.рф/catalog/protivoparazitarnye-preparaty-insekticidy-i-repellenty",
        "Прочие": "https://аптека-омск.рф/catalog/prochie-preparaty"
    }

    # Перебор ссылок
    for category, url in urls.items():
        data = []

        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
        page = requests.get(url, headers=headers)
        print(page.status_code)

        soup = BeautifulSoup(page.text, "html.parser")

        soup_drugs = soup.find_all("div", "col-md-3 views-row")

        # Перебор лекарств
        for soup_drug in soup_drugs:
            info = dict()

            full_name = soup_drug.find("div", class_="h2").find("a").text.strip()

            ref = soup_drug.find("div", class_="h2").find("a", href=True)["href"]

            url = "https://аптека-омск.рф" + ref
            page = requests.get(url, headers=headers)
            html = BeautifulSoup(page.text, "html.parser")
            name = html.find("div",
                             class_="example1 clearfix text-formatted field field--name-field-pokazaniya field--type-text-long "
                                    "field--label-above").find("div", class_="field__label").text.strip()[25::]

            info["Категория"] = category
            info["Название"] = name
            info["Полное название"] = full_name
            info["Ссылка"] = url

            data.append(info)

            print(data)
            print(info["Категория"])
            print(info["Название"])
            print(info["Полное название"])
            print(info["Ссылка"], end="\n\n")

        save_to_csv(data)


parse()
