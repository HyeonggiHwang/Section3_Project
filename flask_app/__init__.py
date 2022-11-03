from flask import Flask, render_template, request
import pickle
import pandas as pd
import os



rec_df = pd.read_csv('rec_df.csv')

model = None
with open('model.pkl','rb') as pickle_file:
    model = pickle.load(pickle_file)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    category = request.form['category']
    subcategory = request.form['subcategory']
    date = request.form['date']
    avgTa = request.form['avgTa']
    sumRn = request.form['sumRn']
    sumSsHr = request.form['sumSsHr']
    
    category_df = rec_df[(rec_df['category']==category) & (rec_df['subcategory']==subcategory)]
    att_list = category_df['attraction'].unique()

    rec_list = []
    for att in att_list:
        X_test = pd.DataFrame.from_dict([{'attraction' : f'{att}', 'category': category,'subcategory': subcategory,'date': int(date), 'avgTa': float(avgTa), 'sumRn': float(sumRn),'sumSsHr':float(sumSsHr)}])
        pred = model.predict(X_test)
        if pred == 1:
            rec_list.append(att)
        
    return render_template('after.html', data=rec_list)
    
if __name__ == "__main__":
  app.run()

