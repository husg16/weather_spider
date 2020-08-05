import time
from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    execute(["scrapy", "crawl", "weather15"])
