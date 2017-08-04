"""
Load a brief+editorial from a file
"""

import pdb
import os,json

scraping_data_path = './codematch/data/'

class Loader():
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.path = scraping_data_path + self.dir_name

    def load_all(self):
        for filename in os.listdir(self.path):
            if "already_processed" not in filename:
                ff = self.path + filename
                if not os.path.exists(ff):
                    print("File "+str(ff)+" doesn't exist")
                else:
                    with open(ff,"r") as file:
                        try:
                            txt = ''.join(file.readlines())
                            #pdb.set_trace()
                            js = json.loads(txt)
                            yield js
                        except:
                            print("Failed to open or process "+str(ff))
                            continue

class CodechefLoader(Loader):
    def __init__(self):
        Loader.__init__(self, 'codechef/')


"""
Return a dict of <title, full_text_brief, full_text_editorial>
"""
class SimpleLoader(Loader):
    def __init__(self, dir_name):
        Loader.__init__(self, dir_name)

    def load_all(self):
        for js in Loader.load_all(self):
            fields = 'brief prompt input constraints explanation'.split()
            jsb = js['brief']
            brief_txt = ''
            for field in fields:
                if field in jsb:
                    brief_txt += jsb[field].replace("\n", "")
            fields = 'problem_summary prerequisites difficulty explanation'.split()
            jse = js['editorial']
            editorial_txt = ''
            for field in fields:
                if field in jse:
                    editorial_txt += jse[field].replace("\n", "")

            d = { "title":js['title'] , "brief":brief_txt , "editorial":editorial_txt}

            yield d
