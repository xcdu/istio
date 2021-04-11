#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd
from default_config import RAW_FORUM_DIR
from istrec.prepare_data.forum.forum_helper_config import FORUM_INDEX_REMAPPING


def load_forum_corpus_from_dir(dir_path=RAW_FORUM_DIR, file_name="raw_forum.csv") -> pd.DataFrame:
    save_file_path = os.path.join(dir_path, file_name)
    dataframe = pd.read_csv(save_file_path)
    # load remapped index keys from config file
    select_and_rename_maps = FORUM_INDEX_REMAPPING
    dataframe = dataframe[select_and_rename_maps.keys()]
    dataframe = dataframe[list(select_and_rename_maps.keys())]
    dataframe = dataframe.rename(columns=select_and_rename_maps)
    return dataframe
