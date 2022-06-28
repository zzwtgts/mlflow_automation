# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 14:59:37 2022

@author: Zheng Zhu

https://towardsdatascience.com/deploy-a-machine-learning-model-using-flask-da580f84e60c
"""

import library as lb


url = 'http://127.0.0.1:8000/'

data = [[11160, 500, 5.87, 0.05, 0, 0, 0]]

df = lb.pd.DataFrame(data, columns=['person_income', 'loan_amnt', 'loan_int_rate', 'loan_percent_income', 'person_home_ownership_RENT', 'loan_grade_D', 'loan_grade_E'])

json_data = df.to_json(orient="records")

headers = {'Content-type': 'application/json'}

response = lb.requests.post(url, data=lb.json.dumps(json_data), headers=headers)

print(response.text)















