

class AssembleCodechefPipeline(object):
    def __init__(self):
        self.briefs = {}
        self.editorials = {}
        self.log_file = open("./data/codechef/_already_processed","a")

    def process_item(self, item, spider):
        if type(item) == EditorialItem:
            self.editorials[item.title] = item
        if type(item) == BriefItem:
            self.briefs[item.title] = item
        if item.title in self.briefs and item.title in self.editorials:
            # Complete, store it!
            print("DONE WITH " + str(item.title))
            self.write_file(item.title)
            spider.already_processed.add(item.title)

    def write_item(self, title):
        br = self.briefs[title]
        ed = self.editorials[title]
        d = {"title":title, "editorial":ed, "brief":br}
        js = json.loads(d)
        if os.path.exists("./data/codechef/"+title):
            print(" WARNING: %s file already processed !!!!"%title)
        else:
            with open("./data/codechef/"+title,"w") as f:
                f.write(js)
            log_file.write(title + "\n")

    def close_spider(self, spider):
        self.log_file.close()
