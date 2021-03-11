#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import pandas as pd
import yaml
from parse_corpus.parse_template.template_parser import IstioTemplateFuzzyParser
from parse_corpus.parse_template.template_converter import convert_from_yaml_to_prefixed
from parse_corpus.parse_template.template_converter import convert_from_prefixed_to_dataframe
from parse_corpus.parse_template.template_converter import convert_from_dataframe_to_json
from components.nlp_preprocess.feature import SpacyFeature
from components.nlp_preprocess.feature import BertFeature
from components.nlp_preprocess.preprocessor import PipelinePreprocessor
# from parse_corpus.parse_template.template_converter import TEMPLATE_PREFIX_DELIMITER
from default_config import PREPROCESSED_CORPUS_FORUM_DIR


def format_forum(forum_dataframe: pd.DataFrame):
    forum_dataframe = preprocess_forum_raw_text(forum_dataframe)
    forum_dataframe = preprocess_forum_template(forum_dataframe)
    save_forum_dataframe(forum_dataframe)


def preprocess_forum_raw_text(forum_dataframe: pd.DataFrame):
    forum_dataframe["processed_text"] = forum_dataframe["raw_text"].apply(__preprocess_forum_raw_text)
    return forum_dataframe


def __preprocess_forum_raw_text(text):
    # TODO(xcdu): the input format of nlp pipeline preprocessor requires array. It should accept str format.
    if text is np.nan:
        return np.nan
    preprocessor = PipelinePreprocessor()
    preprocessor.set_features([SpacyFeature, BertFeature])
    text = preprocessor.feature_process([text])
    # print(text)
    return text


def preprocess_forum_template(forum_dataframe: pd.DataFrame):
    forum_dataframe["template"] = forum_dataframe["template"].apply(__forum_extract_template)
    forum_dataframe = __flatten_forum_templates(forum_dataframe)
    forum_dataframe["processed_template"] = forum_dataframe["template"].apply(__preprocess_forum_template)
    return forum_dataframe


def __forum_extract_template(text) -> str:
    if text is np.nan:
        return np.nan
    parser = IstioTemplateFuzzyParser()
    templates = parser.parse(text)
    if not templates or len(templates) == 0:
        return np.nan
    templates = [yaml.load(template, Loader=yaml.SafeLoader) for template in templates]
    for i in range(len(templates)):
        template = templates[i]
        prefixed_template = convert_from_yaml_to_prefixed(template)
        dataframe_template = convert_from_prefixed_to_dataframe(prefixed_template)
        json_template = convert_from_dataframe_to_json(dataframe_template)
        templates[i] = json_template
    return templates


def __flatten_forum_templates(forum_dataframe: pd.DataFrame):
    new_columns = forum_dataframe.columns.copy()
    new_columns.insert(2, "template_id")
    new_dataframe = pd.DataFrame(columns=forum_dataframe.columns)
    row_cnt = 0
    for i, row in forum_dataframe.iterrows():
        if row["template"] is np.nan:
            new_dataframe.loc[row_cnt] = row.copy()
            new_dataframe.loc[row_cnt, "template_id"] = 0
            row_cnt += 1
        else:
            for j, template in enumerate(row["template"]):
                new_dataframe.loc[row_cnt] = row.copy()
                new_dataframe.loc[row_cnt, "template"] = template
                new_dataframe.loc[row_cnt, "template_id"] = j
                row_cnt += 1
    return new_dataframe


def __preprocess_forum_template(template):
    if template is np.nan:
        return np.nan
    template_dict = json.loads(template)
    template_prefixed_keys_list = []
    for template_key in template_dict["key"].values():
        template_prefixed_keys_list.append(template_key)
    return template_prefixed_keys_list


def save_forum_dataframe(df: pd.DataFrame, dir_path=PREPROCESSED_CORPUS_FORUM_DIR,
                         filename="preprocessed_forum.pickle"):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    df_save_path = os.path.join(dir_path, filename)
    df.to_pickle(df_save_path)


def load_forum_dataframe(dir_path=PREPROCESSED_CORPUS_FORUM_DIR, filename="preprocessed_forum.pickle") -> pd.DataFrame:
    df_load_path = os.path.join(dir_path, filename)
    return pd.read_pickle(df_load_path)
