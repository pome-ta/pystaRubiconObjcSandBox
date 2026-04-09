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


'''
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

'''


class ModelConstants:

  RAW_TYPE = ctypes.c_float * 36
  size: int = ctypes.sizeof(RAW_TYPE)
  stride: int = ctypes.sizeof(RAW_TYPE)

  modelViewMatrix: simd_float4x4
  materialColor: simd_float4
  normalMatrix: simd_float3x3
  specularIntensity: float
  shininess: float

  def __init__(
    self,
    modelViewMatrix: simd_float4x4 | None = None,
    materialColor: simd_float4 | None = None,
    normalMatrix: simd_float3x3 | None = None,
    specularIntensity: float | None = None,
    shininess: float | None = None,
  ):
    self.raw = self.RAW_TYPE(
      # --- modelViewMatrix: 64 bytes ---
      0.0, 0.0, 0.0, 0.0,  # col 0  [0, 1, 2, 3]
      0.0, 0.0, 0.0, 0.0,  # col 1  [4, 5, 6, 7]
      0.0, 0.0, 0.0, 0.0,  # col 2  [8, 9, 10, 11]
      0.0, 0.0, 0.0, 0.0,  # col 3  [12, 13, 14, 15]
      # --- materialColor: 16 bytes ---
      0.0, 0.0, 0.0, 0.0,  # r, g, b, a  [16, 17, 18, 19]
      # --- normalMatrix: 48 bytes ---
      0.0, 0.0, 0.0,       # col 0 (x, y, z)  [20, 21, 22]
      0.0,                 # padding  [23]
      0.0, 0.0, 0.0,       # col 1 (x, y, z)  [24, 25, 26]
      0.0,                 # padding  [27]
      0.0, 0.0, 0.0,       # col 2 (x, y, z)  [28, 29, 30]
      0.0,                 # padding  [31]
      # --- specular & shininess: 8 bytes ---
      0.0,                 # specularIntensity  [32]
      0.0,                 # shininess  [33]
      # --- tail padding: 8 bytes ---
      0.0, 0.0             # padding (SIMD alignment)  [34, 35]
    )  # yapf: disable

    # セッター経由で初期値をセット
    self.modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix
    self.materialColor = simd_float4(
      1) if materialColor is None else materialColor
    self.normalMatrix = matrix_float3x3.identity(
    ) if normalMatrix is None else normalMatrix
    self.specularIntensity = 1.0 if specularIntensity is None else specularIntensity
    self.shininess = 1.0 if shininess is None else shininess

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

  @property
  def normalMatrix(self) -> matrix_float3x3:
    return matrix_float3x3.from_buffer(self.raw, 80)

  @normalMatrix.setter
  def normalMatrix(self, matrix: matrix_float3x3):
    ctypes.memmove(ctypes.addressof(self.raw) + 80, ctypes.byref(matrix), 48)

  @property
  def specularIntensity(self) -> float:
    return float(self.raw[32])

  @specularIntensity.setter
  def specularIntensity(self, value: float):
    self.raw[32] = float(value)

  @property
  def shininess(self) -> float:
    return float(self.raw[33])

  @shininess.setter
  def shininess(self, value: float):
    self.raw[33] = float(value)


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

