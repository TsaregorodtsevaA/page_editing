
import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
d = {} #словарь с дублированиями с ключами - именем и фамилией
new_contacts_list = [] #итоговый список для отправки в файл
for el in contacts_list:
  count = el.count('')
  if '' in el:
    a=0
    while a!=count:
      el.remove('')
      a+=1

  pattern = r"[8\+7]+\s*\(*(\d\d\d)\)*\s*-*(\d\d\d)\-*(\d\d)-*(\d+)*\s*\(*([доб\. \d]*)\)*"
  right_form = re.sub(pattern, r'+7(\1)\2-\3-\4 \5', str(el))
  without_quotes = re.sub(r'[\[\'\]]+', '', right_form)
  if without_quotes.find(' ')<without_quotes.find(','):
    without_quotes = without_quotes.replace(' ', ', ', 1)
  if without_quotes[without_quotes.index(' ')+1:].find(' ')<without_quotes[without_quotes.index(' ') + 1:].find(','):
    without_quotes = without_quotes[0:without_quotes.index(' ')]+without_quotes[without_quotes.index(' ') + 1:].replace(' ', ', ', 1)
  sep = without_quotes.split(',')
  d.setdefault(sep[0]+', '+sep[1], sep[2:])
#создаю словарь без дублирований
no_duble = {}
for k, v in d.items():
  k = k.replace(' ', '')
  if k not in no_duble.keys():
    no_duble[k]=v
  else:
    no_duble[k]= set(no_duble[k]+v)
no_duble_list = list(no_duble.items())
#снова делаю список, только без дубликатов
for el1 in no_duble_list:
  norm_list = []
  for el2 in el1:
    if el2  == str(el2):
      delim = el2.split(',')
      for y in delim:
        norm_list.append(y)
    else:
      for val in el2:
        norm_list.append(val)
    #сортирую список для того, чтобы отправить в файл
  new_sorted_list = [norm_list[0], norm_list[1]]
  norm_list.remove(norm_list[0])
  norm_list.remove(norm_list[0])
  for surname in norm_list:
    if surname[-3:] == 'вич' or surname[-3:]== 'вна':
      new_sorted_list.append(surname)
      norm_list.remove(surname)

  for email in norm_list:
    if '@' in email:
      new_sorted_list.append(email)
      norm_list.remove(email)
  if len(new_sorted_list)<4:
    new_sorted_list.append('')

  for phone in norm_list:
    if phone.find('+7')!=-1:
      new_sorted_list.insert(-1, phone)
      norm_list.remove(phone)
  if len(new_sorted_list)<5:
    new_sorted_list.insert(-1, '')

  for position in norm_list:
    if position.count(' ')>1:
      new_sorted_list.insert(-2, position)
      norm_list.remove(position)
  if len(new_sorted_list)<6:
    new_sorted_list.insert(-2, '')

  for organization in norm_list:
    new_sorted_list.insert(-3, organization)
  if len(new_sorted_list)<7:
    new_sorted_list.insert(-3, '')
  new_contacts_list.append(new_sorted_list)

del(new_contacts_list[0])
new_contacts_list.insert(0, contacts_list[0])


with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_contacts_list)