import ctypes

from rbedge.simd import (
  simd_float2,
  simd_float3,
  simd_float4,
  simd_float3x3,
  simd_float4x4,
)

from matrixMath import matrix_float3x3, matrix_float4x4


class Vertex(ctypes.Structure):
  _fields_ = [
    ('position', simd_float3),
    ('color', simd_float4),
    ('texture', simd_float2),
  ]


class ModelConstants(ctypes.Structure):
  _fields_ = [
    ('modelViewMatrix', simd_float4x4),
    ('materialColor', simd_float4),
    ('normalMatrix', simd_float3x3),
  ]

  def __init__(
    self,
    modelViewMatrix: simd_float4x4 | None = None,
    materialColor: simd_float4 | None = None,
    normalMatrix: simd_float3x3 | None = None,
  ):

    modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix
    materialColor = simd_float4(
      1.0) if materialColor is None else materialColor
    normalMatrix = matrix_float3x3.identity(
    ) if normalMatrix is None else normalMatrix

    super().__init__(
      modelViewMatrix=modelViewMatrix,
      materialColor=materialColor,
      normalMatrix=normalMatrix,
    )


class SceneConstants(ctypes.Structure):
  _fields_ = [
    ('projectionMatrix', simd_float4x4),
  ]

  def __init__(
    self,
    projectionMatrix: simd_float4x4 | None = None,
  ):

    projectionMatrix = matrix_float4x4.identity(
    ) if projectionMatrix is None else projectionMatrix

    super().__init__(projectionMatrix=projectionMatrix)


class Light:

  RAW_TYPE = ctypes.c_float * 12
  size: int = ctypes.sizeof(RAW_TYPE)
  stride: int = ctypes.sizeof(RAW_TYPE)

  color: simd_float3
  ambientIntensity: float
  diffuseIntensity: float
  direction: simd_float3

  def __init__(
    self,
    color: simd_float3 | None = None,
    ambientIntensity: float | None = None,
    diffuseIntensity: float | None = None,
    direction: simd_float3 | None = None,
  ):
    self.raw = self.RAW_TYPE(
      0.0, 0.0, 0.0,  # color  [0, 1, 2]
      0.0,            # padding (SIMD alignment)  [3]
      0.0,            # ambientIntensity  [4]
      0.0,            # diffuseIntensity  [5]
      0.0, 0.0,       # padding (SIMD alignment)  [6, 7]
      0.0, 0.0, 0.0,  # direction  [8, 9, 10]
      0.0,            # padding (SIMD alignment)  [11]
    )  # yapf: disable

    self.color = simd_float3(1) if color is None else color
    self.ambientIntensity = 1.0 if ambientIntensity is None else ambientIntensity
    self.diffuseIntensity = 1.0 if diffuseIntensity is None else diffuseIntensity
    self.direction = simd_float3(0) if direction is None else direction

  @property
  def color(self) -> simd_float3:
    return simd_float3.from_buffer(self.raw)

  @color.setter
  def color(self, values: simd_float3):
    for idx, value in enumerate(values):
      self.raw[idx] = float(value)

  @property
  def ambientIntensity(self) -> float:
    return float(self.raw[4])

  @ambientIntensity.setter
  def ambientIntensity(self, value: float):
    self.raw[4] = float(value)

  @property
  def diffuseIntensity(self) -> float:
    return float(self.raw[5])

  @diffuseIntensity.setter
  def diffuseIntensity(self, value: float):
    self.raw[5] = float(value)

  @property
  def direction(self) -> simd_float3:
    return simd_float3.from_buffer(self.raw, 32)

  @direction.setter
  def direction(self, values: simd_float3):
    for idx, value in enumerate(values):
      self.raw[8 + idx] = float(value)

