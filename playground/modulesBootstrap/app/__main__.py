if __name__ == '__main__':
  try:
    import bootstrap
  except ModuleNotFoundError as e:
    _TARGET_NAME = 'bootstrap'
    if e.name != _TARGET_NAME:
      raise
    import pathlib as _pathlib, runpy as _runpy
    
    _runpy.run_path(
      next(
        filter(
          _pathlib.Path.is_file,
          (_dir / f'{_TARGET_NAME}.py'
           for _dir in _pathlib.Path(__file__).resolve().parents),
        ),
        f'{_TARGET_NAME} not found',
      ))

from pyrubicon.objc import ObjCClass, objc_method  # api
from pyrubicon.objc import send_super  # runtime

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')


class MainViewController(UIViewController):

  @objc_method
  def viewDidLoad(self) -> None:
    send_super(
      __class__,
      self,
      'viewDidLoad',
      restype=None,
    )

    # --- Navigation
    # インスタンス生成後に`title` 指定があるかないかで分岐
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

  @objc_method
  def didReceiveMemoryWarning(self) -> None:
    send_super(
      __class__,
      self,
      'didReceiveMemoryWarning',
      restype=None,
    )
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()
  # 今回は、インスタンス生成後に指定するパターンで
  _title = NSStringFromClass(MainViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen

  app = App.alloc().initWithViewController_(main_vc)
  app.presentWithStyle_(presentation_style)

  try:
    import gc
    gc.collect()
  except Exception as e:
    print('--- collect: error')
    print(f'{e}')

