import requests
from bs4 import BeautifulSoup
import re


class DictRstParser:

    @staticmethod
    def get_content(soup_file, key_word):
        """从传入的html文件(p1)中查找标签(p2)并返回内容

        :param soup_file: 经由BeautifulSoup4解析后的html文本
        :param key_word: 待查找的tag.例如：’div#title‘
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
            # 原作使用的方法
            return '\n'.join([e.get_text() for e in rst])

    def __init__(self, word_str: str):
        """传入单词，查询其对应音标并存储

        :param word_str: 传入单词
        """
        # 解析器.词典链接
        self.dict_link = f'https://cn.bing.com/dict/search?q={word_str}'
        # 返回链接对应的html文件
        self.html_file = requests.get(self.dict_link).text
        # 对返回的html文件解析，存为soup
        self.soup = BeautifulSoup(self.html_file, 'html.parser')

        # 从soup 中搜索 词典area 下的所有div
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
        if self.output_dict['word']:
            self.output_dict['sentences'] = \
                re.split(re.compile(r'(?!\D)\d\.'), self.get_content(self.related_soups[1], 'div#sentenceSeg'))[1]
        pass
