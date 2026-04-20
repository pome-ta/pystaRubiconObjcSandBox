"""
dummy
"""

import math
import ctypes

from rubicon.objc.api import objc_method, objc_property, objc_ivar
from rubicon.objc.runtime import send_super, get_ivar, set_ivar
from rubicon.objc.types import CGSize, CGFloat

# ※ 以下はプロジェクトの構成に合わせてインポートしてください
# from nodes import Model
# from scenes import GameScene


class GameOverScene(Scene):

  # gameOverModelなどのプロパティを定義
  gameOverModel = objc_property(object)
  registerTouch = objc_property(bool)
  time = objc_property(float)

  # 1. win のための内部インスタンス変数を定義
  _win = objc_ivar(bool)

  # 2. win の Getter
  @objc_method
  def win(self) -> bool:
    return get_ivar(self, "_win")

  # 3. win の Setter (ここに didSet のロジックを書く)
  @objc_method
  def setWin_(self, new_win: bool):
    set_ivar(self, "_win", new_win)

    # --- ここから didSet のロジック ---
    if new_win:
      # Modelの初期化はPython側の実装に合わせて適宜変更してください
      self.gameOverModel = Model(device=self.device, modelName="youwin")
      # float4(0, 1, 0, 1) の設定
      self.gameOverModel.materialColor = [0.0, 1.0, 0.0, 1.0]
    else:
      self.gameOverModel = Model(device=self.device, modelName="youlose")
      # float4(1, 0, 0, 1) の設定
      self.gameOverModel.materialColor = [1.0, 0.0, 0.0, 1.0]

    self.addChildNode_(self.gameOverModel)
    # --------------------------------

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    # 親クラス(Scene)の初期化呼び出し
    # セレクタ名は元のメソッドに合わせて 'initWithDevice:size:' になります
    send_super(__class__, self, 'initWithDevice:size:', device, size)

    self.registerTouch = False
    self.time = 0.0

    # Swiftの仕様に合わせ、初期化時の代入では didSet を発火させないため、
    # 内部変数 _win に直接 False をセットします。
    set_ivar(self, "_win", False)

    self.light.color = [1.0, 1.0, 1.0]
    self.light.ambientIntensity = 0.3
    self.light.diffuseIntensity = 0.8
    self.light.direction = [0.0, -1.0, -1.0]
    self.camera.position.z = -30.0

    return self

  @objc_method
  def updateWithDeltaTime_(self, deltaTime: CGFloat):
    self.time += deltaTime

    amplitude = 0.5
    period = 2.0
    periodicAmount = math.sin(
      (self.time + 0.8) * period) * amplitude * deltaTime

    # π は math.pi を使用します
    self.gameOverModel.rotation.x -= math.pi * periodicAmount

    # gameOverModel.scale += float3(periodicAmount/4) の再現
    # 実行環境のベクトル実装によりますが、各要素に足す場合は以下のようになります
    scale_add = periodicAmount / 4.0
    self.gameOverModel.scale.x += scale_add
    self.gameOverModel.scale.y += scale_add
    self.gameOverModel.scale.z += scale_add

  @objc_method
  def touchesBegan_touches_with_(self, view, touches, event):
    self.registerTouch = True

  @objc_method
  def touchesEnded_touches_with_(self, view, touches, event):
    if self.registerTouch:
      # GameSceneへの遷移処理
      scene = GameScene(device=self.device, size=self.size)
      if self.sceneDelegate:
        self.sceneDelegate.transitionTo_(scene)

