class A(object):
    def a(self):
        self.s()

    @staticmethod
    def s():
        print("HA")

o = A()
o.a()
