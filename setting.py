import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class DictRstParser:
    """
    一个类，实际是具有【获取html】功能的数据类型
    """
    def get_content(self, soup_file, key_word):
        """
        从传入的Bs4 html_content 中读取指定标签内容 key_word
        :param soup_file: 经由BeautifulSoup4解析后的html文本
        :param key_word: 在soup_file中搜索的tag 关键词
        :return:
        """
        # soup.select 方法
        rst = soup_file.select(key_word)
        # 按3种情况处理
        if len(rst) == 0:
            return None
        elif len(rst) == 1:
            return rst[0].get_text().replace("\xa0", " ").strip()
        else:
            return '\n'.join([e.get_text() for e in rst])

    def __init__(self, word_str):
        """
        web解析器
        :param word_str:传入单词
        """
        # 解析器.词典链接
        self.dict_link = f'https://cn.bing.com/dict/search?q={word_str}'
        # 返回链接对应的html文件
        self.html_file = requests.get(self.dict_link).text
        # 用Bs4库对 返回的html文件作解析，存为  解析器.soup
        self.soup = BeautifulSoup(self.html_file, 'html.parser')

        # 从解析器.soup 中搜索 词典area 下的所有div
        self.related_soups = self.soup.select('div.lf_area >div')

        # 用字典形式存储所需调用的数据（原因是作者发现使用get_content函数时，重复的代码部分超过3次）
        self.input_list = {
            'word': 'div#headword',
            # 'eng_pr':'div.hd_pr',
            'ame_pr': 'div.hd_prUS',
            # 'tongyi': 'div.wd_div',
            # 'fushu': 'div.hd_div1',
            # 'defination': 'div.qdef > ul >li',
        }

        # 创建新字典
        self.output_dict = {}

        # 按 input_list 需求 调用 get_content  函数
        for key, value in self.input_list.items():
            # 在特定Bs4 html_content内，在第一个div中寻找 input_list字典里的每个key键对应的指定标签值。
            self.output_dict[key] = self.get_content(self.related_soups[0], value)
        # 在特定Bs4 html_content内，在第二个div中寻找对应例句
        self.output_dict['sentences'] = self.get_content(self.related_soups[1], 'div#sentenceSeg')
