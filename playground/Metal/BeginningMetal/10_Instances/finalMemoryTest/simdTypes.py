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


'''
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
'''


class ModelConstants:

  # modelViewMatrix (16) + materialColor (4) = 20 floats
  RAW_TYPE = ctypes.c_float * 20
  size: int = ctypes.sizeof(RAW_TYPE)
  stride: int = ctypes.sizeof(RAW_TYPE)

  modelViewMatrix: simd_float4x4
  materialColor: simd_float4

  def __init__(
    self,
    modelViewMatrix: simd_float4x4 | None = None,
    materialColor: simd_float4 | None = None,
  ):
    self.raw = self.RAW_TYPE(
      # --- modelViewMatrix: 64 bytes ---
      0.0, 0.0, 0.0, 0.0,  # col 0  [0-3]
      0.0, 0.0, 0.0, 0.0,  # col 1  [4-7]
      0.0, 0.0, 0.0, 0.0,  # col 2  [8-11]
      0.0, 0.0, 0.0, 0.0,  # col 3  [12-15]

      # --- materialColor: 16 bytes ---
      0.0, 0.0, 0.0, 0.0,  # [16-19]
    )  # yapf: disable

    self.modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix
    self.materialColor = simd_float4(
      1.0) if materialColor is None else materialColor

  @property
  def modelViewMatrix(self) -> matrix_float4x4:
    return matrix_float4x4.from_buffer(self.raw, 0)

  @modelViewMatrix.setter
  def modelViewMatrix(self, matrix: matrix_float4x4):
    ctypes.memmove(self.raw, ctypes.byref(matrix), 64)

  @property
  def materialColor(self) -> simd_float4:
    return simd_float4.from_buffer(self.raw, 64)

  @materialColor.setter
  def materialColor(self, values: simd_float4):
    for idx, value in enumerate(values):
      self.raw[16 + idx] = float(value)


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

