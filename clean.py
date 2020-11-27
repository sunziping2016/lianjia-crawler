#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('raw.csv')
    data = data.drop_duplicates()
    data = data.sort_values(by=['district', 'subdistrict', 'page'])
    info = data['info'].str.extract(
        r'^\s*(\d+)室(\d+)厅\s*\|'
        r'\s*([0-9.]+)平米\s*\|'
        r'\s*([东南西北 ]+|暂无数据)\s*\|'
        r'\s*(精装|简装|毛坯|其他)\s*\|'
        r'\s*(中楼层|低楼层|高楼层|上叠|下叠|地下室|(?:\d+)层)(?:\(共(\d+)层\))?\s*\|'
        r'\s*(?:(\d+)年建\s*\|)?'
        r'\s*(板楼|塔楼|板塔结合|平房|暂无数据)'
        r'\s*(?:\|\s*(联排别墅|独栋别墅|双拼别墅|叠拼别墅|暂无数据别墅)\s*)?$'
    )
    info_error = data['info'][info[0].isnull()]
    if info_error.size > 0:
        print('Info field parse error:')
        print(info_error)
    position = data['position'].str.extract(r'^\s*(.*?)\s*-\s*(.*?)\s*$')
    position_error = data['position'][position[0].isnull()]
    if position_error.size > 0:
        print('Position field parse error:')
        print(position_error)
    follow = data['follow'].str.extract(
        r'^(\d+)人关注\s*/\s*'
        r'(\d+天以前|\d+个月以前|一年前|刚刚)发布$'
    )
    follow_error = data['follow'][follow[0].isnull()]
    if follow_error.size > 0:
        print('Follow field parse error:')
        print(follow_error)
    total_price = data['total price'].str.extract(r'^([0-9.]+)万$')
    total_price_error = data['total price'][total_price[0].isnull()]
    if total_price_error.size > 0:
        print('Total price field parse error:')
        print(total_price_error)
    unit_price = data['unit price'].str.extract(r'^单价(\d+)元/平米$')
    unit_price_error = data['unit price'][unit_price[0].isnull()]
    if unit_price_error.size > 0:
        print('Unit price field parse error:')
        print(unit_price_error)
    title_tag = data['title tag'].map(json.loads).map(lambda x: '|'.join(x))
    tag = data['tag'].map(json.loads).map(lambda x: '|'.join(x))
    data = pd.concat([data[['district', 'subdistrict', 'page', 'link', 'title']],
                      title_tag, info, position, follow, tag, total_price, unit_price], axis=1)
    data.columns = [
        '区', '镇', '页数', '链接', '标题',
        '标题标签',
        '室', '厅', '面积（平米）', '朝向', '装修', '层数', '总层数', '建造年份', '楼型', '别墅模型',
        '小区', '区（校验）',
        '关注人数', '发布时间',
        '标签',
        '总价（万）', '单价（元/平米）'
    ]
    data.to_csv('result.csv', index=False)
