import os
from lxml import etree
from ..DataSupplier.DataRepository import DataRepository
from ..utility.FileUtility import FileUtility
from ..Adaptor.AdaptorCenter import AdaptorCenter


class GeneratePersonalTask:
    def __init__(self):
        self.materials = DataRepository().get_data('personal_record')

    def generate_xml(self, personal_video):
        xml_string = "<?xml version='1.0'?>" \
                     "<Metadata VendorName='Personal' VendorPath='N/A' VideoPath='%s'>" \
                     "<Program>" \
                     "<Title><ProperTitle>%s</ProperTitle></Title>" \
                     "<Subject>" \
                     "<Keyword>%s</Keyword>" \
                     "</Subject>" \
                     "<Date>" \
                     "<ProducedDate>%s</ProducedDate>" \
                     "</Date>" \
                     "<Format>" \
                     "<StartingPoint>0</StartingPoint>" \
                     "<Duration>%s</Duration>" \
                     "<FileFormat>%s</FileFormat>" \
                     "</Format>" \
                     "<Description>" \
                     "<DescriptionofContent>%s</DescriptionofContent>" \
                     "</Description>" \
                     "</Program></Metadata>" %\
                     (personal_video.video_path, personal_video.title, personal_video.keywords,
                      personal_video.produced_time, personal_video.duration, personal_video.video_format,
                      personal_video.brief)
        return xml_string

    def run(self):
        upload_log_insert_sql = "insert into upload_log " \
                                "(vendor_name, upload_time, uploader_name, xml_upload_path, xml_trans_path," \
                                "video_upload_path, video_cut_path, frame_extract_path, vendor_path, video_price, " \
                                "video_copyright, video_play_path, material_id) values "
        material_update_sql = ""
        for material in self.materials:
            xml_string = self.generate_xml(material)
            xml_root = etree.fromstring(xml_string.encode("utf-8"))
            xml_string = etree.tostring(xml_root, encoding='utf-8', pretty_print=True, xml_declaration=True)
            xml_path = os.getcwd() + "/../../../personal_xml/" + material.title + '_' + str(material["duration"]) + '.xml'
            FileUtility().write_file(xml_path, xml_string)

            vendor_name = "Personal"
            xml_trans_path = os.getcwd() + "/../../../result/" + material.title + '_' + str(material.duration) + '_' + material.format
            video_cut_path = xml_trans_path
            frame_extract_path = xml_trans_path

            video_path = material.video_path
            vendor_path = material.vendor_path
            _copyright = material.copyright
            video_play_path = material.video_play_path
            price = material["price"] if material["price"] else 1
            material_id = material["id"]
            upload_log_insert_sql += "('%s', NOW(), 'Admin', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', %d),"\
                                     (vendor_name, xml_path, xml_trans_path, video_path, video_cut_path,
                                     frame_extract_path, vendor_path, price, _copyright, video_play_path, material_id)
            material_update_sql += "update material set xml_formated = 1 where id=%d;" % material_id
        FileUtility().flush()
        upload_log_insert_sql[-1] = ';'
        AdaptorCenter().get_adaptor('upload_log').run_sql(upload_log_insert_sql)
        AdaptorCenter().get_adaptor('tps').run_sql(material_update_sql)
