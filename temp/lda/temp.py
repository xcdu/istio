#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def clean_text(text):
  text = text.replace('\n', " ")
  text = re.sub(r"-", " ", text)
  text = re.sub(r"\d+/\d+/\d+", "", text)
  text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text)
  text = re.sub(r"[\w]+@[\.\w]+", "", text)
  text = re.sub(
    r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", text)
  pure_text = ''
  for letter in text:
    if letter.isalpha() or letter == ' ':
      pure_text += letter
  text = ' '.join(word for word in pure_text.split() if len(word) > 1)
  return text
