from bs4 import BeautifulSoup
import requests


def parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'}
    page = requests.get(url, headers=headers)

    data = []

    soup = BeautifulSoup(page.text, "html.parser")

    drugs = soup.find("div", class_="view-content").find_all("div", class_="col-md-6 views-row")

    for drug in drugs:
        name = drug.find("div", class_="h2").find("a").text.strip()
        ref = "https://аптека-омск.рф" + drug.find("div", class_="h2").find("a").get("href")
        price = drug.find("div", class_="price-new").text.split(" ")[2].strip()

        quantity = drug.find("span", class_="colich").text[6::].strip()
        if quantity == "":
            quantity = "Не указано"

        form = drug.find("span", class_="forms").text.strip()
        if form == "":
            form = "Не указано"

        data.append({"Название": name,
                     "Ссылка": ref,
                     "Цена": price,
                     "Количество": quantity,
                     "Форма": form})

    return data


if __name__ == "__main__":
    parse()
