import scrapy
import pdb
import json,os,re
import lxml.etree
import re

from codematch.items import EditorialItem, BriefItem

start='https://discuss.codechef.com/tags/editorial/?sort=active&page=3'

base_problem_url="https://www.codechef.com/problems/"
start_base = "https://discuss.codechef.com/tags/editorial/?sort=active&page="
starts = [start_base+str(i) for i in range(1,30)]
brief_api_url = "https://www.codechef.com/api/contests/PRACTICE/problems/"

cols = ['\033[95m','\033[94m','\033[92m','\033[93m','\033[91m']
endcol = '\033[0m'
def pprint(s, lvl=-1):
    if lvl == -1:
        print(s)
    else:
        print(cols[lvl%len(cols)] + s + endcol)

class CodechefSpider(scrapy.Spider):
    name = 'codechef'
    start_urls = starts

    def __init__(self, category=None, *args, **kwargs):
        #super(MySpider, self).__init__(*args, **kwargs)
        already_processed = set([])
        print("Loading already_processed list...")
        if os.path.exists("./data/codechef/_already_processed"):
            with open("./data/codechef/_already_processed", 'r') as f:
                for line in f:
                    already_processed.add(line)
        print(" ... Done, already have %d processed"%len(already_processed))
        self.already_processed = already_processed;
        self.num_total=0
        self.num_success=0

    def close(self, reason):
        print("\nSpider Closed (%d/%d)\n"%(self.num_success,self.num_total))

    def parse(self, response):
        url = response.url
        #pdb.set_trace()

        # this is a list of questions (or editorials)
        if "tags" in url and "question" not in url:
            print("\n\n LISTING PAGE \n")
            for ele in response.css('h2 > a'):
                title = ele.css('a ::text').extract_first()
                #pdb.set_trace()
                lnk_url = ele.css('a::attr(href)').extract_first()
                if '- Editorial' in title:
                    #yield {'title': title}
                    if lnk_url is not None:
                        lnk_url = response.urljoin(lnk_url)
                        yield scrapy.Request(lnk_url, callback=self.parse)


        # this is an editorial
        elif "tags" not in url and "question" in url:
            # Find name -> brief -> editorial_text.
            # I will need to fetch the html for the brief, so
            # I will need some delay mechanism/concurrency
            title = response.css('title::text').extract_first().strip()
            title = title.replace(" - CodeChef Discuss","")
            title = title.replace("-Editorial",'')
            title = title.replace(" - Editorial",'')
            title = title.replace("- Editorial",'').strip()
            if title in self.already_processed:
                print(title+" has already been processed, skipping")
                return
            print("\n\n EDITORIAL -- %s\n"%title)

            body = response.css('.question-body')

            ## Yield request to get brief
            """brief_link = None
            links = body.css('a')
            for lnk in links:
                if "practice" in lnk.extract().lower():
                    brief_link = lnk.css('::attr(href)').extract_first()
                    break
            # Follow the link to the brief
            if brief_link is not None:
                pprint (brief_link,3)
                yield response.follow(brief_link, callback=self.parse)
            else:
                brief_link = base_problem_url + title
                pprint("Failed to find brief link for %s, so now looking for %s !!!!"%(title,brief_link),4)
                yield response.follow(brief_link,callback=self.parse)"""
            yield response.follow(brief_api_url + title, callback=self.parse)

            # Register editorial attribs
            segments = {'title':title}

            # State-machine approach to parsing the body
            state="_start"
            for node in body.xpath('./*'):
                if node.css('h1'):
                    hh = node.css('h1').extract_first()
                    if "DIFFI" in hh: state="difficulty"
                    elif "PROBLEM" in hh: state="problem_summary"
                    elif "PREREQ" in hh: state="preqrequisites"
                    elif "EXPLAN" in hh: state="explanation"
                    elif "SOLUT" in hh: state="solution_links"
                elif state != "solution_links" and node.css('p'):
                    txt = map(str.strip, node.css('p::text').extract())
                    txt = ' '.join(txt).strip()
                    """txt =txt.replace("<b>","").replace("</b>","").replace("<li>","").replace("</li>","").replace("<\/li>","").replace("<\/b>","")
                    txt = re.sub(txt,"\<img>.*\<\/img\>","")
                    txt = re.sub(txt,"\<.?img [^\>]\>","")"""
                    if state in segments:
                        segments[state] += " " + txt
                    elif state != "_start":
                        segments[state] = txt
                    elif state == "solution_links":
                        pass
                    #lnks = .css('::attr(href)').extract()


            item = EditorialItem()
            for (k,v) in segments.items():
                item[k]=v
            yield item


        # This is a brief
        elif "tags" not in url and "problems" in url:
            j = json.loads(response.text)
            if "problem_code" not in j:
                pprint("NO PROBLEM CODE\n",1)
                print(str(j))
            title = str(j["problem_code"])
            full_title = j["problem_name"]
            if title in self.already_processed:
                print(title+" has already been processed, skipping")
                return
            print("\n\n BRIEF ITEM -- %s\n"%title)
            self.num_total += 1

            ss = j['body']
            ss =ss.replace("<b>","").replace("</b>","").replace("<li>","").replace("</li>","").replace("<\/li>","").replace("<\/b>","").replace("<br>","")

            root = lxml.etree.fromstring("<html>" + ss + "</html>")

            segments = {'title':title, 'full_title':full_title}
            state="prompt"

            ss = ''.join(root.xpath("//text()"))
            ss = ss.split('\n')

            for s in ss:
                if "All submissions for this problem are " in s or \
                   "Read problems statements in " in s or \
                   "Read problem statements in" in s:
                   continue
                if "Input" in s and len(s) <= 9:
                    state='input'
                if 'Output' in s and len(s) <= 9:
                    state='output'
                if 'Constraints' in s and len(s) <= 13:
                    state='constraints'
                if 'Example' in s and len(s) <= 10:
                    state='_ignore'
                if 'Explanation' in s and len(s) <= 14:
                    state='explanation'
                elif state != '_ignore' and len(s) > 1:
                    if state in segments:
                        # Add a space if needed
                        if len(segments[state]) > 1 and segments[state][-1] != '\n' and s[0] != '\n':
                            segments[state] += '\n' + s
                        else:
                            segments[state] += s
                    else:
                        segments[state] = s

            item = BriefItem()
            for (k,v) in segments.items():
                item[k]=v
            yield item


        else:
            print("Unknown page.")
