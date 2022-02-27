import xlsxwriter
import string
import datetime

def write_report(items, finaly_info, fi, login, password, order):
    alphabet = string.ascii_uppercase
    date = datetime.datetime.now()
    date = str(date.day) + "." + str(date.month) + "." + str(date.year)
    workbook = xlsxwriter.Workbook(f'excels/Акт закупки № {login}_{date}_{order}.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.write(1, 5, f"Акт закупки № {login} / {date}", bold)
    worksheet.write(4, 4, "Способ доставки", bold)
    worksheet.write(5, 4, "Адрес доставки", bold)
    worksheet.write(6, 4, "Способ оплаты", bold)
    worksheet.write(7, 4, "Дата доставки", bold)

    worksheet.write(4, 5, "Доставка в пункт выдачи")
    worksheet.write(5, 5, items[0]["point_output"])
    worksheet.write(6, 5, "Оплата при получении")
    worksheet.write(8, 5, "Список товаров к закупке", bold)
    worksheet.write(7, 5, items[0]["delivery_time"])
    a10_l10 = ["код товара",	"количество",	"наименование",	"цена за еденицу по каталогу",	"общая стоимость по каталогу",	"скидка представителя",	"сумма со скидкой",	"себестоимость чистая за 1 единицу товара",	"себестоимость грязная за 1 единицу товара"]
    summary_arr = [a10_l10]
    row, col = 9, 0
    for item in items:
        summary_arr.append([item["code"], item["count"], item["name"], item["solo_price"].replace('руб', ''), item["all_price"].replace('руб', ''), item["sale"], item["price_with_discount"].replace('руб', ''), item["clear_cost"], item["dirt_cost"]])
        summary_arr.append(["", "", "Продукты без скидки", "", "", "", item['services_cost'], "", ""])
        summary_arr.append(["", "", "Сбор и доставка", "", "", "", item['taxes'], "", ""])
        summary_arr.append([])
    max_len_cols = [0] * len(summary_arr[0])
    for rows in range(len(summary_arr)):
        for cols in range(len(summary_arr[rows])):
            if rows == 0:
                worksheet.write(row, col, summary_arr[rows][cols], bold)
            else:
                worksheet.write(row, col, summary_arr[rows][cols])
            if max_len_cols[cols] < len(summary_arr[rows][cols]):
                max_len_cols[cols] = len(summary_arr[rows][cols])
            col += 1
        row += 1
        col = 0

    row += 2
    worksheet.write(row, 7, "Общее количество товара", bold)
    worksheet.write(row + 1, 7, "Общая сумма заказа", bold)
    worksheet.write(row + 2, 7, "Сумма скидки", bold)
    worksheet.write(row + 3, 7, "Предварительная сумма к оплате", bold)
    worksheet.write(row + 4, 7, "База для расчета скидки", bold)

    worksheet.write(row, 8, finaly_info[0])
    worksheet.write(row + 1, 8, finaly_info[1])
    worksheet.write(row + 2, 8, finaly_info[2])
    worksheet.write(row + 3, 8, finaly_info[3])
    worksheet.write(row + 4, 8, finaly_info[4])

    for i in range(len(max_len_cols)):
        worksheet.set_column(f'{alphabet[i]}:{alphabet[i]}', max_len_cols[i])
    workbook.close()
    return f'excels/Акт закупки № {login}_{date}_{order}.xlsx'


