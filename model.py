import pymysql
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from category_encoders import OrdinalEncoder
from sklearn.pipeline import make_pipeline
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score
import pickle

conn = pymysql.connect(
    user="aib15",
    passwd="gudrl123",
    host="127.0.0.1",
    db="searching_volume",
    cursorclass=pymysql.cursors.DictCursor
)

cur = conn.cursor()

sql = """SELECT i.*, w.avgTa,w.sumRn,w.sumSsHr
FROM searching i
INNER JOIN weather w 
ON i.date=w.date;"""

cur.execute(sql)
rows = cur.fetchall()

df = pd.DataFrame(rows)
df = df[~df['attraction'].str.contains("제주국제공항")]
df = df[~df['attraction'].str.contains("마트")]
df = df.drop(columns=['id','ranking','cities'], axis=1).reset_index(drop=True)

uni_date = list(df.date.unique())
uni_category = list(df.category.unique())
uni_date[0]

concat_df = pd.DataFrame()
for i in range(len(uni_date)):
  for j in range(len(uni_category)):
    new_df = pd.DataFrame.from_records([{'cate' : uni_category[j], 'dat' : uni_date[i]}])
    concat_df = pd.concat([concat_df, new_df], ignore_index=True)

rec_df = pd.DataFrame()
for i in range(len(concat_df['cate'])):
  a = df[(df['category']==concat_df['cate'][i]) & (df['date']==concat_df['dat'][i])].nlargest(3, 'volume')
  b = df[(df['category']==concat_df['cate'][i]) & (df['date']==concat_df['dat'][i])].drop(a.index)
  a['recommend'] = 1
  b['recommend'] = 0
  
  rec_df = pd.concat([rec_df,a,b])

rec_df = rec_df.drop(columns='volume', axis=1).reset_index(drop=True)


#모델링

target = 'recommend'
features = rec_df.drop(columns=target).columns

X = rec_df[features]
y = rec_df[target]

train, test = train_test_split(rec_df, test_size=0.2, random_state=2)

X_train, X_test = train[features], test[features]
y_train, y_test = train[target], test[target]

pipline = make_pipeline(
    OrdinalEncoder(),
    LGBMClassifier(
        objective='binary',
        n_estimators=1000,
        max_depth = 6,
        n_jobs=-1,
        reg_alpha=0.63,
        reg_lambda=0.56,
        subsample=0.8,
        scale_pos_weight=y_train.value_counts()[0]/y_train.value_counts()[1]
    )
)

pipline.fit(X_train, y_train)

y_pred_train = pipline.predict(X_train)
y_pred = pipline.predict(X_test)


y_real=y_train

def eval_models(y_pred, y_real=y_real):
    accuracy = accuracy_score(y_real, y_pred)
    precision = precision_score(y_real, y_pred)
    f1 = f1_score(y_real, y_pred)
    auc = roc_auc_score(y_real, y_pred)

    return accuracy, precision, f1, auc

train_acc, train_pre, train_f1, train_auc = eval_models(y_pred_train, y_real=y_train)
test_acc, test_pre, test_f1, test_auc = eval_models(y_pred, y_real=y_test)

with open('model.pkl', 'wb') as pickle_file:
  pickle.dump(pipline, pickle_file)

conn.close()