import ctypes

from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super

from rbedge.simd import (
  simd_float2,
  simd_float3,
  simd_float4,
)

from .primitive import Primitive

from simdTypes import Vertex


class Cube(Primitive):

  # --- override
  @objc_method
  def buildVertices(self):
    send_super(__class__, self, 'buildVertices')

    self.vertices = (Vertex * (4 + 4))(
      Vertex(  # v0  Front
        position=simd_float3(-1.0,  1.0,  1.0), color=simd_float4(1.0, 0.0, 0.0, 1.0), texture=simd_float2(0.0, 0.0)),
      Vertex(  # v1
        position=simd_float3(-1.0, -1.0,  1.0), color=simd_float4(0.0, 1.0, 0.0, 1.0), texture=simd_float2(0.0, 1.0)),
      Vertex(  # v2
        position=simd_float3( 1.0, -1.0,  1.0), color=simd_float4(0.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 1.0)),
      Vertex(  # v3
        position=simd_float3( 1.0,  1.0,  1.0), color=simd_float4(1.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 0.0)),

      Vertex(  # v4  Back
        position=simd_float3(-1.0,  1.0, -1.0), color=simd_float4(0.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 1.0)),
      Vertex(  # v5
        position=simd_float3(-1.0, -1.0, -1.0), color=simd_float4(0.0, 1.0, 0.0, 1.0), texture=simd_float2(1.0, 1.0)),
      Vertex(  # v6
        position=simd_float3( 1.0, -1.0, -1.0), color=simd_float4(1.0, 0.0, 0.0, 1.0), texture=simd_float2(0.0, 0.0)),
      Vertex(  # v7
        position=simd_float3( 1.0,  1.0, -1.0), color=simd_float4(1.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 0.0)),
    )  # yapf: disable

    self.indices = (ctypes.c_uint16 * (3 * (2 * (3 + 3))))(
      0, 1, 2,   0, 2, 3,   # Front
      4, 6, 5,   4, 7, 6,   # Back

      4, 5, 1,   4, 1, 0,   # Left
      3, 6, 7,   3, 2, 6,   # Right

      4, 0, 3,   4, 3, 7,   # Top
      1, 5, 6,   1, 6, 2,   # Bottom
    )  # yapf: disable

