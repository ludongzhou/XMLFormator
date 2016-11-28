import glob
import json
import logging
import os

import xmltodict
from .JsonFormator import JSONFormator


class xml2Json:
    def xml2json(self, xml_path, dest_path, xml_attribs=True):
        with open(xml_path, "rb") as f:  # notice the "rb" mode
            d = xmltodict.parse(f, xml_attribs=xml_attribs, encoding='utf-8', attr_prefix='')
            if not d:
                logging.error("xml2Json. xmltodict failed for file: %s. Exit" % xml_path)
                return 1

            string = json.dumps(d, indent=4, ensure_ascii=False)
            if not string:
                logging.error("xml2Json. json dumps failed for file: %s. Exit" % xml_path)
                return 2

            with open(dest_path, 'w+', encoding='utf-8') as outFile:
                outFile.write(string)
            return 0

    # 将一个文件夹下的xml文件转成json文件, 不会递归的遍历文件夹, 只是在顶层目录查找
    def batch_transform(self, xml_folder, json_folder):
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)
            logging.info("xml2Json. Create jsonFolder: %s\n" % json_folder)

        xml_files = glob.glob(xml_folder + "/*.xml")
        if len(xml_files) == 0:
            logging.warning("xml2Json. can't find any xml file in %s to transform. Exit\n" % xml_folder)
            return 0

        for xml_file in xml_files:
            dest_path = json_folder + '/' + xml_file.split('/')[-1][:-4] + '.json'
            self.xml2json(xml_file, dest_path)

        json_formator = JSONFormator()
        json_formator.format(json_folder)
