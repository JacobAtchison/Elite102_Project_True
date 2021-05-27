class test:
    def __init__(self, name, acct_num, pin, balance = 0):
        self.name = name
        self.acct = acct_num
        self.pin = pin
        self.balance = balance)

    
def __get__(self, obj, objtype):
    return self.name, self.name

test = test("test",1234,0000)


print(__get__(test,str))