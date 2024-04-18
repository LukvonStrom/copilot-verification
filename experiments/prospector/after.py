import sys

def someFunction():
  global x
  x = 10
  x=x+1 

class myClass():
    def __init__(self, data):
        self.data = data

    def do_something(self):
        if (self.data == None): 
            print("No data!")
        else:
            print("Data: " + self.data)  

def unused_function():
    pass

def error_prone_function():
    try:
        risky_call()
    except:
        pass 

def risky_call():

    print("Hello, world!")
    return 1 / 0 

if __name__ == "__main__":
    someFunction()
    obj = myClass(None)
    obj.do_something()
    print(x)
