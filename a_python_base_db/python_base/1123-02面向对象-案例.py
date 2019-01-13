#coding=utf-8

class Road:
    def __init__(self):
        self.juli = 100
        self.shijian = 0
    def run(self, shijian):
        self.shijian = shijian
        if self.shijian > 60:
            shengyu = self.juli - self.shijian * 0.5
            if shengyu < 20:
                print('last %d KM' %shengyu)
            else:
                print('go on,remain %d KM.'%shengyu)

        else:
            print('so fast!')

dongguan = Road()
dongguan.run(20)
dongguan.run(70)
