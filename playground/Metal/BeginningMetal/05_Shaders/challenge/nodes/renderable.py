from pyrubicon.objc.api import ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property

class Renderable(metaclass=ObjCProtocol):

  pipelineState: 'MTLRenderPipelineState!' = objc_property()
  vertexFunctionName: str = objc_property(object)
  fragmentFunctionName: str = objc_property(object)
  vertexDescriptor: 'MTLVertexDescriptor' = objc_property()

  @objc_method
  def buildPipelineStateWithDevice_(self, device):
    ...
    
