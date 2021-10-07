import json


# data 있는 json 파일 열기
with open("./books/fixtures/book_origin.json", "r", encoding="utf8") as f:
    books = f.read()
    json_data = json.loads(books)
    # print(json_data[0]['ISBN'])


# 태그 데이터
tag_dict = {}


def create_tag_data():

    with open("./books/fixtures/book.json", "r", encoding="utf8") as f:
        contents = f.read()
        tag_data = json.loads(contents)

        tag_id = 1
        tags = []  # 중복되지 않게 tag를 list에 넣어서 관리

        for book in json_data:
            # 태그 null 값이면 굳이 넣지말자
            if book['tags'] == None:

                continue

            for tag in book['tags']:

                # tags에 있으면 ㄴㄴ
                if tag in tags:
                    continue

                tags.append(tag)

                # 해당 태그의 book_id 리스트 넣어주기
                # book_id = 0
                # book_ids = []

                # for data in json_data:
                #     # book_id += 1
                #     if data['tags'] == None:
                #         continue

                # if tag in data['tags']:
                #     book_ids.append(book_id)

                tmp = {
                    'model': 'books.tag',
                    'pk': tag_id,
                    'fields': {
                        # 'books': book_ids,
                        'tag_name': tag,
                    }
                }
                tag_data.append(tmp)
                tag_dict[tag] = tag_id

                tag_id += 1

    with open("./books/fixtures/book.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(tag_data, ensure_ascii=False, indent=4))


# 책 데이터
def create_book_data():

    # n_data = open("./books/fixtures/book.json", 'a', encoding="utf-8")

    # 새로 만들어 줄 데이터 파일에 넣을라고~
    with open("./books/fixtures/book.json", "r", encoding="utf8") as f:
        contents = f.read()
        book_data = json.loads(contents)

        book_id = 1  # book의 id 값

        for book in json_data:
            tags = []

            for tag in book['tags']:
                tag_id = tag_dict[tag]
                tags.append(tag_id)

            book['like_users'] = []
            book['read_users'] = []
            tmp = {
                'model': 'books.book',
                'pk': book_id,
                # json으로 들어오는 필드명 != 모델에 정의한 필드명!!
                # 필드명 맞춰서 넣기
                'fields': {
                    'isbn': book['ISBN'],
                    'title': book['title'],
                    'author': book['author'],
                    'translator': book['translator'],
                    'publisher': book['publisher'],
                    'publish_date': book['date'],
                    'book_img': book['imgurl'],
                    'price': book['price'],
                    'page': book['page'],
                    'content': book['content'],
                    'kb_score': book['kb_score'],
                    'kb_review_cnt': book['kb_review_cnt'],
                    'tags': tags
                }
            }
            book_data.append(tmp)

            book_id += 1

    # 이렇게 하면 기존의 리스트에 안드가고 리스트가 새로생김
    # n_data.write(json.dumps(book_data, ensure_ascii=False, indent=4))
    # n_data.close()

    with open("./books/fixtures/book.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(book_data, ensure_ascii=False, indent=4))


# 카테고리 데이터
def create_category_data():

    # book 정보가 들어갔을 거니까 다시 읽어줘야지
    with open("./books/fixtures/book.json", "r", encoding="utf8") as f:
        contents = f.read()
        # book_data = json.loads(contents)
        category_data = json.loads(contents)

        book_id = 1
        for book in json_data:
            # 갖고오는 데이터의 ISBN과 pk 만들어준 book 데이터의 isbn 확인하고 book_id 가져오기 -> 카테고리는 굳이 ㄴㄴㄴㄴㄴㄴ!!!!!!
            # for data in book_data:
            #     if book['ISBN'] == data['fields']['isbn']:
            #         pk = data['pk']

            tmp = {
                'model': 'books.category',
                'pk': book_id,
                'fields': {
                    'book': book_id,
                    # category 5개 이하인거 처리해줘야함
                    # 'category_first': book['categories'][0],
                    # 'category_second': book['categories'][1],
                    # 'category_third': book['categories'][2],
                    # 'category_fourth': book['categories'][3],
                    # 'category_fifth': book['categories'][4],
                }
            }

            tmp['fields']['category_first'] = book['categories'][0]
            tmp['fields']['category_second'] = book['categories'][1]
            if len(book['categories']) > 2:
                tmp['fields']['category_third'] = book['categories'][2]
            if len(book['categories']) > 3:
                tmp['fields']['category_fourth'] = book['categories'][3]
            if len(book['categories']) > 4:
                tmp['fields']['category_fifth'] = book['categories'][4]

            category_data.append(tmp)

            book_id += 1

    with open("./books/fixtures/book.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(category_data, ensure_ascii=False, indent=4))


create_tag_data()
print('create_tag_data()')
create_book_data()
print('create_book_data()')
create_category_data()
print('create_category_data()')

# py manage.py loaddata books/books/fixtures/book.json
