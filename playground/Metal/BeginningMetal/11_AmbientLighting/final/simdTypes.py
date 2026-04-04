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


'''
class Light(ctypes.Structure):
  _fields_ = [
    ('color', simd_float4),
    ('ambientIntensity', ctypes.c_float),
    ('_pad', ctypes.c_float * 3),
  ]

  def __init__(
    self,
    color: simd_float4 | None = None,
    ambientIntensity: ctypes.c_float | None = None,
  ):

    color = simd_float4(1) if color is None else color

    ambientIntensity = ctypes.c_float(
      1.0) if ambientIntensity is None else ambientIntensity

    super().__init__(
      color=color,
      ambientIntensity=ambientIntensity,
    )
'''


class Light(ctypes.Structure):
  _fields_ = [
    ('color', simd_float4),
    ('ambientIntensity', ctypes.c_float),
    ('_pad', ctypes.c_float * 3),
  ]

