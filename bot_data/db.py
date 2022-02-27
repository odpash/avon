import sqlite3
import json


def write_partner(data):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""INSERT INTO partners
                              (FIO)  VALUES  ('{data}')"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


def write_member(data):
    fio = get_members_list_from_partner(data['members_partner'])
    partners = []
    for i in fio:
        partners.append(i)
    partners.append(data['members_fio'])
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    if len(partners) == 1:
        sqlite_insert_query = f"""INSERT INTO members
                                      (partner, login, password, fio)  VALUES  (?, ?, ?, ?)"""
        cursor.execute(sqlite_insert_query, (
        data['members_partner'], data['members_login'], data['members_pass'], str(partners)))

    else:
        sqlite_insert_query = f"""UPDATE members SET
                                          partner=?, login=?, password=?, fio=? WHERE partner=(?)"""
        cursor.execute(sqlite_insert_query, (data['members_partner'], data['members_login'], data['members_pass'], str(partners), data['members_partner']))
    sqlite_connection.commit()
    cursor.close()


def get_members_list_from_partner(partner):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT fio FROM members where partner='{partner}'"""
    res = cursor.execute(sqlite_insert_query).fetchone()
    if res is None:
        return []
    return eval(res[0])


def get_partners_list():
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT FIO FROM partners"""
    res = cursor.execute(sqlite_insert_query)
    arr = []
    for i in res.fetchall():
        arr.append(i[0])
    cursor.close()
    return arr


def get_members_list_from_partner(partner):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT fio FROM members WHERE partner='{partner}'"""
    res = cursor.execute(sqlite_insert_query)
    try:
        arr = eval(res.fetchone()[0])
    except:
        arr = []
    cursor.close()
    return arr


def select_logpas_by_partner(partner):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT login, password FROM members WHERE partner='{partner}'"""
    res = cursor.execute(sqlite_insert_query)
    ans = res.fetchone()
    print(ans)
    cursor.close()
    return ans

def is_partner_has_member(partner):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT partner FROM members"""
    res = cursor.execute(sqlite_insert_query).fetchall()
    for i in res:
        if i[0] == partner.replace("partners_", ''):
            return True
    return False


def get_last_order():
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT * FROM orders"""
    res = cursor.execute(sqlite_insert_query).fetchall()
    return res[-1]


def get_order_by_id(id):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT * FROM orders where order_id={id}"""
    res = cursor.execute(sqlite_insert_query).fetchone()
    return res


def add_info_to_order(order_id, partner, item, count):
    order_info = get_order_by_id(order_id)
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    new_items = eval(order_info[2])
    new_items[int(item)] = int(count)
    sqlite_insert_query = f"""UPDATE orders SET items='{str(new_items)}' where order_id={order_id}"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()
    return order_id


def create_order(partner, item, count, current_member):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""INSERT INTO orders
                                  (partner, items, member) VALUES ('{partner}', '{str({int(item): int(count)})}', '{current_member}')"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()
    return get_last_order()[0]


def delete_order(id):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""DELETE FROM orders WHERE order_id={id}"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


def get_all_orders(partner, member):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""SELECT order_id, is_sended FROM orders WHERE partner='{partner}' AND member='{member}'"""
    res = cursor.execute(sqlite_insert_query).fetchall()
    ans = []
    for i in res:
        ans.append([i[0], i[1]])
    cursor.close()
    return ans


def update_order_status(order_id):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""UPDATE orders SET is_sended=1 WHERE order_id={order_id}"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()


def set_date(order_id, date):
    sqlite_connection = sqlite3.connect('bot_data/prod.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""UPDATE orders SET date='{date}' WHERE order_id={order_id}"""
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()