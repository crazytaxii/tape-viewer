import tushare as ts
import json
import time
from colored import fg, bg, attr
import pygame

class SingleStock:
    def __init__(self, code):
        self.code = code
        self.name = ""
        self.pre = 0.0
        self.price = 0.0
        self.volume = 0
        self.amount = 0.0
        self.pre_fluc = 0.0
    def set(self, name, pre, price, volume, amount):
        self.name = name
        self.pre = pre
        # self.pre_price = self.price
        self.pre_fluc = self.cal_fluctuation()
        self.price = price
        self.volume = volume
        self.amount = amount
    def get_cur_price(self):
        return self.price
    def get_pre_price(self):
        return self.pre
    def get_pre_fluc(self):
        return self.pre_fluc
    def get_cur_fluc(self):
        return self.cal_fluctuation()
    def coloring(self):
        if self.price > self.pre:
            return 1
        elif self.price == self.pre:
            return 15
        else:
            return 2
    def cal_fluctuation(self):
        return (self.price - self.pre) / self.pre
    def output(self):
        print('%s%-6s\t%s%-6s\t%spre: %s\tnow: %s%s\tfluc: %.2f\t%svol: %14s\tamount: %.0f' % (\
            fg(15), self.code,\
            fg(214), self.name,\
            fg(15), str(self.pre),\
            fg(self.coloring()), str(self.price), self.cal_fluctuation() * 100,\
            fg(15), self.volume, self.amount\
        ))

class Alarm:
    def __init__(self, audio_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
    def play(self):
        pygame.mixer.music.play(0)

def load(file_path):
    file = open(file_path)
    return json.loads(file.read())

def monit(dic, alarm, make_warn):
    for key in dic:
        df = ts.get_realtime_quotes(key)
        dic[key].set(\
            df.loc[0]['name'],\
            float(df.loc[0]['pre_close']),\
            float(df.loc[0]['price']),\
            int(df.loc[0]['volume']),\
            float(df.loc[0]['amount']),\
        )
        if dic[key].get_pre_fluc() > 0 and dic[key].get_cur_fluc() < 0 and make_warn:
            alarm.play()
        dic[key].output()

def main():
    config = load('./config.json')
    alarm = Alarm('./resource/you_suffer.mp3')
    indexDic = {code: SingleStock(code) for code in config['index']}
    selectionDic = {code: SingleStock(code) for code in config['selection']}
    extraDic = {code: SingleStock(code) for code in config['extra']}

    # test
    # monit(codeList)

    while True:
        print('%s%s' % (fg(5), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        monit(indexDic, alarm, True)
        print('---')
        monit(selectionDic, alarm, config['warn'])
        print('---')
        monit(extraDic, alarm, False)
        print()
        time.sleep(config['interval'])

if __name__ == '__main__':
    main()
