import re
from bs4 import BeautifulSoup
import csv
import requests
import time

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
}
header = ["book_id","title","describe_title","author","describe_detail","price","price_pure_number","ori_price","ori_price_pure_number","discount","publishing_date","publishing_company","star","comment_num","url","image_url"]
book_count = 0


def format_str(s):
    return s.strip()


def format_discount(s):
    return s.replace("(", "").replace(")", "").replace("折", "").strip()


def format_publishing(s):
    return s.replace("/", "")


def format_star(s):
    return str(int(re.match("width: (\d+)%;", s).group(1)) // 10.)


def format_comment(s):
    return s.replace("条评论", "").strip()


def dict_to_file(book_info, filename):
    global header
    is_exist = check_file(filename)
    with open(filename,'a+', encoding="utf-8", newline="") as f:

        fieldnames = ["id","book_id","title","describe_title","author","describe_detail","price","price_pure_number","ori_price","ori_price_pure_number","discount","publishing_date","publishing_company","star","comment_num","url","image_url"]
        writer = csv.DictWriter(f=f, fieldnames=fieldnames)
        if is_exist == False:
            writer.writeheader()
        writer.writerow(book_info)

def check_file(filename):
    try:
        f = open(filename, 'r', encoding='utf-8')
    except:
        return False
    return True

def get_book_info(page, filename):
    global book_count
    count = 1
    base_url = "http://category.dangdang.com/pg{}-cp01.54.00.00.00.00.html".format(str(page))
    req = requests.get(base_url, headers=headers)
    html = BeautifulSoup(req.text,'lxml')
    # html = BeautifulSoup(html_data, 'lxml')

    html_books_block = html.select(".bigimg")[0]

    html_book_list = html_books_block.select("li[class^='line']")
    len_of_book_list = len(html_book_list)
    # book parser

    for book_item in html_book_list:
        try:
            book_id = book_item.get("id")
        except:
            book_id = ""
        try:
            title = book_item.select("a > img")[0].get("alt")
        except:
            title = ""
        try:
            describe_title = book_item.select("p.name > a")[0].get("title")
        except:
            describe_title = ""

        try:
            author = book_item.select("p.search_book_author > span > a")[0].get("title")
        except:
            author = ""

        try:
            describe_detail = book_item.select("p.detail")[0].get_text()
        except:
            describe_detail = ""

        try:
            price = book_item.select("p.price > span.search_now_price")[0].get_text()
        except:
            price = ""

        try:
            price_pure_number = price.replace("¥", "")
        except:
            price_pure_number = ""

        try:
            ori_price = book_item.select("p.price > span.search_pre_price")[0].get_text()
        except:
            ori_price = ""

        try:
            ori_price_pure_number = ori_price.replace("¥", "")
        except:
            ori_price_pure_number = ""

        try:
            discount = book_item.select("p.price > span.search_discount")[0].get_text()
        except:
            discount = ""

        try:
            publishing_date = book_item.select("p.search_book_author > span")[-2].get_text()
        except:
            publishing_date = ""

        try:
            publishing_company = book_item.select("p.search_book_author > span")[-1].get_text()
        except:
            publishing_company = ""

        try:
            star = book_item.select("p.search_star_line > span > span")[0].get("style")
        except:
            star = ""

        try:
            comment_num = book_item.select("p.search_star_line > a")[0].get_text()
        except:
            comment_num = ""

        try:
            url = book_item.select("p.name > a")[0].get("href")
        except:
            url = ""

        try:
            image_url = book_item.select("a > img")[0].get("src")
        except:
            image_url = ""
        book = {
            "book_id": format_str(book_id),  # id
            "title": format_str(title),  # 书名
            "describe_title": format_str(describe_title),  # 项目名
            "author": format_str(author),  # 作者
            "describe_detail": format_str(describe_detail),  # 图书介绍
            "price": format_str(price),  # 价格
            "price_pure_number": format_str(price_pure_number),  # 价格(纯数字)
            "ori_price": format_str(ori_price),  # 原价
            "ori_price_pure_number": format_str(ori_price_pure_number),  # 原价(纯数字)
            "discount": format_discount(discount),  # 折扣
            "publishing_date": format_publishing(publishing_date),  # 出版日期
            "publishing_company": format_publishing(publishing_company),  # 出版社
            "star": format_star(star),  # 评分
            "comment_num": format_comment(comment_num),  # 评论数
            "url": format_str(url),  # 连接地址
            "image_url": format_str(image_url)  # 图片地址
        }
        book["id"] = book_count
        book_count += 1
        count += 1
        dict_to_file(book, filename)
        print("第{}页第{}条记录，总共{}条记录".format(page, count, book_count))

if __name__ == '__main__':
    for page in range(1,101):
        print("开始爬第{}页".format(page))
        get_book_info(page, "books.csv")
        print("第{}页已爬完".format(page))
        time.sleep(3)
