#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open("topicwords.txt", "r", encoding="utf-8") as in_file:
  content = in_file.readlines()

content = sorted(list(set(content)))
with open("topicwords-rd.txt", "w", encoding="utf-8") as out_file:
  out_file.writelines(content)



