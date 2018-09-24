#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:51:41 2018

@author: xingyang
"""

import pandas as pd 
import numpy as np

data = pd.read_excel('Book1.xlsx').iloc[3:]
data.columns = ['high', 'low', 'close']
data.index = pd.to_datetime(data.index, format = '%Y-%m-%d %H:%m:%s')

'''
LLT
'''

close = data.close

def calc_one_llt(price, price_1, price_2, llt_1, llt_2, span = 60):
    alpha = 2 / (1 + span)
    llt = (alpha - (alpha ** 2) * 0.25) * price + (alpha ** 2) * 0.5 * price_1 \
          - (alpha - (alpha ** 2) * 0.75) * price_2 + (1 - alpha) * 2 * llt_1 \
          - (1 - alpha) ** 2 * llt_2
    return llt

def calc_llt(close, span = 60):
    llt = close.copy()
    for i in range(3, len(close)):
        llt_1 = llt.iloc[i-1]
        llt_2 = llt.iloc[i-2]
        price = close.iloc[i]
        price_1 = close.iloc[i-1]
        price_2 = close.iloc[i-2]
        llt.iloc[i] = calc_one_llt(price, price_1, price_2, llt_1, llt_2, span = span)
    return llt

llt = calc_llt(close, span = 60)
idct = llt.diff(1)
idct = (idct.where(idct > 0).isnull() * -1) + 1

(close / close.iloc[0]).tail(200).plot()
(close.pct_change() * idct.shift(1) + 1).cumprod().tail(200).plot()

llt.tail(60).plot()
close.tail(60).plot()