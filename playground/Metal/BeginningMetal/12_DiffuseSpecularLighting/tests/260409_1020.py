"""
dummy
"""

import ctypes
# from simd import simd_float3 (適宜インポート)


class Light:

  # 48バイト (float(4バイト) × 12個)
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
      0.0, 0.0, 0.0,  # color [0, 1, 2]
      0.0,            # padding [3]
      0.0,            # ambientIntensity [4]
      0.0,            # diffuseIntensity [5]
      0.0, 0.0,       # padding [6, 7] (SIMD alignment)
      0.0, 0.0, 0.0,  # direction [8, 9, 10]
      0.0,            # padding [11]
    )  # yapf: disable

    self.color = simd_float3(1) if color is None else color
    self.ambientIntensity = 1.0 if ambientIntensity is None else ambientIntensity
    self.diffuseIntensity = 1.0 if diffuseIntensity is None else diffuseIntensity
    self.direction = simd_float3(0, -1, 0) if direction is None else direction

  # --- color ---
  @property
  def color(self) -> simd_float3:
    return simd_float3.from_buffer(self.raw)

  @color.setter
  def color(self, values: simd_float3):
    for idx, value in enumerate(values):
      self.raw[idx] = float(value)

  # --- ambientIntensity ---
  @property
  def ambientIntensity(self) -> float:
    return float(self.raw[4])

  @ambientIntensity.setter
  def ambientIntensity(self, value: float):
    self.raw[4] = float(value)

  # --- diffuseIntensity ---
  @property
  def diffuseIntensity(self) -> float:
    return float(self.raw[5])

  @diffuseIntensity.setter
  def diffuseIntensity(self, value: float):
    self.raw[5] = float(value)

  # --- direction ---
  @property
  def direction(self) -> simd_float3:
    # 32バイト(float 8個分)スキップした位置からレンズを被せる
    return simd_float3.from_buffer(self.raw, 32)

  @direction.setter
  def direction(self, values: simd_float3):
    for idx, value in enumerate(values):
      # direction はインデックス 8 からスタート
      self.raw[8 + idx] = float(value)

