import cv2


class PersonalVideo:
    def __init__(self, material_id, title, video_path, vendor_path, keywords, produced_time, hours, minutes, seconds,
                 copyright, mtype, format, brief, price, xml_formatted, video_play_path):
        self.material_id = material_id
        self.title = title
        self.video_path = video_path
        self.vendor_path = vendor_path
        self.keywords = keywords
        self.produced_time = produced_time
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.duration = self.get_video_duration(video_path)
        self.copyright = copyright
        self.mtype = mtype
        self.format = format
        self.brief = brief
        self.price = price
        self.xml_formatted = xml_formatted
        self.video_play_path = video_play_path

    @staticmethod
    def get_video_duration(file_path):
        cap = cv2.VideoCapture(file_path)
        return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

