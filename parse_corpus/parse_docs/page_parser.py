#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
from lxml import etree
from queue import Queue
import logging


class IstioPageParser(object):
  def __init__(self):
    """
    Header slicing -> Context slicing
    """
    self.header_slice_tags = list([
      "h2", "h3", "h4", "h5"
    ])
    self.ignore_tag_names = list([
      "nav"
    ])

  def parse(self, page):
    if self.is_index_page(page):
      self._parse_index_page(page)
    else:
      self._parse_intro_page(page)

  @staticmethod
  def is_index_page(page):
    selector = etree.HTML(page.raw)
    has_section_index = selector.xpath("boolean(//*[@class='section-index'])")
    return has_section_index

  @staticmethod
  def __has_attr_value(node, name, attr, value):
    """
    Identify whether BeautifulSoup Tag has give name, attribute and
    attribute_value.
    :param node: Tag node
    :param name: Tag name
    :param attr: Tag attribute
    :param value: Tag attribute value
    :return: Boolean
    """
    if node is None:
      return False
    return node.name == name and node.has_attr(attr) and value in node.get(attr)

  def _parse_index_page(self, page):
    soup = BeautifulSoup(page.raw, features="lxml")
    content_list = list()
    current_content_list_pos = 0
    current_topic = page.headline
    slice_pos_topic_dict = dict({current_content_list_pos: current_topic})
    article_root = soup.findAll("article")[0]
    for child in article_root.children:
      # skip the navigation
      if child.name in self.ignore_tag_names:
        continue
      if self.__has_attr_value(child, "div", "class", "section-index"):
        for grandchild in child.children:
          if self.__has_attr_value(grandchild, "div", "class", "entry"):
            content_list.append(grandchild)
            grand_topic = grandchild.find_all("h5")
            if len(grand_topic) > 0:
              grand_topic = " ".join([s for s in grand_topic[0].strings])
            else:
              grand_topic = ""
            slice_pos_topic_dict[current_content_list_pos] = grand_topic
            current_content_list_pos += 1
          elif grandchild.name == "ul":
            for li in grandchild.children:
              content_list.append(li)
              grand_topic = grandchild.find_all("h5")
              if len(grand_topic) > 0:
                grand_topic = " ".join([s for s in grand_topic[0].strings])
              else:
                grand_topic = ""
              slice_pos_topic_dict[current_content_list_pos] = grand_topic
              current_content_list_pos += 1
        slice_pos_topic_dict[current_content_list_pos] = current_topic
      elif child.name in self.header_slice_tags:
        current_topic = child.text
        content_list.append(child)
        slice_pos_topic_dict[current_content_list_pos] = current_topic
        current_content_list_pos += 1
      else:
        content_list.append(child)
        current_content_list_pos += 1

    # handle link and templates
    links = dict()
    templates = dict()
    for i, content_node in enumerate(content_list):
      for hyperlink in content_node.find_all("a"):
        self._append_hyperlink(append_dict=links, slice_id=i,
                               hyperlink_tag=hyperlink)

      for template in content_node.find_all("code", "language-yaml"):
        if i not in templates:
          templates[i] = list()
        # print("TEMP {}:{}".format(i, template.text))
        templates[i].append(template.text)

    page.contents = [list(content_node.strings) for content_node in
                     content_list]
    page.slice_pos_topic_dict = slice_pos_topic_dict

    page.links = links
    page.templates = templates

  def _parse_intro_page(self, page):
    soup = BeautifulSoup(page.raw, features="lxml")
    content_list = list()
    current_content_list_pos = 0
    current_topic = page.headline
    slice_pos_topic_dict = dict({current_content_list_pos: current_topic})
    article_root = soup.findAll("article")[0]
    for child in article_root.children:
      if child.name in self.ignore_tag_names:
        continue
      if child.name in self.header_slice_tags:
        current_topic = child.text
        content_list.append(child)
        slice_pos_topic_dict[current_content_list_pos] = current_topic
        current_content_list_pos += 1
      else:
        content_list.append(child)
        current_content_list_pos += 1

    # handle link and templates
    contents = list()
    links = dict()
    templates = dict()
    for i, content_node in enumerate(content_list):
      # handle content
      if isinstance(content_node, NavigableString):
        contents.append([content_node.string])
      else:
        contents.append(list(content_node.strings))
        # handle hyperlink
        for hyperlink in content_node.find_all("a"):
          self._append_hyperlink(append_dict=links, slice_id=i,
                                 hyperlink_tag=hyperlink)

        # handle template
        for template in content_node.find_all("code", "language-yaml"):
          if i not in templates:
            templates[i] = list()
          templates[i].append(template.text)

    page.contents = contents
    page.slice_pos_topic_dict = slice_pos_topic_dict
    page.links = links
    page.templates = templates

  @staticmethod
  def _append_hyperlink(append_dict, slice_id, hyperlink_tag):
    href = hyperlink_tag["href"]
    domain_prefix = "/latest/docs"
    remove_prefix = "/latest/"
    if not href.startswith(domain_prefix):
      return
    if href.rfind("/#") > 0:
      result = href[len(remove_prefix):href.rfind("/#")]
    else:
      result = href[len(remove_prefix):]
    indexer = "$".join([s for s in result.split("/") if s])
    if slice_id not in append_dict:
      append_dict[slice_id] = dict()
    append_dict[slice_id][hyperlink_tag.text] = indexer
