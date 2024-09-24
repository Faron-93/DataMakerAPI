from faker import Faker
import random
import string
import time
import json
import os
import re

languages = {
        "English": "en_US",
        "Polish": "pl_PL",
        "Spanish": "es_ES"}

def cols(dictionary):
    keys = ''
    for i in dictionary:
        keys += i + ","
    keys_2 = keys[:-1]
    return keys_2

def long_last_name(fake):
    lastName = fake.last_name().upper() + '-' + fake.last_name().upper()
    return lastName

def special_string(word):
    uppercase_letters = list(string.ascii_uppercase)
    lowercase_letters = list(string.ascii_lowercase)
    new_str = ''
    for i in word:
        if i == "D":
            a = random.randint(0,9)
            new_str += str(a)
        elif i == "L":
            a = random.choice(uppercase_letters)
            new_str += a
        elif i == "l":
            a = random.choice(lowercase_letters)
            new_str += a
        else:
            new_str += i
    return new_str

def column_type(insert, fake):
    value = ""
    if insert["type"] == "first name":
        value = fake.first_name()
    elif insert["type"] == "last name":
        value = fake.last_name()
    elif insert["type"] == "city":
        value = fake.city()
    elif insert["type"] == "street":
        value = fake.street_name()
    elif insert["type"] == "email":
        value = fake.email()
    elif insert["type"] == "phone number":
        value = fake.phone_number()
    elif insert["type"] == "date":
        value = fake.date()
    elif insert["type"] == "integer":
        min = int(insert["min"])
        max = int(insert["max"])
        value = random.randint(min, max)
    elif insert["type"] == "integer as string":
        min = int(insert["min"])
        max = int(insert["max"])
        value = str(random.randint(min, max))
    elif insert["type"] == "constant_value":
        value = insert["value"]
    elif insert["type"] == "special_string":
        value = special_string(insert["value"])
    elif insert["type"] == "list":
        insert_list = re.split(r'\W+', insert["list"])
        value = random.choice(insert_list)
    return value

def pgsql_creator(dictionary, table_name, num_of_data, lang):
    languages = {
        "English": "en_US",
        "Polish": "pl_PL"
    }
    start = time.time()
    name = "export/" + table_name + "-" + str(start)[0:9] + ".txt"
    f = open(name, "w")
    fake = Faker([languages[lang]])
    error = 0
    columns = cols(dictionary)
    for num in range(num_of_data):
        query = ''
        for i in dictionary:
            value = column_type(dictionary[i], fake)
            if type(value) == str:
                query += "'" + str(value) + "'" + ","
            else:
                query += str(value) + ","
            query2 = query[:-1] + ""
        f.write("INSERT INTO" + str(table_name).upper() + "(" + str(columns).upper() + ") VALUES("+ str(query2) + "); \n")
    f.close()
    f = open(name, "r")
    response = f.read()
    f.close()
    os.remove(name)
    end = time.time()
    print(end - start)
    return response

def csv_creator(dictionary, table_name, num_of_data, lang):
    languages = {
        "English": "en_US",
        "Polish": "pl_PL"}
    start = time.time()
    name = "export/" + table_name + "-" + str(start)[0:9] + ".csv"
    f = open(name, "w")
    inserts = ''
    fake = Faker([languages[lang]])
    error = 0
    columns = cols(dictionary) + "\n"
    f.write(columns)
    for num in range(num_of_data):
        query = ''
        for i in dictionary:
            value = column_type(dictionary[i], fake)
            query += str(value) + ","
            query2 = query[:-1] + "\n"
        f.write(query2)
    f.close()
    f = open(name, "r")
    response = f.read()
    f.close()
    os.remove(name)
    end = time.time()
    print(end - start)
    return response



