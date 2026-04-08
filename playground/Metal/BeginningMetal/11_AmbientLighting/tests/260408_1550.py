"""
ダミー
"""

from rubicon.objc import objc_method, objc_property, send_super, objc_id
from rubicon.objc.types import CGRect, CGPoint, CGSize

# ※ UIViewController, MTKView, UIView, UIColor などは
# 既にインポート・取得されている前提としています。


class MainViewController(UIViewController):

  metalView = objc_property()
  renderer = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    device = MTLCreateSystemDefaultDevice()
    metalView = MTKView.alloc().initWithFrame_device_(
      self.view.bounds,
      device,
    )

    renderer = Renderer.alloc().initWithDevice_(device)
    renderer.scene = LightingScene.alloc().initWithDevice_size_(
      device,
      metalView.bounds.size,
    )

    metalView.clearColor = Colors.wenderlichGreen
    metalView.delegate = renderer

    metalView.enableSetNeedsDisplay = True
    metalView.setNeedsDisplay()

    self.view.addSubview_(metalView)

    self.metalView = metalView
    self.renderer = renderer
    self.setupLayoutConstraint()

    # デバッグ用の円を保持するための変数を初期化
    self.debugCircle = None

  # ==========================================
  # タッチイベント
  # ==========================================

  @objc_method
  def touchesBegan_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesBegan:withEvent:',
               touches,
               event,
               argtypes=[objc_id, objc_id])
    try:
      self.renderer.scene.touchesBegan_touches_with_(self.view, touches, event)
    except Exception as e:
      print(e)

    # [視覚デバッグ] 円を作って保持する
    touch = touches.anyObject()
    if touch:
      location = touch.locationInView_(self.view)
      radius = 25.0

      # 既に円が残っていたら念のため消す
      if getattr(self, 'debugCircle', None):
        self.debugCircle.removeFromSuperview()

      frame = CGRect(CGPoint(location.x - radius, location.y - radius),
                     CGSize(radius * 2, radius * 2))

      self.debugCircle = UIView.alloc().initWithFrame_(frame)
      self.debugCircle.backgroundColor = UIColor.redColor.colorWithAlphaComponent_(
        0.5)
      self.debugCircle.layer.cornerRadius = radius
      self.debugCircle.userInteractionEnabled = False

      self.view.addSubview_(self.debugCircle)

  @objc_method
  def touchesMoved_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesMoved:withEvent:',
               touches,
               event,
               argtypes=[objc_id, objc_id])
    try:
      self.renderer.scene.touchesMoved_touches_with_(self.view, touches, event)
    except Exception as e:
      print(e)

    # [視覚デバッグ] 円を指の位置に追従させる
    if getattr(self, 'debugCircle', None):
      touch = touches.anyObject()
      if touch:
        # center プロパティの更新でスムーズに移動
        self.debugCircle.center = touch.locationInView_(self.view)

  @objc_method
  def touchesEnded_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesEnded:withEvent:',
               touches,
               event,
               argtypes=[objc_id, objc_id])
    try:
      self.renderer.scene.touchesEnded_touches_with_(self.view, touches, event)
    except Exception as e:
      print(e)

    # [視覚デバッグ] 指が離れたら円を消す
    self._remove_debug_circle()

  @objc_method
  def touchesCancelled_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesCancelled:withEvent:',
               touches,
               event,
               argtypes=[objc_id, objc_id])
    try:
      self.renderer.scene.touchesCancelled_touches_with_(
        self.view, touches, event)
    except Exception as e:
      print(e)

    # [視覚デバッグ] キャンセル時も円を消す
    self._remove_debug_circle()

  # ==========================================
  # Pythonネイティブの補助メソッド
  # ==========================================

  def _remove_debug_circle(self):
    """保持しているデバッグ用の円をアニメーションで消去する"""
    if getattr(self, 'debugCircle', None):
      circle = self.debugCircle
      self.debugCircle = None  # 再操作されないように参照を切る

      def animations():
        circle.alpha = 0.0

      def completion(finished: bool):
        circle.removeFromSuperview()

      UIView.animateWithDuration_animations_completion_(
        0.3, animations, completion)


## べたぬり

self.debugCircle = UIView.alloc().initWithFrame_(frame)
self.debugCircle.backgroundColor = UIColor.redColor.colorWithAlphaComponent_(
  0.5)
self.debugCircle.layer.cornerRadius = radius
self.debugCircle.userInteractionEnabled = False

## 線のみ

self.debugCircle = UIView.alloc().initWithFrame_(frame)

# 1. 「塗り」を透明にする
self.debugCircle.backgroundColor = UIColor.clearColor

# 2. 「線」の太さを設定する(例: 2.0ポイント)
self.debugCircle.layer.borderWidth = 2.0

# 3. 「線」の色を設定する(※重要:UIColorではなくCGColorに変換して渡す)
self.debugCircle.layer.borderColor = UIColor.redColor.colorWithAlphaComponent_(
  0.8).CGColor

# 4. 角丸にして円にする処理はそのまま残す
self.debugCircle.layer.cornerRadius = radius
self.debugCircle.userInteractionEnabled = False

