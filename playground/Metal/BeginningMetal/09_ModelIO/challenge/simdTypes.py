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

  def __init__(self,
               modelViewMatrix: simd_float4x4 | None = None,
               materialColor: simd_float4 | None = None):

    modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix
    materialColor = simd_float4(
      1.0) if materialColor is None else materialColor

    super().__init__(modelViewMatrix=modelViewMatrix,
                     materialColor=materialColor)


class SceneConstants(ctypes.Structure):
  _fields_ = [
    ('projectionMatrix', simd_float4x4),
  ]

