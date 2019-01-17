import LeclercDataLoader as dataLoader
import re
import sys
import math
from nltk.tokenize import word_tokenize,punkt
import string
class Tfidf_vec():
    dataset_path = "./base"
    #__________________restructuré les donees
    def prepare_dataset(self,percent):
        products=dataLoader.read_leclerc_dataset(self.dataset_path)
        texts=list()
        categories=list()
        percent=100
        i=0
        for product in products:
            i=i+1
            texts.append([w.lower() for w in word_tokenize(str(product['text']),'french') if w not in string.punctuation])
            categories.append([w.lower() for w in word_tokenize(str(product['categories']),'french') if w not in string.punctuation])
            sys.stdout.write("\rpreparing dataset : "+str(round((i/len(products))*100,2))+" %")
            if (((i / len(products)) * 100) >= percent):
                return {'texts': texts, 'categories': categories}
        return {'texts': texts,'categories' : categories}

#_______________ calculate term freconcy _______________________#

    def cal_tf(self,word,text):
        return text.count(word)

 # _______________ calculate document freconcy _______________________#
    def cal_df(self,word,texts,percent):
        count_word=0
        i=0
        for text in texts:
            if word in text:
                count_word=count_word+1
            if (((i/len(texts))*100)>=percent):
                return count_word
        return count_word

    # _______________ calculate tf-idf _______________________#
    def calculate_tf_idf(self,texts,percent):
        tf_idf_list=list()
        i=0
        for text in texts:
            tf_idf_text={}
            sys.stdout.write("\rprocessing text N° "+str(i)+" : " + str(round((i / len(texts)) * 100, 2)) + " %")
            for word in text:
                tf_word=self.cal_tf(word,text)
                df_word= self.cal_df(word,texts,percent)
                tf_idf = math.log10(1 +tf_word)*math.log10(len(texts)/df_word)
                tf_idf_text[word]=tf_idf
            tf_idf_list.append(tf_idf_text)
            i+=1
            if (((i/len(texts))*100)>=percent):
                return tf_idf_list
        return tf_idf_list
    def tf_idf(self,percent=100):
        products_list = self.prepare_dataset(percent)
        print("____ calculate tf-idf of texts ______")
        texts=self.calculate_tf_idf(products_list['texts'],percent)
        print("____ calculate tf-idf of categories ______")
        categories=self.calculate_tf_idf(products_list['categories'],percent)
        return {'texts': texts,'categories': categories}



test =Tfidf_vec()
list_test=test.tf_idf(0.01)['texts']
for l in list_test:
    print("text : ",l,"\n")
