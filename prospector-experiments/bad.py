import os

def BADFunctionName(  ):
  global x
  x=1
  print( "Hello, World!"  )

class some_class:
  def __init__(self, a, B):
    self.A = a
    self.B = B

  def do_something():
    assert self.A>0
    return self.A+self.B

if 1==1:
  print("This is bad practice.")

y=BADFunctionName()