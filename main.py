# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

import library as lb
import parameters as ps
import visulization as vz
import data_preprocess as dp
import feature_engineering as fe
import feature_selection as fs
import model as ml
import output as op

if __name__ == '__main__':

    with lb.mf.start_run():

        df = lb.pd.read_csv('../data/'+ps.FILENAME)

        lb.mf.log_artifact('../data/'+ps.FILENAME)

        df, df_one_hot = dp.one_hot_encode(df)

        df, df_feature_engineering = fe.feature_tools(df, ps.ENTITY_NAME, ps.MAKE_INDEX_TRUE, ps.INDEX_NAME, ps.TRANS_PRIMITIVES_LIST, ps.AGG_PRIMITIVES_LIST, ps.MAX_DEPTH_NUM)

        df, df_constant_features = fs.constant_feature_drop(df)

        df, df_missing_value_features = fs.missing_value_feature_drop(df, ps.MISSING_THRESHOLD)

        df, df_iv_features = fs.iv_features_drop(df, ps.TARGET, ps.IV_THRESHOLD)

        df, df_psi_features = fs.psi_features_drop(df, ps.TARGET, ps.PSI_SPLIT, ps.PSI_THRESHOLD)

        df, df_correlation_features = fs.correlation_features_drop(df, ps.TARGET, ps.CORRELATION_THRESHOLD)

        lb.mf.log_param('CORRELATION_THRESHOLD', ps.CORRELATION_THRESHOLD)

        vz.pair_plot(df)

        X_train, X_test, y_train, y_test = ml.read_data(df, ps.TARGET, ps.TRAINING_VALIDATION_SPLIT)

        best_estimator, feature_importances, features, ks_train, auc_train, ks_test, auc_test, psi_train_test = ml.model_training_validation(X_train, y_train, X_test, y_test)

      #  lb.mf.log_metric('ks_test', ks_test)

        lb.mf.log_metric('psi_train_test', psi_train_test)

        df_single_variable_analysis = ml.single_variable_output(df,  ps.TARGET)

        op.output_format(ps.OUTPUT_FILENAME, df_one_hot, df_feature_engineering, df_constant_features, df_missing_value_features, df_iv_features, df_psi_features, df_correlation_features, feature_importances, features, ks_train, auc_train, ks_test, auc_test, psi_train_test, df_single_variable_analysis)
