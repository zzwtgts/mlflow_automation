# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

import library as lb
import parameters as ps
import feature_selection as fs

def model_training_validation(X_train, y_train, X_test, y_test):

    estimator = lb.XGBClassifier(
        objective= 'binary:logistic',
        use_label_encoder=False,
        eval_metric='auc',
        importance_type = 'gain'
    )

    parameters = {
        'max_depth': ps.MAX_DEPTH,
        'n_estimators': ps.N_ESTIMATORS,
        'learning_rate': ps.LEARNING_RATE
    }

    grid_search = lb.GridSearchCV(
        estimator=estimator,
        param_grid=parameters,
        scoring = 'roc_auc',
        n_jobs = -1,
        cv = 10,
        verbose=3
    )

    grid_search.fit(X_train, y_train)

    lb.mf.sklearn.log_model(grid_search, 'model')

    lb.dump(grid_search, open('../data/'+ps.JOBLIB_FILENAME,'wb'))

    y_train_pred = grid_search.predict(X_train)

    y_test_pred = grid_search.predict(X_test)

    y_train_pred_list = list(grid_search.predict_proba(X_train))

    y_test_pred_list = list(grid_search.predict_proba(X_test))

    y_train_pred_proba = lb.np.array([pred[1] for pred in y_train_pred_list])

    y_test_pred_proba = lb.np.array([pred[1] for pred in y_test_pred_list])

    ks_train, auc_train = ks_auc(y_train, y_train_pred)

    ks_test, auc_test = ks_auc(y_test, y_test_pred)

    psi_train_test  = lb.np.mean(fs.psi(y_train_pred_proba, y_test_pred_proba, ps.BIN_NUM, mode = 'quantile'))
   
    return (grid_search.best_estimator_, grid_search.best_estimator_.feature_importances_, list(X_train.columns.values), ks_train, auc_train, ks_test, auc_test, psi_train_test)



def ks_auc(y, y_pred):

    df_compare = lb.pd.DataFrame({'y':y, 'y_pred':y_pred})

    ks_value = lb.stats.ks_2samp(df_compare[df_compare['y']==0]['y_pred'], df_compare[df_compare['y']==1]['y_pred'])

    auc_value = lb.roc_auc_score(y, y_pred)

    return  (ks_value, auc_value)


def single_variable_analysis(df, feature, target, bin_num):

    if df[feature].nunique() <= 5:

        d1 = df.groupby(by=feature, as_index=True)

        data = lb.pd.DataFrame()

        data['bad'] = d1[target].sum()

        data['d_b'] = data['bad'] / data['bad'].sum()

        df_output = lb.pd.DataFrame(list(zip([feature]*data['d_b'].shape[0], data['d_b'].index, list(data['d_b'].values))), columns =['feature', 'range', 'mean'])

        return (df_output)

    else:
  
         bins = lb.pd.qcut(df[feature], bin_num)

         df_series = df.groupby(bins)[target].agg(['mean'])

         df_output = lb.pd.DataFrame(list(zip([feature]*df_series.shape[0], df_series.index, (list(df_series.values.flatten())))), columns =['feature', 'range', 'mean'])

         return (df_output)    


def single_variable_output(df, target):

    columns_list = df.columns.tolist()

    df_row_merged =  lb.pd.DataFrame(columns = ['feature', 'range', 'mean'])

    for column in columns_list:

        if column != target:

            df_b = single_variable_analysis(df, column, target, ps.BIN_NUM)
           
            df_row_merged = lb.pd.concat([df_row_merged, df_b], ignore_index=True)

    return (df_row_merged)



def read_data(df, target, test_size):

    Y = df[target]

    X = df.drop([target], axis = 1)

    X_train, X_test, y_train, y_test = lb.train_test_split(X, Y, test_size=test_size)

    return (X_train, X_test, y_train, y_test)
