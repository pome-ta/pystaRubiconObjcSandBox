'''
  note: [今さら聞けないObjective-Cのメモリ管理 弱い参照と強い参照って何? | DevelopersIO](https://dev.classmethod.jp/articles/object-c-memory/)
'''

import ctypes

from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.functions import NSStringFromClass


class Engine(NSObject):

  @objc_method
  def dealloc(self):
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')


class Car(NSObject):

  engine: Engine = objc_property()

  @objc_method
  def dealloc(self):
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')


def main():
  car = Car.new()
  engine = Engine.new()
  car.engine = engine


if __name__ == '__main__':
  main()
