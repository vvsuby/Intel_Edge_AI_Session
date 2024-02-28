import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./cleaned_reviews_final.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
# sublinear_tf=True: 로그를 적용하는 것을 의미 =>  예를 들어, 단어가 20번 등장하는 것이 10번 등장하는 것보다 2배 더 중요하지 않을 수 있다
# 즉 선형적으로 증가하는 것이 아니라 TF 값이 1, 10, 100일 때 각각 로그 변환된 값은 약 0, 1, 2로 값을 조정해주는 것을 의미
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
# 'reviews' 열의 텍스트 데이터를 TF-IDF 방식으로 벡터화하고, 그 결과를 희소 행렬로 저장
# 희소 행렬(Sparse Matrix): 행렬의 원소 중에 많은 항들이 '0'으로 구성되어 있는 행렬
# 희소 행렬의 대부분의 항은 '0'으로 이루어져 있어, 실제 사용하지 않는 메모리 공간으로 인해 메모리 낭비가 발생하게 된다
# 그러나 0 값을 제외하고 0이 아닌 값(비영 요소)만 따로 추출하여 새로운 배열로 구성하는 방법을 사용함으로써 메모리를 효율적으로 사용할 수 있다.
# 관련자료: https://sweetnew.tistory.com/436
print(Tfidf_matrix.shape)
# # TF-IDF 벡터화를 거친 결과 행렬이 1329개의 행(문서)과 28150개의 열(단어)를 가진다는 것을 의미
# # 즉 여기서는 1329개의 호텔과 문서전체의 동사 형용사 가 28150개의 단어로 표현이 된다

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_hotel_review.mtx', Tfidf_matrix)
# Matrix Market 포맷의 파일로 저장하고 이 파일은 희소 행렬 데이터를 효율적으로 저장하고 불러올 수 있습니다.
# 단어를 백터화 해주는 작업