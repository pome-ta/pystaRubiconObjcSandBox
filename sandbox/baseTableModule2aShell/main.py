'''
  note: [今さら聞けないObjective-Cのメモリ管理 弱い参照と強い参照って何? | DevelopersIO](https://dev.classmethod.jp/articles/object-c-memory/)
'''

import ctypes

from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.functions import NSStringFromClass
from rbedge import pdbr


class Engine(NSObject):
  car = objc_property(weak=True)
  
  # car = objc_property()
  
  @objc_method
  def dealloc(self):
    # send_super(__class__, self, 'dealloc')
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')
    print(
      f'\t# {NSStringFromClass(__class__)}.retainCount: {self.retainCount()}')
  
  @objc_method
  def init(self):
    send_super(__class__, self, 'init', restype=objc_id)
    print(f'{NSStringFromClass(__class__)}: int')
    print(
      f'\t# {NSStringFromClass(__class__)}.retainCount: {self.retainCount()}')
    return self


class Car(NSObject):
  engine: Engine = objc_property()
  
  @objc_method
  def dealloc(self):
    # send_super(__class__, self, 'dealloc')
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')
    print(
      f'\t# {NSStringFromClass(__class__)}.retainCount: {self.retainCount()}')
  
  '''
  @objc_method
  def initWithEngine_(self, engine):
    send_super(__class__, self, 'init', restype=objc_id)
    print(f'{NSStringFromClass(__class__)}: initWithEngine:')
    print(
      f'\t# {NSStringFromClass(__class__)}.retainCount: {self.retainCount()}')
    self.engine = engine
    print(
      f'\t# {NSStringFromClass(__class__)}.retainCount: {self.retainCount()}')
    
    return self
  
  '''
  
  @objc_method
  def init(self):
    send_super(__class__, self, 'init', restype=objc_id)
    print(f'{NSStringFromClass(__class__)}: init')
    print(
      f'\t# {NSStringFromClass(__class__)}.retainCount: {self.retainCount()}')
    
    return self


def main():
  engine = Engine.new()
  print(f'# {engine}.retainCount: {engine.retainCount()}')
  # car = Car.alloc().initWithEngine_(engine)
  car = Car.new()
  print(f'# {car}.retainCount: {car.retainCount()}')
  car.engine = engine
  engine.car = car


if __name__ == '__main__':
  main()
