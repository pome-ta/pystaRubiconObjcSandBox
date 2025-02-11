import ctypes

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import objc_id, send_super
from pyrubicon.objc.types import NSInteger

from rbedge.functions import NSStringFromClass

from rbedge import pdbr

from tableViewController import TableViewController
from gcCount import Engine, Car


items = ['ほげ', 'ふが',]  # yapf: disable

class ViewController(TableViewController):

  engine: Engine = objc_property()
  car: Car = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    print(f'\t{NSStringFromClass(__class__)}: loadView')
    [self.cellItems.addObject_(i) for i in items]

    engine = Engine.new()
    print(f'# {engine}.retainCount: {engine.retainCount()}')
    car = Car.alloc().initWithEngine_(engine)
    #car = Car.new()
    print(f'# {car}.retainCount: {car.retainCount()}')
    #car.engine = engine
    engine.car = car

    self.engine = engine
    self.car = car

  @objc_method
  def initWithStyle_(self, style: NSInteger) -> ObjCClass:
    send_super(__class__,
               self,
               'initWithStyle:',
               style,
               restype=objc_id,
               argtypes=[
                 NSInteger,
               ])
    print(f'\t{NSStringFromClass(__class__)}: initWithStyle:')
    return self

    # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App

  from rbedge.enumerations import (
    UITableViewStyle,
    UIModalPresentationStyle,
  )
  print(__name__)

  table_style = UITableViewStyle.plain
  main_vc = ViewController.alloc().initWithStyle_(table_style)
  _title = NSStringFromClass(ViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  app = App(main_vc)
  app.main_loop(presentation_style)
  print('--- end ---\n')

