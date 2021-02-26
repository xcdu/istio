#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import yaml
from queue import Queue


def recursive_items(dictionary):
    if dictionary is None:
        return
    for key, value in dictionary.items():
        if type(value) is dict:
            yield key, value
            yield from recursive_items(value)
        else:
            yield key, value


in_dir = "./test_templates"

in_filenames = [os.path.join(root, filename) for root, _, filenames in os.walk(in_dir) for filename in filenames]

contents_dict = dict()
keys = dict()
for filename in in_filenames:
    with codecs.open(filename, "r", encoding="utf-8") as in_file:
        data = yaml.load_all(in_file, Loader=yaml.FullLoader)
        if data is None:
            continue
        for y in data:
            contents_dict[filename] = y
            for k, v in recursive_items(y):
                # print(k, v)
                if k not in keys:
                    keys[k] = 0
                keys[k] += 1

keys = sorted(keys.items(), key=lambda x: x[1], reverse=True)

print(len(keys))
cntk_1 = 0
cntk_2 = 0
cnt = 0
cnt_1 = 0
cnt_2 = 0
for i in keys:
    cnt += i[1]
    if i[1] == 1:
        cntk_1 += 1
        cnt_1 += i[1]
    elif i[1] == 2:
        cntk_2 += 1
        cnt_2 += i[1]
    print(i)
print(cntk_1, cntk_2)
print(cnt_1, cnt_2, cnt)
