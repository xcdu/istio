#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os

from default_config import RAW_FORUM_DIR


def load_raw_forum_data(path=None):
    if path is None:
        path = os.path.join(RAW_FORUM_DIR, "raw_forum.csv")
    raw_forum = pd.read_csv(path)
    return raw_forum
