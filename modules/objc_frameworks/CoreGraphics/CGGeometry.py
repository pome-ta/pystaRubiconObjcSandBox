from pyrubicon.objc.types import CGPoint, CGRect
from .constants import framework as CoreGraphics

CGPointZero = CGPoint.in_dll(CoreGraphics, 'CGPointZero')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

