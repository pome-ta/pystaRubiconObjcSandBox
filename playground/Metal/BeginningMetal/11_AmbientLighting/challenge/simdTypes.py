import ctypes

from rbedge.simd import (
  simd_float2,
  simd_float3,
  simd_float4,
  simd_float4x4,
)

from matrixMath import matrix_float4x4


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
  ]

  def __init__(
    self,
    modelViewMatrix: simd_float4x4 | None = None,
    materialColor: simd_float4 | None = None,
  ):

    modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix
    materialColor = simd_float4(
      1.0) if materialColor is None else materialColor

    super().__init__(
      modelViewMatrix=modelViewMatrix,
      materialColor=materialColor,
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

  RAW_TYPE = ctypes.c_float * 8
  size: int = ctypes.sizeof(RAW_TYPE)
  stride: int = ctypes.sizeof(RAW_TYPE)

  color: simd_float3
  ambientIntensity: float

  def __init__(
    self,
    color: simd_float3 | None = None,
    ambientIntensity: float | None = None,
  ):
    self.raw = self.RAW_TYPE(
      0.0, 0.0, 0.0,  # color
      0.0,            # padding (SIMD alignment)
      0.0,            # ambientIntensity
      0.0, 0.0, 0.0,  # padding (SIMD alignment)
    )  # yapf: disable

    self.color = simd_float3(1) if color is None else color
    self.ambientIntensity = 1.0 if ambientIntensity is None else ambientIntensity

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


