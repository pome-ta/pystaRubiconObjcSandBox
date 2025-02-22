import ctypes
from enum import Enum

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id, SEL
from pyrubicon.objc.types import NSInteger, CGPoint

from caseElement import CaseElement

from baseTableViewController import BaseTableViewController
from storyboard.testMainViewController import prototypes

from rbedge.enumerations import (
  UIControlState,
  UIControlEvents,
  UIButtonConfigurationCornerStyle,
  UIImageRenderingMode,
  NSUnderlineStyle,
  UIImageSymbolScale,
  NSDirectionalRectEdge,
  UIButtonConfigurationSize,
)

from rbedge.globalVariables import (
  NSAttributedStringKey,
  UIFontTextStyle,
)

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIColor = ObjCClass('UIColor')
UIButtonConfiguration = ObjCClass('UIButtonConfiguration')
UIColor = ObjCClass('UIColor')
NSAttributedString = ObjCClass('NSAttributedString')
UIImageSymbolConfiguration = ObjCClass('UIImageSymbolConfiguration')
UIFont = ObjCClass('UIFont')
UIImage = ObjCClass('UIImage')
NSDictionary = ObjCClass('NSDictionary')
UIToolTipConfiguration = ObjCClass('UIToolTipConfiguration')
UIAction = ObjCClass('UIAction')
UIButton = ObjCClass('UIButton')  # todo: 型確認用


class testKind(Enum):
  hoge = 'hoge'
  fuga = 'fuga'


class TestMainViewController(BaseTableViewController):
  cartItemCount:NSInteger = objc_property(NSInteger)

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def initWithStyle_(self, style: NSInteger) -> ObjCInstance:
    send_super(__class__,
               self,
               'initWithStyle:',
               style,
               restype=objc_id,
               argtypes=[
                 NSInteger,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: initWithStyle_')
    return self

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')
    [
      self.tableView.registerClass_forCellReuseIdentifier_(
        prototype['cellClass'], prototype['identifier'])
      for prototype in prototypes
    ]

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = 'title' if (
      title := self.navigationItem.title) is None else title

    self.cartItemCount = 0
    
    c1 = CaseElement.alloc().initWithTitle_cellID_configHandlerName_(
      'hogehoge', testKind.hoge.value, 'configureHogeView:')

    c2 = CaseElement.alloc().initWithTitle_cellID_configHandlerName_(
      'fugafuga', testKind.fuga.value, 'configureFugaView:')


    self.testCells.addObject_(c1)
    self.testCells.addObject_(c2)

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    # print('\t↑ ---')
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    # print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

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
    # xxx: a-shell で動くけど、Pythonista3 の2回目の`dealloc` が呼ばれない
    #self.testCells = None

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  @objc_method
  def toolTipInteraction_configurationAtPoint_(
      self, interaction, point: CGPoint) -> ctypes.c_void_p:
    return UIToolTipConfiguration.configurationWithToolTip_('hoge').ptr

  @objc_method
  def addToCart_(self, _action: ctypes.c_void_p) -> None:
    print('いい')
    
    action = ObjCInstance(_action)

    self.cartItemCount = 0 if self.cartItemCount > 0 else 12

    if action.sender.isKindOfClass_(UIButton):
      button = action.sender
      button.setNeedsUpdateConfiguration()
    

  # MARK: - Configuration
  @objc_method
  def configureHogeView_(self, button):
    config = UIButtonConfiguration.filledButtonConfiguration()
    config.buttonSize = UIButtonConfigurationSize.large
    config.image = UIImage.systemImageNamed('cart.fill')
    config.title = 'Add to Cart'
    config.cornerStyle = UIButtonConfigurationCornerStyle.capsule
    config.baseBackgroundColor = UIColor.systemTealColor()
    button.configuration = config
    

    button.toolTip = ''  # The value will be determined in its delegate. > 値はデリゲート内で決定されます。
    # xxx: wip
    # button.toolTipInteraction.delegate = self
    button.addAction_forControlEvents_(
      UIAction.actionWithHandler_(Block(self.addToCart_, None,
                                        ctypes.c_void_p)),
      UIControlEvents.touchUpInside)

    button.changesSelectionAsPrimaryAction = True
    

    @Block
    def _handler(button_id: objc_id) -> None:
      _button = ObjCInstance(button_id)

      # Start with the current button's configuration.
      # > 現在のボタンの設定から始めます。
      # newConfig = _button.configuration
      newConfig = UIButtonConfiguration.filledButtonConfiguration()
      newConfig.buttonSize = UIButtonConfigurationSize.large
      newConfig.title = 'Add to Cart'
      newConfig.cornerStyle = UIButtonConfigurationCornerStyle.capsule
      newConfig.baseBackgroundColor = UIColor.systemTealColor()

      if _button.isSelected():
        # xxx: これだと`0` の時、取れない?
        newConfig.image = UIImage.systemImageNamed('cart.fill.badge.plus') if self.cartItemCount > 0 else UIImage.systemImageNamed('cart.badge.plus')
        # xxx: 力技
        newConfig.subtitle = f'{self.cartItemCount}items'
        #newConfig.subtitle = f'{1}items'
        print('あ')
      else:
        # As the button is highlighted (pressed), apply a temporary image and subtitle.
        # > ボタンがハイライト表示される(押される)と、一時的な画像と字幕が適用されます。
        newConfig.image = UIImage.systemImageNamed('cart.fill')
        newConfig.subtitle = ' '  # xxx: 文字パディング

      newConfig.imagePadding = 8
      _button.configuration = newConfig

    # This handler is called when this button needs updating.
    # > このハンドラーは、このボタンを更新する必要がある場合に呼び出されます。
    button.configurationUpdateHandler = _handler
    

  @objc_method
  def configureFugaView_(self, button):
    pass

  # MARK: - Button Actions
  @objc_method
  def buttonClicked_(self, sender):
    print(f'Button was clicked.{sender}')

  @objc_method
  def toggleButtonClicked_(self, sender):
    print(f'Toggle action: {sender}')

if __name__ == '__main__':
  from rbedge.app import App

  from rbedge.enumerations import (
    UITableViewStyle,
    UIModalPresentationStyle,
  )

  print('__name__')

  table_style = UITableViewStyle.grouped
  main_vc = TestMainViewController.alloc().initWithStyle_(table_style)
  _title = NSStringFromClass(TestMainViewController)
  main_vc.navigationItem.title = _title

  # presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc)
  print('---')
  app.main_loop(presentation_style)
  print('--- end ---\n')

