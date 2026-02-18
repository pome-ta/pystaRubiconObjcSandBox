import ctypes
from enum import IntEnum

from pyrubicon.objc.api import ObjCInstance

from .constants import Metal


def MTLCreateSystemDefaultDevice() -> ObjCInstance:
  _function = Metal.MTLCreateSystemDefaultDevice
  _function.restype = ctypes.c_void_p
  return ObjCInstance(_function())


class MTLGPUFamily(IntEnum):
  #[doc(alias = "MTLGPUFamilyApple1")]
  apple1 = 1001
  #[doc(alias = "MTLGPUFamilyApple2")]
  apple2 = 1002
  #[doc(alias = "MTLGPUFamilyApple3")]
  apple3 = 1003
  #[doc(alias = "MTLGPUFamilyApple4")]
  apple4 = 1004
  #[doc(alias = "MTLGPUFamilyApple5")]
  apple5 = 1005
  #[doc(alias = "MTLGPUFamilyApple6")]
  apple6 = 1006
  #[doc(alias = "MTLGPUFamilyApple7")]
  apple7 = 1007
  #[doc(alias = "MTLGPUFamilyApple8")]
  apple8 = 1008
  #[doc(alias = "MTLGPUFamilyApple9")]
  apple9 = 1009
  #[doc(alias = "MTLGPUFamilyApple10")]
  apple10 = 1010
  #[doc(alias = "MTLGPUFamilyMac1")]
  #[deprecated]
  mac1 = 2001
  #[doc(alias = "MTLGPUFamilyMac2")]
  mac2 = 2002
  #[doc(alias = "MTLGPUFamilyCommon1")]
  common1 = 3001
  #[doc(alias = "MTLGPUFamilyCommon2")]
  common2 = 3002
  #[doc(alias = "MTLGPUFamilyCommon3")]
  common3 = 3003
  #[doc(alias = "MTLGPUFamilyMacCatalyst1")]
  #[deprecated]
  macCatalyst1 = 4001
  #[doc(alias = "MTLGPUFamilyMacCatalyst2")]
  #[deprecated]
  macCatalyst2 = 4002
  #[doc(alias = "MTLGPUFamilyMetal3")]
  metal3 = 5001
  #[doc(alias = "MTLGPUFamilyMetal4")]
  metal4 = 5002
  

