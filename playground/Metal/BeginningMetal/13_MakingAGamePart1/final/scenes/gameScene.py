from dataclasses import dataclass
from math import radians, tan, pi

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3, simd_float4

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model, Instance

from utilities import generateColorsNumber_


@dataclass
class Constants:
  gameHeight: float = 48.0
  gameWidth: float = 27.0
  bricksPerRow: int = 8
  bricksPerColumn: int = 8


class GameScene(Scene):

  ball: Model = objc_property()
  paddle: Model = objc_property()

  bricks: Instance = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.ball = Model.alloc().initWithDevice_modelName_(
      device,
      'ball',
    )
    self.paddle = Model.alloc().initWithDevice_modelName_(
      device,
      'paddle',
    )

    self.bricks = Instance.alloc().initWithDevice_modelName_instances_(
      device,
      'brick',
      Constants.bricksPerRow * Constants.bricksPerColumn,
    )

    send_super(__class__,
               self,
               'initWithDevice:size:',
               device,
               size,
               argtypes=[
                 objc_id,
                 CGSize,
               ])

    self.camera.position.z = -self.sceneOffsetHeight_fov_(
      Constants.gameHeight,
      camera.fovRadians,
    )
    self.camera.position.x = -Constants.gameWidth / 2
    self.camera.position.y = -Constants.gameHeight / 2
    self.camera.rotation.x = radians(20)
    self.camera.position.y = -Constants.gameHeight / 2 + 5

    self.light.color = simd_float3(1, 1, 1)
    self.light.ambientIntensity = 0.3
    self.light.diffuseIntensity = 0.8
    self.light.direction = simd_float3(0, -1, -1)
    self.setupScene()

    return self

  @objc_method
  def setupScene(self):
    self.ball.position.x = Constants.gameWidth / 2
    self.ball.position.y = Constants.gameHeight * 0.1
    self.ball.materialColor = simd_float4(0.5, 0.9, 0, 1)
    self.addChildNode_(self.ball)

    self.paddle.position.x = Constants.gameWidth / 2
    self.paddle.position.y = Constants.gameHeight * 0.05
    self.paddle.materialColor = simd_float4(1, 0, 0, 1)
    self.addChildNode_(self.paddle)

    border = Model.alloc().initWithDevice_modelName_(
      self.device,
      'border',
    )
    border.position.x = Constants.gameWidth / 2
    border.position.y = Constants.gameHeight / 2
    border.materialColor = simd_float4(0.51, 0.24, 0, 1)
    self.addChildNode_(border)

    colors = generateColorsNumber_(Constants.bricksPerRow)

    margin = Constants.gameWidth * 0.11
    startY = Constants.gameHeight * 0.5

    for row in range(Constants.bricksPerRow):
      for column in range(Constants.bricksPerColumn):
        position = simd_float3(0)
        position.x = margin + (margin * float(row))
        position.y = startY + (margin * float(column))
        index = row * Constants.bricksPerColumn + column
        self.bricks.nodes[index].position = position
        self.bricks.nodes[index].materialColor = colors[row]

    self.addChildNode_(self.bricks)

  # --- override
  @objc_method
  def updateWithDeltaTime_(self, deltaTime: CGFloat):
    send_super(__class__,
               self,
               'updateWithDeltaTime:',
               deltaTime,
               argtypes=[
                 CGFloat,
               ])

    for brick in self.bricks.nodes:
      brick.rotation.y += pi / 4 * deltaTime
      brick.rotation.z += pi / 4 * deltaTime

  @objc_method
  def sceneOffsetHeight_fov_(self, height: float, fov: float) -> float:
    return (height / 2) / tan(fov / 2)

