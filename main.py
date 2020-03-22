import configparser
cfg = configparser.ConfigParser()
cfg.read('pand0ra.conf')

crawled=[]#记录爬取过的URL
class Do:
    def __init__(self):
        print('1')
    def speak(self,dd):
        print(dd)
    def __del__(self):
        print('2')

a=Do()
