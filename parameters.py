# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

FILENAME = 'credit_risk_dataset.csv'

TARGET = 'loan_status' 

ENTITY_NAME = 'credit_risk'

MAKE_INDEX_TRUE = True

INDEX_NAME = 'id'

TRANS_PRIMITIVES_LIST = []

AGG_PRIMITIVES_LIST = []

MAX_DEPTH_NUM = 1

MISSING_THRESHOLD = 0.2 

IV_THRESHOLD = 0.1

PSI_SPLIT = 0.5

PSI_THRESHOLD = 0.2

CORRELATION_THRESHOLD = 0.8

TRAINING_VALIDATION_SPLIT = 0.4

MAX_DEPTH = range (2, 8, 2) 

N_ESTIMATORS = range(40, 200, 40) 

LEARNING_RATE = [0.02, 0.04]

BIN_NUM = 4

OUTPUT_FILENAME = 'output_results.xlsx' 

JOBLIB_FILENAME = 'model_grid_search.joblib'

IP_ADDRESS = '127.0.0.1'

PORT = 8000
