#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import yaml
import os


def load_templates_from_dir(dir_path):
    template_list = list()
    # Search .yaml file in give directory
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if not filename.endswith(".yaml"):
                continue
            template_file_path = os.path.join(root, filename)
            with codecs.open(template_file_path, "r", encoding="utf-8") as template_file:
                # There can be multiple template in a single file. Read all templates in a single file.
                templates_in_single_file = yaml.load_all(template_file, Loader=yaml.FullLoader)
                for template_content in templates_in_single_file:
                    # Template_content could be None. Skip the None.
                    if template_content is None:
                        continue
                    template_list.append(template_content)
    return template_list


def load_templates_from_file(file_path: str):
    templates_list = list()
    with codecs.open(file_path, "r", encoding="utf-8") as template_file:
        templates_in_file = yaml.load_all(template_file, Loader=yaml.FullLoader)
        for template_content in templates_in_file:
            if template_content is None:
                continue
            templates_list.append(template_content)
    return templates_list


def load_templates_from_string(template_string: str):
    templates_list = list()
    templates_in_string = yaml.load_all(template_string, Loader=yaml.FullLoader)
    for template_content in templates_in_string:
        if template_content is None:
            continue
        templates_list.append(template_content)
    return templates_list
