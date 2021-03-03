#!/usr/bin/env python
# -*- coding: utf-8 -*-
from preprocess_corpus.preprocess_forum import load_forum_dataframe


def prepare_input():
    df = load_forum_dataframe()
    df = df.loc[:, ["processed_text", "processed_template"]]
    df = df.loc[df["processed_text"].notnull() & df["processed_template"].notnull()]
    return df


if __name__ == '__main__':
    prepare_input()
