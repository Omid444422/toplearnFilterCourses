from requests import get
from scrapy import Selector
from json import dumps

URL = 'https://toplearn.com/courses?Search=&orderby=createAndUpdatedate&filterby=all'
COURSES_INFORMATION = list()
FREE_COURSES_INFORMATION = list()

user_input = int(input('enter price: '))

isEnd = False
pageNumber = 1
counter = 0

while isEnd == False:

    response = get(f"{URL}&pageId={pageNumber}")
    response.encoding = 'utf-8'

    courses_title = Selector(response=response).css('#filter-search > div.main-content-page > div > div.col-lg-9.col-md-8.col-sm-12.col-xs-12.courses-view > div.row > div > div > h2 > a::text').getall()
    courses_url = Selector(response=response).css('#filter-search > div.main-content-page > div > div.col-lg-9.col-md-8.col-sm-12.col-xs-12.courses-view > div.row > div > div > h2 > a').xpath('@href').getall()
    courses_price = Selector(response=response).css('#filter-search > div.main-content-page > div > div.col-lg-9.col-md-8.col-sm-12.col-xs-12.courses-view > div.row > div > div > div.detail > div.bottom > span.price > i::text').getall()

    for index,course_price in enumerate(courses_price):

        if course_price.find('اعضای ویژه') > -1:
            continue

        if course_price.find('رایگان') > -1:
            course_title = courses_title[index]
            course_url = courses_url[index]
            
            FREE_COURSES_INFORMATION.append({'title': course_title,'url' : 'https://toplearn.com' + course_url, 'price' : course_price})
            counter += 1

            print('name: ' + course_title + ' ' + course_price)
            print(counter)

            continue


        if int(course_price.replace(',','')) <= user_input:
            course_title = courses_title[index]
            course_url = courses_url[index]
            
            COURSES_INFORMATION.append({'title': course_title,'url' : 'https://toplearn.com' + course_url, 'price' : course_price})
            counter += 1

            print('name: ' + course_title + ' ' + course_price)
            print(counter)

            continue
   
    pageNumber += 1

    if len(courses_title) == 1:
        isEnd = True


with open('output.json','w',encoding='utf-8') as json_output_file:
    json_output_file.write(dumps(COURSES_INFORMATION))


for course in COURSES_INFORMATION:
    with open('courses.txt','a',encoding='utf-8') as txt_output_file:
        txt_output_file.write(f"{course['title']} | price: {course['price']} \n")
        txt_output_file.write(f"url: {course['url']} \n")
        txt_output_file.write('='*100 + '\n')

 
#free courses 
with open('free.json','w',encoding='utf-8') as json_output_file:
    json_output_file.write(dumps(FREE_COURSES_INFORMATION))


for course in FREE_COURSES_INFORMATION:
    with open('free.txt','a',encoding='utf-8') as txt_output_file:
        txt_output_file.write(f"{course['title']} | price: {course['price']} \n")
        txt_output_file.write(f"url: {course['url']} \n")
        txt_output_file.write('='*100 + '\n')       

