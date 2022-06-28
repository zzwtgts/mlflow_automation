# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

import library as lb
import parameters as ps

def output_format(FILENAME, df_one_hot, df_feature_engineering, df_constant_features, df_missing_value_features, df_iv_features, df_psi_features, df_correlation_features, feature_importances, features, ks_train, auc_train, ks_test, auc_test, psi_train_test, df_single_variable_analysis):

    with lb.pd.ExcelWriter('../data/'+ps.OUTPUT_FILENAME) as writer:

        df_one_hot.to_excel(writer, sheet_name = 'one_hot_features')

        df_feature_engineering.to_excel(writer, sheet_name = 'feature_engineering_features')

        df_constant_features.to_excel(writer, sheet_name = 'constant_features_drop')

        df_missing_value_features.to_excel(writer, sheet_name = 'missing_value_features_drop')

        df_iv_features.to_excel(writer, sheet_name = 'iv_features_drop')

        df_psi_features.to_excel(writer, sheet_name = 'psi_features_drop')

        df_correlation_features.to_excel(writer, sheet_name = 'correlation_features_drop')

        df_feature_importances =  lb.pd.DataFrame({'feature': features, 'feature_importance': feature_importances})

        df_feature_importances.to_excel(writer, sheet_name = 'feature_importances')

        df_ks_auc_psi =  lb.pd.DataFrame({'metrics': ['ks_train', 'auc_train', 'ks_test', 'auc_test', 'psi_train_test'], 'value': [ks_train, auc_train, ks_test, auc_test, psi_train_test]})

        df_ks_auc_psi.to_excel(writer, sheet_name = 'ks_auc_psi')

        df_single_variable_analysis.to_excel(writer, sheet_name = 'single_variable_analysis')
