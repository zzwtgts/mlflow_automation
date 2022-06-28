# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

import library as lb
import parameters as ps


def constant_feature_drop(df):

   df = (df.loc[:, (df != df.iloc[0]).any()])

   df_constant_features = lb.pd.DataFrame(list((df.loc[:, (df == df.iloc[0]).all()]).columns), columns = ['constant_features_drop'])
  
   return (df, df_constant_features)


def missing_value_feature_drop(df, treshold):

   all_features_list = list(df.columns)

   df = df.dropna(thresh= (1.0-treshold)*len(df), axis=1)

   missing_value_features_list = [feature for feature in  all_features_list if feature not in list(df.columns)]

   df_missing_value_features = lb.pd.DataFrame(missing_value_features_list, columns = ['missing_value_features_drop'])

   return (df, df_missing_value_features)


def correlation_matrix(df):

    feature_corr=df.corr()

    return (feature_corr)


def correlation_features_drop(df, target, threshold):
  
    features_corr = correlation_matrix(df)

    features_drop_set = set()

    columns_list = df.columns.tolist()

    for column_1 in columns_list:

        for column_2 in columns_list:

            if column_1 != target and column_2 != target and column_1 != column_2:

                if abs(features_corr.loc[column_1, column_2]) > threshold:

                    iv_1 = calc_iv_single_feature(df, column_1, target, False)

                    iv_2 = calc_iv_single_feature(df, column_2, target, False)

                    features_drop_set.add(column_1 if iv_1 < iv_2 else column_2)

    df = df.drop(list(features_drop_set), axis = 1)

    df_correlation_features = lb.pd.DataFrame(list(features_drop_set), columns = ['correlation_features_drop'])

    return (df, df_correlation_features)  



def calc_iv_single_feature(df, feature, target, pr=False):

    d1 = df.groupby(by=feature, as_index=True)

    data = lb.pd.DataFrame()

    data['all'] = d1[target].count()

    data['bad'] = d1[target].sum()

    data['share'] = data['all'] / data['all'].sum()

    data['bad_rate'] = d1[target].mean()

    data['d_g'] = (data['all'] - data['bad']) / (data['all'] - data['bad']).sum()

    data['d_b'] = data['bad'] / data['bad'].sum()

    data['woe'] = lb.np.log(data['d_g'] / data['d_b'])

    data = data.replace({'woe': {lb.np.inf: 0, -lb.np.inf: 0}})

    data['iv'] = data['woe'] * (data['d_g'] - data['d_b'])

    data.insert(0, 'variable', feature)

    data.insert(1, 'value', data.index)

    data.index = range(len(data))

    iv = data['iv'].sum()

    if pr:

        print(data)

        print('IV = %s' % iv)

    return iv


def iv_features_drop(df, target, threshold):

    columns_list = df.columns.tolist()

    iv_features_list = [] 

    for column in columns_list:

        column_data_type = df.dtypes[column]

        if column != target:

           iv = calc_iv_single_feature(df, column, target, pr=False)

           if iv <= threshold:

               df = df.drop([column], axis = 1)

               iv_features_list.append(column)

    df_iv_features = lb.pd.DataFrame(iv_features_list, columns = ['iv_features_drop']) 

    return (df, df_iv_features) 


def psi(score_initial, score_new, num_bins = 10, mode = 'quantile'):
    
    eps = 1e-4

    if len(set(score_initial)) < num_bins + 1:

         num_bins = 1

    # Sort the data
    score_initial.sort()

    score_new.sort()
    
    # Prepare the bins
    min_val = min(min(score_initial), min(score_new))

    max_val = max(max(score_initial), max(score_new))

    if mode == 'fixed':

        bins = [min_val + (max_val - min_val)*(i)/num_bins for i in range(num_bins+1)]

    elif mode == 'quantile':

        bins = lb.pd.qcut(score_initial, q = num_bins, retbins = True)[1] # Create the quantiles based on the initial population

    else:

        raise ValueError(f"Mode \'{mode}\' not recognized. Your options are \'fixed\' and \'quantile\'")

    bins[0] = min_val - eps # Correct the lower boundary

    bins[-1] = max_val + eps # Correct the higher boundary
        
        
    # Bucketize the initial population and count the sample inside each bucket

    bins_initial = lb.pd.cut(score_initial, bins = bins, labels = range(1,num_bins+1))

    df_initial = lb.pd.DataFrame({'initial': score_initial, 'bin': bins_initial})

    grp_initial = df_initial.groupby('bin').count()

    grp_initial['percent_initial'] = grp_initial['initial'] / sum(grp_initial['initial'])
    
    # Bucketize the new population and count the sample inside each bucket
    bins_new = lb.pd.cut(score_new, bins = bins, labels = range(1,num_bins+1))

    df_new = lb.pd.DataFrame({'new': score_new, 'bin': bins_new})

    grp_new = df_new.groupby('bin').count()

    grp_new['percent_new'] = grp_new['new'] / sum(grp_new['new'])
    
    # Compare the bins to calculate PSI
    psi_df = grp_initial.join(grp_new, on = "bin", how = "inner")

    
    # Add a small value for when the percent is zero
    psi_df['percent_initial'] = psi_df['percent_initial'].apply(lambda x: eps if x == 0 else x)

    psi_df['percent_new'] = psi_df['percent_new'].apply(lambda x: eps if x == 0 else x)
    
    # Calculate the psi
    psi_df['psi'] = (psi_df['percent_initial'] - psi_df['percent_new']) * lb.np.log(psi_df['percent_initial'] / psi_df['percent_new'])
    
    # Return the psi values
    return psi_df['psi'].values

    '''
    example to use this function 
    for col in df.columns.tolist():

        csi_values = psi(df['age'].values, 1.01*(df['age'].values), mode = 'quantile')

        print (lb.np.mean(csi_values))
    '''


def psi_features_drop(df, target, time_threshold, cut_off_threshold):

    columns_list = df.columns.tolist()

    psi_features_list = []

    for column in columns_list:

        column_data_type = df.dtypes[column]

        if column != target:

           initial = lb.np.array(df.loc[:int(df.shape[0]*time_threshold), column].values)

           new = lb.np.array(df.loc[int(df.shape[0]*time_threshold):, column].values)

           psi_values_list = psi(initial, new, ps.BIN_NUM, mode = 'quantile')

           if lb.np.mean(psi_values_list) > cut_off_threshold:

               df = df.drop([column], axis = 1)

               psi_features_list.append(column)
    
    df_psi_features = lb.pd.DataFrame(psi_features_list, columns = ['psi_features_drop'])

    return (df, df_psi_features)
