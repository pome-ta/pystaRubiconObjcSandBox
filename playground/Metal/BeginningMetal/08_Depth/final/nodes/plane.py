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


class Plane(Node):

  # --- override
  @objc_method
  def buildVertices(self):
    send_super(__class__, self, 'buildVertices')

    self.vertices = (Vertex * 4)(
      Vertex(  # v0
        position=simd_float3(-1.0,  1.0,  0.0), color=simd_float4(1.0, 0.0, 0.0, 1.0), texture=simd_float2(0.0, 1.0)),
      Vertex(  # v1
        position=simd_float3(-1.0, -1.0,  0.0), color=simd_float4(0.0, 1.0, 0.0, 1.0), texture=simd_float2(0.0, 0.0)),
      Vertex(  # v2
        position=simd_float3( 1.0, -1.0,  0.0), color=simd_float4(0.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 0.0)),
      Vertex(  # v3
        position=simd_float3( 1.0,  1.0,  0.0), color=simd_float4(1.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 1.0)),
    )  # yapf: disable

    self.indices = (ctypes.c_uint16 * (2 * 3))(
      0, 1, 2,
      2, 3, 0,
    )  # yapf: disable

