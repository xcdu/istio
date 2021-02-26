#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from webpage_data_loader import load_raw_forum_data


def render_demo_page(page="index.html"):
    raw_form = load_raw_forum_data()

    return render_template(page)
