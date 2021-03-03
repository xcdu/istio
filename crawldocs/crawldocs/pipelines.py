# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json
import os


class SerializationPipeline:
  def __init__(self):
    self.save_dir = "../.raw_data/istio_docs"
    if not os.path.exists(self.save_dir):
      os.makedirs(os.path.abspath(self.save_dir))

  def process_item(self, item, spider):
    page_indexer = item["page_indexer"]
    save_file_path = os.path.join(self.save_dir, page_indexer)
    save_file = codecs.open(save_file_path, "w", encoding="utf-8")
    save_file.write(json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n")
    save_file.close()
    return item
