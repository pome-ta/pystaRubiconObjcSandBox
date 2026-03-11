import ctypes

from rbedge.simd import (
  simd_float2,
  simd_float3,
  simd_float4,
)


class Vertex(ctypes.Structure):
  _fields_ = [
    ('position', simd_float3),
    ('color', simd_float4),
    ('texture', simd_float2),
  ]


if __name__ == '__main__':
  pass

