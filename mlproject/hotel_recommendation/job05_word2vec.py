import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('./cleaned_reviews_final.csv')
df_review.info()

reviews = list(df_review['reviews'])
print(reviews[0])

tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=20, workers=4, epochs=100, sg=1)
# vector_size: 100 차원의 수로 줄인다(학습을 용이하게 하기 위해)
# window: 한 단어를 중심으로 좌우 몇 개의 단어를 컨텍스트(문맥)로 고려할지 결정 / 여기서는 중심 단어를 기준으로 좌우 4개의 단어를 컨텍스트(문맥)로 사용
# min_count: 최소출현빈도, 이 수를 넘겨야 학습에 포함시키겠다
# workers: 모델 학습 시 사용될 작업자 수 / cpu 어느정도 쓸지(여기서는 4개의 코어를 사용)
# sg: skip-gram의 약자로, 0일 경우 CBOW(Continuous Bag of Words), 1일 경우 Skip-Gram을 사용
# CBOW는 주변의 단어들을 바탕으로 중심 단어를 예측하는 방식으로 학습 / Skip-Gram은 반대로 중심 단어를 바탕으로 주변의 단어들을 예측하는 방식으로 학습
embedding_model.save('./models/word2vec_hotel_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))