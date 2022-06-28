# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""

import library as lb


def python_sql(start_date, end_date):

    inbound_sql = "select A.data_date, A.warehouse_name, A.winit_order_no, A.order_type, A.merchandise_serno, A.package_serno, A.locator_serno, A.shelf_qty, A.manage_mode, A.product_class, A.product_volume, A.package_level, A.second_abc_of_recommend from bi_dw.base_shelf_merchandise_locator as A where TO_CHAR(A.data_date, 'YYYY-MM-DD') >= '" + str(
        start_date) + "' and TO_CHAR(A.data_date, 'YYYY-MM-DD') < '" + str(end_date) + "' and A.warehouse_name = '" + str(warehouse) + "' and A.order_type != 'RETURN'"

    connection = pg.connect(host='10.110.32.162',  port='8000', dbname='winit_dws', user='bi_public_dev', password='Winit*2018')

    df = pd.read_sql_query(inbound_sql, connection)

    return df
