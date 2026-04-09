"""
dummy
"""


class ModelConstants:
  # float(4バイト) × 36個 = 144バイト
  # [0-15] Matrix4x4 (64 bytes)
  # [16-19] Float4 (16 bytes)
  # [20-31] Matrix3x3 (48 bytes)
  # [32] Specular (4 bytes)
  # [33] Shininess (4 bytes)
  # [34-35] Padding (8 bytes) -> 合計 144 (16の倍数)
  RAW_TYPE = ctypes.c_float * 36
  size: int = ctypes.sizeof(RAW_TYPE)
  stride: int = ctypes.sizeof(RAW_TYPE)

  def __init__(
    self,
    modelViewMatrix: matrix_float4x4 | None = None,
    materialColor: simd_float4 | None = None,
    normalMatrix: matrix_float3x3 | None = None,
    specularIntensity: float = 1.0,
    shininess: float = 1.0,
  ):
    # ゼロ初期化
    self.raw = self.RAW_TYPE()

    # セッター経由で初期値をセット
    self.modelViewMatrix = matrix_float4x4.identity(
    ) if modelViewMatrix is None else modelViewMatrix
    self.materialColor = simd_float4(
      1.0) if materialColor is None else materialColor
    self.normalMatrix = matrix_float3x3.identity(
    ) if normalMatrix is None else normalMatrix
    self.specularIntensity = specularIntensity
    self.shininess = shininess

  # --- modelViewMatrix (オフセット: 0 bytes) ---
  @property
  def modelViewMatrix(self) -> matrix_float4x4:
    return matrix_float4x4.from_buffer(self.raw, 0)

  @modelViewMatrix.setter
  def modelViewMatrix(self, matrix: matrix_float4x4):
    # 行列は大きいので memmove で一気にコピーするのが効率的です
    ctypes.memmove(self.raw, ctypes.byref(matrix), 64)

  # --- materialColor (オフセット: 64 bytes) ---
  @property
  def materialColor(self) -> simd_float4:
    return simd_float4.from_buffer(self.raw, 64)

  @materialColor.setter
  def materialColor(self, values: simd_float4):
    for idx, value in enumerate(values):
      self.raw[16 + idx] = float(value)

  # --- normalMatrix (オフセット: 80 bytes) ---
  @property
  def normalMatrix(self) -> matrix_float3x3:
    # 64(行列) + 16(色) = 80バイト目から
    return matrix_float3x3.from_buffer(self.raw, 80)

  @normalMatrix.setter
  def normalMatrix(self, matrix: matrix_float3x3):
    # 3x3行列は 48バイト
    ctypes.memmove(ctypes.addressof(self.raw) + 80, ctypes.byref(matrix), 48)

  # --- specularIntensity (オフセット: 128 bytes / index: 32) ---
  @property
  def specularIntensity(self) -> float:
    return float(self.raw[32])

  @specularIntensity.setter
  def specularIntensity(self, value: float):
    self.raw[32] = float(value)

  # --- shininess (オフセット: 132 bytes / index: 33) ---
  @property
  def shininess(self) -> float:
    return float(self.raw[33])

  @shininess.setter
  def shininess(self, value: float):
    self.raw[33] = float(value)

  def __repr__(self):
    return (f"<ModelConstants specular={self.specularIntensity:.2f}, "
            f"shininess={self.shininess:.2f}>")




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

