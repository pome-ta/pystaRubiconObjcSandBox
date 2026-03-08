import ctypes

simd_float2 = (ctypes.c_float * 2)
simd_float3 = (ctypes.c_float * 2)
simd_float4 = (ctypes.c_float * 4)

Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)
Texture = (ctypes.c_float * 2)


class Vertex(ctypes.Structure):
  _fields_ = [
    ('position', Position),
    ('color', Color),
    ('texture', Texture),
  ]

