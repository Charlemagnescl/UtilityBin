'''
程序思想：
有两个本地语音库，美音库Speech_US，英音库Speech_US
调用有道api，获取语音MP3，存入对应的语音库中
'''

import os
import urllib.request
import argparse


class youdao():
    def __init__(self, type="us", word='hellow'):
        '''
        调用youdao API
        type = 0：美音
        type = 1：英音

        判断当前目录下是否存在两个语音库的目录
        如果不存在，创建
        '''
        word = word.lower()  # 小写
        type = type.lower()
        if type == 'en':
            self._type = 1
        else:
            self._type = 0
        self._word = word  # 单词

        # 文件根目录
        self._dirRoot = os.getcwd()
        self._dirSpeech = self._dirRoot
        
    
    def down(self, words):
        '''
        下载单词的MP3
        判断语音库中是否有对应的MP3
        如果没有就下载
        '''

        word = words
        if isinstance(words, list):
            word = words[0]
            for w in words[1:]:
                word += "%2B"+w

        print(word)

        tmp = self._getWordMp3FilePath(word)
        if tmp is None:
            self._getURL()  # 组合URL
            # 调用下载程序，下载到目标文件夹
            # print('不存在 %s.mp3 文件\n将URL:\n' % word, self._url, '\n下载到:\n', self._filePath)
            # 下载到目标地址
            urllib.request.urlretrieve(self._url, filename=self._filePath)
            print('%s.mp3 下载完成' % self._word)
        else:
            print('已经存在 %s.mp3, 不需要下载' % self._word)

        # 返回声音文件路径
        return self._filePath

    def _getURL(self):
        '''
        私有函数，生成发音的目标URL
        http://dict.youdao.com/dictvoice?type=0&audio=
        '''
        self._url = r'http://dict.youdao.com/dictvoice?type=' + str(
            self._type) + r'&audio=' + self._word

    def _getWordMp3FilePath(self, word):
        '''
        获取单词的MP3本地文件路径
        如果有MP3文件，返回路径(绝对路径)
        如果没有，返回None
        '''
        word = word.lower()  # 小写
        self._word = word
        self._fileName = self._word + '.mp3'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # 判断是否存在这个MP3文件
        if os.path.exists(self._filePath):
            # 存在这个mp3
            return self._filePath
        else:
            # 不存在这个MP3，返回none
            return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download mp3 of words or expressions via Youdao Dictionary API")
    parser.add_argument("--words", nargs="+", type=str, help="words or expressions", required=True)
    parser.add_argument("--accent", choices=["us", "en"], help="us for American accent, en for British accent", default="us")
    args = parser.parse_args()

    sp = youdao(type=args.accent)
    sp.down(args.words)
