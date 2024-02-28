import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel
import collections

form_window = uic.loadUiType('./hotel_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_hotel_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_hotel_review.model')
        self.df_reviews = pd.read_csv('./cleaned_reviews_final.csv')
        self.names = list(self.df_reviews['names'])
        self.regions = list(self.df_reviews['regions'])
        self.na_re = []
        self.hotel_name = []
        for i in range(len(self.names)):
            self.na_re.append([self.names[i], self.regions[i]])
        regions = ['부산', '충청',  '강원', '경기', '경상', '인천', '제주', '전라', '서울']
        regions.sort()
        self.cmb_region.addItem('지역을 선택해주세요')
        self.cmb_region.addItem('전국')
        for region in regions:
            self.cmb_region.addItem(region)

        self.hotel_flag = 0
        self.rec_flag = 1

        model = QStringListModel()
        model.setStringList(self.names)
        completer = QCompleter()
        completer.setModel(model)
        self.le_search.setCompleter(completer)

        self.cmb_region.currentIndexChanged.connect(self.select_regions)
        self.cmb_hotel.currentIndexChanged.connect(self.cmb_hotel_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)

    def select_regions(self):
        self.hotel_flag = 0
        self.lbl_keyword.setText('')
        self.hotel_name = []
        region = self.cmb_region.currentText()
        self.cmb_hotel.clear()
        # if self.cmb_region.currentIndex(0):
        #     self.lbl_hotel.setText('')
        if region == '전국':
            for i in range(len(self.names)):
                self.hotel_name.append(self.na_re[i][0])
        for i in range(len(self.names)):
            if self.na_re[i][1] == region:
                self.hotel_name.append(self.na_re[i][0])
        for name in self.hotel_name[:10]:
            self.lbl_hotel.setText("\n".join(self.hotel_name[:10]))
        self.hotel_name.sort()
        self.cmb_hotel.addItem('호텔을 선택해주세요')
        for name in self.hotel_name:
            self.cmb_hotel.addItem(name)
        self.hotel_flag = 1


    def cmb_hotel_slot(self):
        if self.hotel_flag == 1:
            name = self.cmb_hotel.currentText()
            recommendation = self.recommendation_by_name(name)
            self.lbl_hotel.setText(recommendation)
            words = self.relate_keyword(name)
            point = '\n'.join(list(words))
            self.lbl_keyword.setText(point)
        else:
            pass

    def btn_slot(self):
        # self.cmb_region.setCurrentIndex(0)
        # self.cmb_hotel.setCurrentIndex(0)
        key_word = self.le_search.text()
        if key_word in self.names:
            self.rec_flag = 0
            recommendation = self.recommendation_by_name(key_word)
            words = self.relate_keyword(key_word)
            keykey = '\n'.join(list(words))
            self.lbl_keyword.setText(keykey)
        else:
            recommendation = self.recommendation_by_keyword(key_word)
        if recommendation:
            self.lbl_hotel.setText(recommendation)
            if self.rec_flag:
                point = '\n'.join(list(self.words))
                self.lbl_keyword.setText(point)
            else:
                self.rec_flag = 1

    def recommendation_by_name(self, name):
        hotel_idx = self.df_reviews[self.df_reviews['names'] == name].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[hotel_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        print(recommendation)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def relate_keyword(self, name):
        hotel_idx = self.df_reviews[self.df_reviews['names'] == name].index[0]
        words = self.df_reviews.iloc[hotel_idx, 1].split()
        worddict = dict(collections.Counter(words))
        sorted_worddict = list(dict(sorted(worddict.items(), key= lambda item:item[1], reverse=True)).keys())
        sorted_worddict = sorted_worddict[:10]
        return sorted_worddict

    def recommendation_by_keyword(self, key_word):
        try:
            sim_world = self.embedding_model.wv.most_similar(key_word, topn=10)
        except:
            if key_word:
                self.lbl_hotel.setText('존재하지 않는 호텔입니다.')
                self.lbl_keyword.setText('존재하지 않는 키워드입니다.')
            else:
                self.lbl_hotel.setText('호텔을 입력해주세요.')
                self.lbl_keyword.setText('키워드를 입력해주세요.')
            return
        self.words = [key_word]
        for word, _ in sim_world:
            self.words.append(word)
        sentence = []
        count = 10
        for word in self.words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        print(sentence)
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1])
        if self.cmb_region.currentText() == '전국':
            simScore = simScore[:11]
            hotelIdx = [i[0] for i in simScore]
            rechotelList = list(self.df_reviews.iloc[hotelIdx, 0] + ' (' + self.df_reviews.iloc[hotelIdx, 2] + ')')
            return rechotelList[1:11]
        elif self.cmb_region.currentText() != '지역을 선택해주세요':
            simScore = simScore[:]
            hotelIdx = [i[0] for i in simScore]
            region_list = []
            for near in hotelIdx:
                if self.df_reviews.iloc[near, 2] == self.cmb_region.currentText():
                    region_list.append(self.df_reviews.iloc[near, 0] + ' (' + self.df_reviews.iloc[near, 2] + ')')
            return region_list[1:11]
        else:
            simScore = simScore[:11]
            hotelIdx = [i[0] for i in simScore]
            rechotelList = list(self.df_reviews.iloc[hotelIdx, 0] + ' (' + self.df_reviews.iloc[hotelIdx, 2] + ')')
            return rechotelList[1:11]



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())