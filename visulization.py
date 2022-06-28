# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 10:20:07 2022

@author: Zheng Zhu
"""


import library as lb 


def pair_plot(df): 

    pair_hist_scatter_figure = lb.sns.pairplot(df)

    lb.plt.savefig('../data/pair_hist_scatter.png')

    lb.plt.close()

    pair_corr_figure = lb.sns.heatmap(df.corr())

    lb.plt.savefig('../data/pair_corr.png')

    lb.plt.close()
