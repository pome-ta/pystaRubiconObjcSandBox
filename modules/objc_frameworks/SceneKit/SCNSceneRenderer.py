from enum import IntEnum, IntFlag


class SCNRenderingAPI(IntEnum):
  metal = 0
  openGLES2 = 1


class SCNDebugOptions(IntFlag):
  none = 0
  showPhysicsShapes = 1 << 0
  showBoundingBoxes = 1 << 1
  showLightInfluences = 1 << 2
  showLightExtents = 1 << 3
  showPhysicsFields = 1 << 4
  showWireframe = 1 << 5
  renderAsWireframe = 1 << 6
  showSkeletons = 1 << 7
  showCreases = 1 << 8
  showConstraints = 1 << 9
  showCameras = 1 << 10

