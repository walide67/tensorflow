import pandas as pd
import numpy as np
import pickle
import random
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Activation,Dense,Dropout
from sklearn.svm import libsvm
from sklearn.preprocessing import MultiLabelBinarizer
from pathlib import Path
import LeclercDataLoader as dataLoader
class text_classification():
    np.random.seed(12379)
    path_train="./base"
    products=dataLoader.read_leclerc_dataset(path_train)
    np.random.shuffle(products)
    train_size = int(len(products)*.7)

    #_____________________tronsforme to data frame with two columns text and category ________________
    df_product=pd.DataFrame(data=[product for product in products])
    train_text=df_product['text'][:train_size]
    train_categories=df_product['categories'][:train_size]
    test_text=df_product['text'][train_size:]
    test_categories=df_product['categories'][train_size:]
    vocab_size=15000
    batch_size=100
    tokenizer=Tokenizer(num_words=vocab_size, lower=True)
    tokenizer.fit_on_texts(train_text)
    x_train=tokenizer.texts_to_matrix(train_text,mode='tfidf')
    x_test=tokenizer.texts_to_matrix(test_text,mode='tfidf')
    encoder= MultiLabelBinarizer()
    encoder.fit(train_categories)
    y_train=encoder.transform(train_categories)
    y_test=encoder.transform(test_categories)
    model=Sequential()
    model.add(Dense(3000,input_shape=(vocab_size,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(3000))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(len(y_train[0])))
    model.add(Activation('sigmoid'))
    model.summary()
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    history=model.fit(x_train,y_train,batch_size=batch_size,epochs=5,verbose=1,validation_split=0.1)
    score=model.evaluate(x_test,y_test,batch_size=batch_size,verbose=1)
    print("test accuracy : ",score[1])
    print("========== just for test ============")
    text_labels = list(test_categories)
    for i in range(10):
        index=random.randint(0,len(x_test-1))
        prediction=model.predict(np.array([x_test[index]]))
        predicted_label=text_labels[np.argmax(prediction[0])]
        print("Actuel label", test_categories.iloc[index])
        print("predicted label : ", predicted_label)
        #=============Saving the model ===========================
       # model.model.save("text_classification.h5")

    '''
    predicted_label = list()
    for i in range(10):
        text_labels = encoder.classes_
        prediction=model.predict(np.array([x_test[random.randint(0,len(x_test-1))]]))
        predicted_label.clear()
        for j in range(3):
            predicted_label.append(text_labels[np.argmax(prediction[0])])
            text_labels=np.setdiff1d(text_labels,predicted_label)
        print("Actuel label",test_categories.iloc[i])
        print("predicted label : ",predicted_label)
    '''
#=============== class test ===================
test=text_classification()



