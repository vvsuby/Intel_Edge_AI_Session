import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

df = pd.read_csv('./cleaned_reviews_final.csv')
words = df.iloc[1320, 1].split() # 띄워쓰기 기준으로 나눠서 리스트로 만들어 줌
print(words)

worddict = collections.Counter(words) #pandas의 value_counts처럼 리스트 내의 유니크한 값들의 출현 빈도를 알려 줌
worddict = dict(worddict)
print(worddict)
print(type(worddict))

wordlcloud_img = WordCloud(background_color='white', max_words=2000, font_path=font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))
plt.imshow(wordlcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()