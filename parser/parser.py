import os
import sys
import django
import requests
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils.text import slugify
from products.models import Category, SubCategory, Items


BASE_URL = "https://www.kivano.kg"


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def parse():
    soup = get_soup(BASE_URL)

    # Находим категории
    category_divs = soup.find_all("div", class_="leftmenu-title arrowRight")

    for cat_div in category_divs[:10]:  # Ограничим до 10 категорий
        a_tag = cat_div.find("a")
        cat_name = a_tag.text.strip()
        cat_url = BASE_URL + a_tag['href']

        category, _ = Category.objects.get_or_create(name=cat_name)
        print(f"[+] Категория: {cat_name}")

        # Парсим подкатегории (до 5)
        cat_soup = get_soup(cat_url)
        sub_divs = cat_soup.find_all("div", class_="secondli")[:5]

        for sub_div in sub_divs:
            sub_a = sub_div.find("a")
            sub_name = sub_a.text.strip()
            sub_url = BASE_URL + sub_a['href']

            subcategory, _ = SubCategory.objects.get_or_create(category=category, name=sub_name)
            print(f"    └─ Подкатегория: {sub_name}")

            # Парсим товары (до 10)
            sub_soup = get_soup(sub_url)
            item_divs = sub_soup.find_all("div", class_="item product_listbox oh")[:10]

            for item_div in item_divs:
                title_tag = item_div.find("div", class_="listbox_title oh")
                price_tag = item_div.find("div", class_="listbox_price text-center")
                img_tag = item_div.find("div", class_="listbox_img pull-left").find("img")

                title = title_tag.text.strip() if title_tag else "Без названия"
                price_str = price_tag.text.strip().replace("сом", "").replace(" ", "") if price_tag else "0"
                price = Decimal(price_str) if price_str.isdigit() else Decimal("0")
                image_url = BASE_URL + img_tag['src'] if img_tag and img_tag.get("src") else None
                slug = slugify(title)

                item, created = Items.objects.get_or_create(
                    title=title,
                    subcategory=subcategory,
                    defaults={
                        "slug": slug,
                        "price": price,
                        "is_available": True,
                        "image": image_url,
                        "is_active": True,
                        "is_deleted": False,
                    }
                )
                status = "Создан" if created else "Уже есть"
                print(f"        └─ [{status}] {title} | {price} сом")

if __name__ == "__main__":
    parse()

