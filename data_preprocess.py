# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

import library as lb





def missing_columns_preprocess(df, continous_type, category_type):

    missing_columns_list = df.columns[df.isnull().any()].tolist()

    for column in missing_columns_list:

        column_data_type = df.dtypes[column]

        if column_data_type in ['float64']:

           if continous_type == 'mean':

               df[column].fillna((df[column].mean()), inplace=True)

           elif continous_type == 'median':

               df[column].fillna((df[column].median()), inplace=True)

           else:

               pass 

        elif column_data_type in ['int64', 'bool', 'category']:

           if category_type == 'most_frequent':

               df[column].fillna((df[column].mode()[0]), inplace=True)


           else:

               pass

    return (df)




def normalization_standardization(df, normalization_standardization_type):

    columns_list = df.columns.tolist()
 
    for column in columns_list:

        column_data_type = df.dtypes[column]
        
        if column_data_type in ['float64', 'int64']:

            if normalization_standardization_type == 'normalization':

                print (column)
 
                df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())

            elif normalization_standardization_type == 'standardization':

                df[column] = (df[column] - df[column].mean()) / df[column].std()

    return (df)

                  
def one_hot_encode(df):

    columns_list = df.columns.tolist()

    one_hot_column_list = []

    for column in columns_list:

        column_data_type = df.dtypes[column]

        if column_data_type in ['object']:

                dummy_column = lb.pd.get_dummies(df[column], prefix = column)              

                df = lb.pd.merge(left=df, right=dummy_column, left_index=True,right_index=True)

                df = df.drop([column], axis = 1)

                one_hot_column_list.append(column)

    df_one_hot = lb.pd.DataFrame (one_hot_column_list, columns = ['one_hot_features'])

    return (df, df_one_hot)



def sample_imbalance(df):

    ###upsampling, downsampling and SMOTE do not work well)

    pass

    return (df)
