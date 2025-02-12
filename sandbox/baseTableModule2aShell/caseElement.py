'''
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.api import NSObject, NSString
from pyrubicon.objc.runtime import send_super, objc_id, send_message, SEL

from rbedge.functions import NSStringFromClass
from rbedge import pdbr


class CaseElement(NSObject):
  # セルの視覚的なタイトル (テーブル セクションのヘッダー タイトル)
  title: NSString = objc_property()
  # nib ファイル内でセルを検索するためのテーブルビューのセルの識別子
  cellID: NSString = objc_property()
  # セルのサブビューを設定するための構成ハンドラー。
  # xxx: ガバガバ
  # configHandler = objc_property()
  configHandlerName: NSString = objc_property()
  
  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')
  
  @objc_method
  def initWithTitle_cellID_configHandlerName_(
      self, title, cellID, configHandlerName):
    self.title = NSString.stringWithString_(title)
    self.cellID = NSString.stringWithString_(cellID)
    self.configHandlerName = NSString.stringWithString_(configHandlerName)
    return self
  
  @objc_method
  def targetView(self, cell):
    return cell.contentView.subviews()[0] if cell is not None else None



'''
'''
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import objc_id, send_message, SEL

from rbedge.objcMainThread import onMainThread
from rbedge import pdbr
'''


class CaseElement:

  def __init__(self, title: str, cellID: str, configHandlerName: str):
    # セルの視覚的なタイトル (テーブル セクションのヘッダー タイトル)
    self.title = title
    # nib ファイル内でセルを検索するためのテーブルビューのセルの識別子。
    self.cellID = cellID
    # セルのサブビューを設定するための構成ハンドラー。
    # xxx: ガバガバ
    #self.target = target
    self.configHandlerName = configHandlerName

  def __del__(self):
    print('\t\t__del__')

    self.title = None
    self.cellID = None

    self.configHandlerName = None

  #@onMainThread
  '''
  def configHandler(self, view):
    

    @Block
    def block_handler(v: objc_id) -> None:
      #self._configHandler(v)
      #self.target.performSelector_withObject_(SEL(self._configHandlerName), v)
      #self.target.performSelectorOnMainThread_withObject_waitUntilDone_(SEL(self._configHandlerName),v, False)
      send_message(self.target, self._configHandler, v, restype=None, argtypes=[objc_id])

    block_handler(view)
    

    target.performSelector_withObject_(SEL(send_message(self.target, self._configHandler, view, restype=None, argtypes=[objc_id])), view)
    #self.target.performSelectorOnMainThread_withObject_waitUntilDone_(SEL(self._configHandlerName),view, False)
    #sel = SEL(self._configHandlerName)

    #pdbr.state(self._configHandler)
    #print(self._configHandler)
    #self._configHandler(view)
    #print(self._configHandler)
    #print(dir(self._configHandler))
    #send_message(self.target,self._configHandler , view, restype=None, argtypes=[objc_id])
    #send_message(self.target, self._configHandler, v, restype=None, argtypes=[objc_id])
    pass
    '''

  @staticmethod
  def targetView(cell):
    return cell.contentView.subviews()[0] if cell is not None else None

