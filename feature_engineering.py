# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""


import library as lb


'''
https://linuxtut.com/en/6b5204899ea61366d494/
https://featuretools.alteryx.com/en/stable/generated/featuretools.dfs.html
'''


def feature_tools(df, entity_name, make_index_true, index_name, trans_primitives_list, agg_primitives_list, max_depth_num):

    es = lb.ft.EntitySet()

    es = es.entity_from_dataframe(entity_id=entity_name,
                              dataframe=df,
                              make_index=make_index_true,
                              index=index_name)

    feature_matrix, feature_defs = lb.ft.dfs(entityset=es,
                                      target_entity=entity_name,
                                      trans_primitives=trans_primitives_list,
                                      agg_primitives=agg_primitives_list,
                                      max_depth=max_depth_num)

    df_feature_engineering = lb.pd.DataFrame (list(feature_matrix.columns), columns = ['feature_engineering_features'])

    return (feature_matrix, df_feature_engineering)
