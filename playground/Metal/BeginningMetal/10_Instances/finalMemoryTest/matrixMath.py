from math import cos, sin, tan, pi

from rbedge.simd import (
  simd_float3,
  simd_float4,
  simd_float3x3,
  simd_float4x4,
  matrix_multiply,
)


def radians(fromDegrees: float) -> float:
  return (fromDegrees / 180.0) * pi


def degrees(fromRadians: float) -> float:
  return (fromRadians / pi) * 180.0


class matrix_float3x3(simd_float3x3):

  _array = simd_float3 * 3

  @classmethod
  def from_columns(cls, c0, c1, c2):
    return cls(cls._array(c0, c1, c2))

  @classmethod
  def identity(cls):
    return cls.from_columns(
      simd_float3(1, 0, 0),
      simd_float3(0, 1, 0),
      simd_float3(0, 0, 1),
    )

  def __repr__(self):
    rows = []
    for r in range(3):
      row = []
      for c in range(3):
        row.append(f'{self.columns[c][r]: .4f}')
      rows.append(' '.join(row))
    return '\n'.join(rows)


class matrix_float4x4(simd_float4x4):

  _array = simd_float4 * 4

  @classmethod
  def from_columns(cls, c0, c1, c2, c3):
    return cls(cls._array(c0, c1, c2, c3))

  @classmethod
  def identity(cls):
    return cls.from_columns(
      simd_float4(1, 0, 0, 0),
      simd_float4(0, 1, 0, 0),
      simd_float4(0, 0, 1, 0),
      simd_float4(0, 0, 0, 1),
    )

  @classmethod
  def translation(cls, x: float, y: float, z: float):
    return cls.from_columns(
      simd_float4(1, 0, 0, 0),
      simd_float4(0, 1, 0, 0),
      simd_float4(0, 0, 1, 0),
      simd_float4(x, y, z, 1),
    )

  def translatedBy(self, x: float, y: float, z: float):
    return matrix_multiply(self, matrix_float4x4.translation(x, y, z))

  @classmethod
  def scale(cls, x: float, y: float, z: float):
    return cls.from_columns(
      simd_float4(x, 0, 0, 0),
      simd_float4(0, y, 0, 0),
      simd_float4(0, 0, z, 0),
      simd_float4(0, 0, 0, 1),
    )

  def scaledBy(self, x: float, y: float, z: float):
    return matrix_multiply(self, matrix_float4x4.scale(x, y, z))

  @classmethod
  def rotationAngle(cls, angle: float, x: float, y: float, z: float):
    c = cos(angle)
    s = sin(angle)

    column0 = simd_float4(
      x * x + (1 - x * x) * c,
      x * y * (1 - c) - z * s,
      x * z * (1 - c) + y * s,
      0,
    )
    column1 = simd_float4(
      x * y * (1 - c) + z * s,
      y * y + (1 - y * y) * c,
      y * z * (1 - c) - x * s,
      0,
    )
    column2 = simd_float4(
      x * z * (1 - c) - y * s,
      y * z * (1 - c) + x * s,
      z * z + (1 - z * z) * c,
      0,
    )
    column3 = simd_float4(
      0,
      0,
      0,
      1,
    )

    return cls.from_columns(
      column0,
      column1,
      column2,
      column3,
    )

  def rotatedBy(self, angle: float, x: float, y: float, z: float):
    return matrix_multiply(
      self,
      matrix_float4x4.rotationAngle(angle, x, y, z),
    )

  @classmethod
  def projectionFov(cls, fov: float, aspect: float, nearZ: float, farZ: float):
    y = 1 / tan(fov * 0.5)
    x = y / aspect
    z = farZ / (nearZ - farZ)

    return cls.from_columns(
      simd_float4(x, 0, 0, 0),
      simd_float4(0, y, 0, 0),
      simd_float4(0, 0, z, -1),
      simd_float4(0, 0, z * nearZ, 0),
    )

  def upperLeft3x3(self):
    return matrix_float3x3.from_columns(
      self.columns[0].xyz,
      self.columns[1].xyz,
      self.columns[2].xyz,
    )

  def __repr__(self):
    rows = []

    for r in range(4):
      row = []
      for c in range(4):
        row.append(f'{self.columns[c][r]: .4f}')
      rows.append(' '.join(row))

    return '\n'.join(rows)

