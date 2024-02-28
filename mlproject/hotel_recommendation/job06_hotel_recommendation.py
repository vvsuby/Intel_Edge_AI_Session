import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1])) #sorting 하면 인덱스가 깨지기 때문에 enumerate로 인덱스를 같이 받아준다
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 0]
    return recmovieList[1:11]

df_reviews = pd.read_csv('./cleaned_reviews_final.csv')
Tfidf_matrix = mmread('./models/Tfidf_hotel_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 호텔 index 이용 추천
ref_idx = 1000
print(df_reviews.iloc[ref_idx, 0])
cosine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix) #코사인 유사도 값을 찾는다
print(cosine_sim[0])
print(len(cosine_sim))
recommendation = getRecommendation(cosine_sim)
print(recommendation)

#keyword 이용 추천
# embedded_model = Word2Vec.load('./models/word2vec_hotel_review.model')
# keyword = '바다'
# sim_world = embedded_model.wv.most_similar(keyword, topn=10)
# words = [keyword]
# for word, _ in sim_world:
#     words.append(word)
# sentence = []
# count = 10
# for word in words:
#     sentence = sentence + [word] * count
#     count -= 1
# sentence = ' '.join(sentence)
# print(sentence)
# sentence_vec = Tfidf.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
#
# print(recommendation)