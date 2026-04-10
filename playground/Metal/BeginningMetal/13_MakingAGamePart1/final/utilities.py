from rbedge.simd import simd_float4


def colorNumber_(number: float) -> simd_float4:
  x = number
  r: float = 0.0
  g: float = 0.0
  b: float = 1.0

  if x >= 0.0 and x < 0.2:
    x = x / 0.2
    r = 0.0
    g = x
    b = 1.0
  elif x >= 0.2 and x < 0.4:
    x = (x - 0.2) / 0.2
    r = 0.0
    g = 1.0
    b = 1.0 - x
  elif x >= 0.4 and x < 0.6:
    x = (x - 0.4) / 0.2
    r = x
    g = 1.0
    b = 0.0
  elif x >= 0.6 and x < 0.8:
    x = (x - 0.6) / 0.2
    r = 1.0
    g = 1.0 - x
    b = 0.0
  elif x >= 0.8 and x <= 1.0:
    x = (x - 0.8) / 0.2
    r = 1.0
    g = 0.0
    b = x

  return simd_float4(r, g, b, 1.0)


def generateColorsNumber_(number: int) -> [simd_float4]:
  colors = [simd_float4(0) for _ in range(number)]
  for i in range(number):
    colors[i] = colorNumber_((number - i) / number)
  return colors

