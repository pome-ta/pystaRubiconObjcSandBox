"""
dummy
"""


# 1
# --- extension Renderable
@objc_method
def doRenderWithCommandEncoder_modelViewMatrix_(
  self,
  commandEncoder,
  modelViewMatrix: object,
):

  if not ((instanceBuffer := self.instanceBuffer) and len(self.nodes) > 0):
    return

  # 1. instanceBuffer の先頭メモリアドレス(整数値)を取得
  base_address = ctypes.cast(instanceBuffer.contents, ctypes.c_void_p).value

  # 2. 毎ノードでメモリを新しく作らないよう、書き込み用のインスタンスを「1つ」だけ用意
  constants = ModelConstants()

  for idx, node in enumerate(self.nodes):
    # --- 値の計算 ---
    # (何度も計算しないよう、一度変数に格納すると効率的です)
    mv_matrix = matrix_multiply(modelViewMatrix, node.modelMatrix)

    # --- constants へのセット ---
    constants.modelViewMatrix = mv_matrix
    constants.materialColor = node.materialColor
    constants.normalMatrix = mv_matrix.upperLeft3x3()
    constants.shininess = node.shininess
    constants.specularIntensity = node.specularIntensity

    # 3. メモリの書き込み先アドレスを計算 (先頭アドレス + インデックス × 144バイト)
    dst_address = base_address + (idx * ModelConstants.size)

    # 4. 完成した 144バイト (constants.raw) を Metal のバッファへ一気にコピー!
    ctypes.memmove(dst_address, constants.raw, ModelConstants.size)

  # --- 以降の描画処理はそのまま ---
  commandEncoder.setFragmentTexture_atIndex_(self.model.texture, 0)
  commandEncoder.setRenderPipelineState_(self.pipelineState)
  commandEncoder.setVertexBuffer_offset_atIndex_(instanceBuffer, 0, 1)

  if not ((meshes := self.model.meshes) and len(meshes) > 0):
    return

  for mesh in meshes:
    vertexBuffer = mesh.vertexBuffers.objectAtIndexedSubscript_(0)
    commandEncoder.setVertexBuffer_offset_atIndex_(
      vertexBuffer.buffer,
      vertexBuffer.offset,
      0,
    )

    for submesh in mesh.submeshes:
      commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_instanceCount_(
        submesh.primitiveType,
        submesh.indexCount,
        submesh.indexType,
        submesh.indexBuffer.buffer,
        submesh.indexBuffer.offset,
        len(self.nodes),
      )


# 2

# Swift: var pointer = instanceBuffer.contents().bindMemory(...)
# Python: 先頭のメモリアドレス(整数)を pointer として取得
pointer = ctypes.cast(instanceBuffer.contents, ctypes.c_void_p).value

# Swift の `pointer.pointee` の役割を果たすデータコンテナ
pointee = ModelConstants()

# Swift: for node in nodes
for node in self.nodes:

  # Swift: pointer.pointee.xxx = ...
  pointee.modelViewMatrix = matrix_multiply(modelViewMatrix, node.modelMatrix)
  pointee.materialColor = node.materialColor
  pointee.normalMatrix = matrix_multiply(modelViewMatrix,
                                         node.modelMatrix).upperLeft3x3()
  pointee.shininess = node.shininess
  pointee.specularIntensity = node.specularIntensity

  # Python固有の処理: pointee (ModelConstants) に詰めたデータを、現在の pointer の位置へ書き込む
  ctypes.memmove(pointer, pointee.raw, ModelConstants.size)

  # Swift: pointer = pointer.advanced(by: 1)
  # Python: 1つ分のサイズ (144バイト) アドレスを進める
  pointer += ModelConstants.size

