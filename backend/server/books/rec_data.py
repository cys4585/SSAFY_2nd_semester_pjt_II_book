from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import pickle
import json


DATA_DIR = './books/fixtures'
ORIGIN_DATA_FILE = os.path.join(DATA_DIR, 'book_origin.json')
CBF_TAGNAME_FILE = os.path.join(DATA_DIR, 'cbf_tagname.pkl')


def dump_data(path):
    print('dump_data() 실행')
    with open(ORIGIN_DATA_FILE, 'r', encoding='utf8') as f:
        books = json.loads(f.read())
    book_ids = []
    book_tags = []
    for idx, book in enumerate(books):
        book_ids.append(idx + 1)
        book_tags.append(', '.join(book['tags']))
    print('book_ids & book_tags 생성...')

    # tag 너무 많이 겹치는 거 필터
    vect = TfidfVectorizer(max_df=50)
    sparse_matrix = vect.fit_transform(book_tags)

    tfidf_df = pd.DataFrame(sparse_matrix.toarray(),
                            index=book_ids, columns=sorted(vect.vocabulary_))
    print('tfidf_df 생성...')

    sim_np = cosine_similarity(tfidf_df, tfidf_df)
    sim_df = pd.DataFrame(sim_np, index=book_ids, columns=book_ids)
    print('sim_df 생성...')

    with open(path, 'wb') as f:
        pickle.dump(sim_df, f, protocol=pickle.HIGHEST_PROTOCOL)
    print('cbf_tagname.pkl 파일 생성...')
    print('Done!')
    print('dump_data() 종료')


def load_data(path):
    print('load cbf_tagname.pkl...')
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    if not os.path.exists(CBF_TAGNAME_FILE):
        dump_data(CBF_TAGNAME_FILE)
    print(load_data(CBF_TAGNAME_FILE))
