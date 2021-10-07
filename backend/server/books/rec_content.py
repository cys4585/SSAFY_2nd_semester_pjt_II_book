# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import pickle
import json
from konlpy.tag import Komoran


komoran = Komoran()

# word = komoran.nouns(u"19세기 영어와 번역 문학을 동시에 즐길 수 있는 모든 셜로키언을 위한 즐거운 가이드 북   “왓슨 박사님, 이쪽은 셜록 홈즈 씨입니다.” 스탬퍼드가 우리 두 사람 을 소개시켜 주었다.  “안녕하십니까? 아프가니스탄에 계시다 왔군요.” 그가 친근하게 인사를 건네며 내 손을 꼭 쥐었는데 보기보다 손아귀 힘이 꽤 셌다.  “도대체 그걸 어떻게 아신 겁니까?” 나는 깜짝 놀라며 물었다.  “아, 별것 아닙니다.” 그는 장난스럽게 웃으며 말했다.   “Dr. Watson, Mr. Sherlock Holmes,” said Stamford, introducing us.  “How are you?” he said cordially, gripping my hand with a strength  for which I should hardly have given him credit. “You have been in  Afghanistan, I perceive.”  “How on earth did you know that?” I asked in astonishment.  “Never mind,” said he, chuckling to himself.   왓슨은 첫눈에 셜록 홈즈가 놀라운 추론을 했다는 것을 알 수 있었습니다. 하지만 그들이 데뷔한 뒤 한 세기가 지나도록 전 세계인들에게 인기를 끌 것이라고는 상상조차 하지 못했습니다. 코난 도일은 장편 소설 4권과 단편 56편으로 100년이 넘는 세월 동안 독자들을 감동시키는 극적인 모험을 창조했으며, 숙련된 플롯, 시대적인 세부 사항, 등장인물의 유머 및 독특한 캐릭터를 제공합니다. 홈즈의 팬에게 풍성한 상상의 세계로 돌아가는 것과 비교할 만한 즐거움은 없습니다. 19세기 빅토리아 시대의 어슴푸레한 가스등 거리, 221B 베이커 스트리트, 그 당시 삶을 느낄 수 있는 여러 장치 등 모든 것이 이 책이 담겨 있습니다.    《영문과 함께하는 1일 1편 셜록 홈즈 365》는 세계 유일의 컨설팅 탐정 팬을 위한 완벽한 침대 옆 동반자입니다. 독자들은 셜록 홈즈의 모든 이야기를 언제 어디서든 부담 없이 1년 내내 영어 원문과 함께 읽을 수 있습니다. 이제껏 출간된 그 어떤 책도 홈즈 팬에게 이보다 큰 즐거움을 가져다주지 않을 것입니다. 책을 읽으며 19세기 영국 영어와 오늘날 미국 영어의 차이점을 느껴 보는 것도 이 책이 주는 또 다른 즐거움입니다. 시카고대학에서 심혈을 기울인 365개의 인용문이 있는 이 책은 세계 최고의 탐정 팬에게 완벽한 선물입니다.")
# word = list(set(word))
# for w in word:
#     if len(w) == 1:
#         word.remove(w)
# print(word)


DATA_DIR = './books/fixtures'
ORIGIN_DATA_FILE = os.path.join(DATA_DIR, 'book_origin.json')
CBF_CONTENT_FILE = os.path.join(DATA_DIR, 'cbf_content.pkl')


def dump_data(path):
    print('dump+_data() 실행')
    with open(ORIGIN_DATA_FILE, 'r', encoding='utf8') as f:
        books = json.loads(f.read())

    remove_words = [
        '베스트셀러', '독자', '베스트', '베스트 셀러',
        '책', '저자', '작가', '원문', '의역', '번역',
        '권', '단어', '출간', '도서', '독자층', '시리즈',
        '작품', '것']
    book_ids = []
    book_contents = []
    # book_contents = []
    for idx, book in enumerate(books):
        if book['content']:
            book_ids.append(idx + 1)
            content_nouns = komoran.nouns(book['content'])
            content_nouns = list(set(content_nouns))
            for nouns in content_nouns:
                if nouns in remove_words:
                    content_nouns.remove(nouns)
            # for i in content_nouns:
            #     if len(i) == 1:
            #         content_nouns.remove(i)
            book_contents.append(', '.join(content_nouns))
            # book_contents.append(book['content'])
    print('book_ids & book_contents 생성...')

    vect = TfidfVectorizer()
    sparse_matrix = vect.fit_transform(book_contents)

    tfidf_df = pd.DataFrame(sparse_matrix.toarray(),
                            index=book_ids, columns=sorted(vect.vocabulary_))
    print('tfidf_df 생성')

    sim_np = cosine_similarity(tfidf_df, tfidf_df)
    sim_df = pd.DataFrame(sim_np, index=book_ids, columns=book_ids)
    print('sim_df 생성')

    with open(path, 'wb') as f:
        pickle.dump(sim_df, f, protocol=pickle.HIGHEST_PROTOCOL)
    print('cbf_tagname.pkl 파일 생성...')
    print('파일 생성')
    print('Done!')


def load_data(path):
    print('load cbf_content.pkl...')
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    if not os.path.exists(CBF_CONTENT_FILE):
        dump_data(CBF_CONTENT_FILE)
    print(load_data(CBF_CONTENT_FILE))
