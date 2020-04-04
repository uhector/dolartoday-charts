# -*- coding: utf-8 -*-

import datetime
import xlrd

def sort_date_values_list(date_values_list) -> list:
    ordered_values = list(reversed(date_values_list))
    ordered_values[1], ordered_values[2] = ordered_values[2], ordered_values[1]
    return ordered_values

def get_list_from_string(string) -> list:
    return string.split('-')

def get_date_object_from_string(string) -> 'Date Object':
    formatted_date = sort_date_values_list(get_list_from_string(string))
    formatted_date = list(map(lambda x: int(x), formatted_date))
    return datetime.date(formatted_date[0],
                         formatted_date[1],
                         formatted_date[2])

def get_current_year():
    return str(datetime.date.today().year)

def get_spreadsheets_object(file_name, sheet_name):
    file = xlrd.open_workbook(file_name)
    return file.sheet_by_name(sheet_name)
