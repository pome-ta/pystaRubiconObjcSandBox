from pyrubicon.objc import NSUInteger  #ntypes

from .constants import framework as ARKit

ARSCNDebugOptionShowFeaturePoints = NSUInteger.in_dll(
  ARKit, 'ARSCNDebugOptionShowFeaturePoints').value
showFeaturePoints = ARSCNDebugOptionShowFeaturePoints

ARSCNDebugOptionShowWorldOrigin = NSUInteger.in_dll(
  ARKit, 'ARSCNDebugOptionShowWorldOrigin').value
showWorldOrigin = ARSCNDebugOptionShowWorldOrigin

