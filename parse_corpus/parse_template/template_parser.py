#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import codecs
from collections import deque
import re


class IstioTemplatesParser(object):
    pass


class IstioTemplateFuzzyParser(object):
    def __init__(self):
        self.__api_version_tag = "apiVersion"
        self.__line_break_tag = '\n'
        self.__colon_tag = ":"
        self.__yaml_separator_tag = "---"
        self.__eof_tag = "EOF"

    def parse(self, raw_text: str) -> list:
        parsed_templates = list()
        for (begin, end) in self.parse_position_index(raw_text):
            parsed_templates.append(raw_text[begin:end])
        return parsed_templates

    def parse_position_index(self, raw_text) -> list:
        # coarse-grain sliced indexes
        # confirm how many potential yaml template in raw text
        api_version_positions = [(p.start(), p.end()) for p in re.finditer(self.__api_version_tag, raw_text)]

        api_version_slices = []
        num_api_versions = len(api_version_positions)
        if num_api_versions < 1:
            return []
        else:
            for i in range(num_api_versions - 1):
                api_version_slices.append((api_version_positions[i][0], api_version_positions[i + 1][0]))
        api_version_slices.append((api_version_positions[num_api_versions - 1][0], len(raw_text)))

        # fine-grain sliced end indexes
        possible_position_indexes = []
        # try to update the end position
        for api_version_start, api_version_end in api_version_slices:
            sliced_text = raw_text[api_version_start:api_version_end]
            line_break_positions = [(p.start(), p.end()) for p in re.finditer(self.__line_break_tag, sliced_text)]
            if len(line_break_positions) == 0:
                # no line break found, stop updating the end position
                break
            line_break_positions = [0] + [p[1] for p in line_break_positions] + [len(sliced_text)]

            line_break_slices = []
            for num_pos in range(len(line_break_positions) - 1):
                line_break_slices.append((line_break_positions[num_pos], line_break_positions[num_pos + 1]))

            min_line_break_index = len(sliced_text)
            for line_start, line_end in line_break_slices:
                line_text = sliced_text[line_start: line_end]
                if not line_text.strip():
                    min_line_break_index = line_start
                    break

            min_eof_index = len(sliced_text)
            for line_start, line_end in line_break_slices:
                line_text = sliced_text[line_start: line_end]
                if line_text.startswith(self.__eof_tag):
                    min_eof_index = line_start
                    break

            separator_index = sliced_text.find(self.__yaml_separator_tag)
            min_separator_index = separator_index if separator_index >= 0 else len(sliced_text)

            slice_text_end_index = min(min_line_break_index, min_separator_index, min_eof_index)

            # find latest EOF
            possible_template = (sliced_text[:slice_text_end_index])

            try:
                parsed_result = yaml.load(possible_template, Loader=yaml.FullLoader)
                if type(parsed_result) is not dict:
                    continue
                possible_position_indexes.append((api_version_start, api_version_start + slice_text_end_index))
            except Exception:
                continue
        return possible_position_indexes
