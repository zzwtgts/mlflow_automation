# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""
import library as lb
import parameters as ps

app = lb.Flask(__name__)

model = lb.load(open('../data/'+ps.JOBLIB_FILENAME,'rb'))

@app.route('/', methods = ['POST'])

def predict_proba():

    json_ = lb.request.get_json()

    X = lb.pd.read_json(json_, orient='records')

    return lb.jsonify({'prediction_probability': str(model.predict_proba(X))})

if __name__ == '__main__':

    app.run(host=ps.IP_ADDRESS, debug=True, port=ps.PORT)
