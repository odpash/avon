import bs4


def parse_statistic(html, fi, login, password):
    #html = open("test.html", 'r', encoding='UTF-8').read()
    b = bs4.BeautifulSoup(html, features="lxml")
    #print(str(b.findAll("div", {'class': "SubTotal_columns_border"})[1]))
    try:
        services_cost = bs4.BeautifulSoup(str(b.findAll("div", {'class': "SubTotal_columns_border"})[1]), features="lxml")

        services_cost = services_cost.find("li", {
            "class": "d-inline-block add-product__header-item text-center font-weight-bold w-15 my-4"}).text.strip().replace(
            'руб', '')
    except:
        services_cost = b.findAll("div", {"class": "p-2 bd-highlight SubTotal_Order-Total"})[-1].text.strip().replace("руб", '')
    point_output = b.find_all("li", {'class': "SubTotal_Estimated-Deli"})[3].text
    delivery_time = b.findAll('li', {'class': 'SubTotal_Estimated-Deli'})[4].text.split("Ожидаемая дата доставки")[1].strip()
    taxes = b.find("li", {'class': 'd-inline-block w-15 font-weight-bold text-center mt-2'}).text.strip().replace("руб", '')
    products_with_discount = bs4.BeautifulSoup(str(b.find("div", {'class', "SubTotal_columns_border withDiscount"})), features="lxml")
    idx = 0
    res = []
    for product in products_with_discount.findAll("ul", {"class": "list-unstyled SubTotal_table_contents mt-3 w-100"}):
        product = product.text.strip()
        if product == "":
            continue
        result = {"company": "", "code": "", "count": "", "name": "", "solo_price": "", "all_price": "", "sale": "",
                  "price_with_discount": "", "clear_cost": "", "dirt_cost": "", "services_cost": services_cost,
                  "taxes": taxes, "point_output": point_output, 'login': '', 'password': '', "fio": '', "delivery_time": delivery_time}

        product_arr = product.split('\n')
        for product in product_arr:
            product = bs4.BeautifulSoup(product, features='lxml').text
            idx += 1
            if idx == 1:
                result["company"] = product
            elif idx == 2:
                result["code"] = product
            elif idx == 3:
                result["count"] = product
            elif idx == 4:
                result["name"] = product
            elif idx == 5:
                result["solo_price"] = product
            elif idx == 6:
                result["all_price"] = product
            elif idx == 7:
                result["sale"] = product
                result["clear_cost"] = str(float(result["solo_price"].replace('руб', '')) * ((100 - float(product.replace("%", ''))) / 100))
                result['dirt_cost'] = str(float(result['clear_cost']) + (float(taxes) + float(services_cost)) / int(result["count"]))
            elif idx == 8:
                result['price_with_discount'] = product
                result['fio'] = fi
                result['login'] = login
                result['password'] = password
                idx = 0
                res.append(result)
                break

    finaly_info = []
    count = 0
    for i in res:
        count += int(i["count"])
    finaly_info.append(str(count))
    finaly_info.append(b.find('div', {'class': 'p-2 bd-highlight'}).text)
    items = b.findAll('div', {'class': "p-2 bd-highlight SubTotal_Order-Total"})
    for i in items:
        finaly_info.append(i.text)
    print(*res, sep='\n')
    print(finaly_info)
    return res, finaly_info
