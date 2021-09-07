# This is a sample Python script.
import time

import pandas as pd

import setting as tool
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # 从本地读取单词表
    with open('wordlist.txt', 'r') as word_list_file:
        word_list = word_list_file.readlines()
    # 除重
    word_list = set(word_list)

    row_list = []

    for item in word_list:
        # 对单词表内每个单词调用 html解析器-DictRstParser，并返回每个单词的parser对象
        parser = tool.DictRstParser(item)
        # 将每个单词的parser对象中的属性-parser.output_dict <dict> 传入 row_list<list>
        row_list.append(parser.output_dict)
        # 窗口输出结果
        print(parser.output_dict)
        # 防屏蔽
        time.sleep(0.8)

    # 将list 转为 DataFrame对象
    df = pd.DataFrame(row_list)
    df['ame_pr'].replace('美 ','')
    # 用xlsxwriter 去解析该使用什么编码
    xlwriter = pd.ExcelWriter('word_list.xlsx',engine='xlsxwriter')

    df.to_excel(xlwriter,'Sheet0')
    xlwriter.save()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
