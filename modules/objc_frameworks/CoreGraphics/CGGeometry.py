from pyrubicon.objc.types import CGRect
from .constants import framework as CoreGraphics

CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

