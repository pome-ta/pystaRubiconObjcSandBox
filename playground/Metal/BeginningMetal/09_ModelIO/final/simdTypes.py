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
  ]

  def __init__(self, modelViewMatrix: simd_float4x4 | None = None):

    modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix

    super().__init__(modelViewMatrix=modelViewMatrix)


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

