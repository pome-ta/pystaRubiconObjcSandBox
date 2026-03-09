import ctypes

#from ctypes import Structure, c_float, sizeof, alignment


class _SimdMeta(type(ctypes.Structure)):

  @property
  def stride(cls):
    return ctypes.sizeof(cls)

  @property
  def size(cls):
    return ctypes.sizeof(cls)

  @property
  def alignment(cls):
    return ctypes.alignment(cls)

  @property
  def count(cls):
    return len(cls._components_)


class _SimdBase(ctypes.Structure, metaclass=_SimdMeta):

  _components_ = ''
  _aliases_ = {
    'r': 'x', 'g': 'y', 'b': 'z', 'a': 'w',
    's': 'x', 't': 'y', 'p': 'z', 'q': 'w',
  }  # yapf: disable

  def __init__(self, *values):

    n = len(self._components_)
    vals = list(values[:n])
    vals += [0.0] * (n - len(vals))

    if len(self._fields_) > n:
      vals.append(0.0)

    super().__init__(*vals)

  def __len__(self):
    return len(self._components_)

  def __getitem__(self, item_index):
    return getattr(self, self._components_[item_index])

  def __iter__(self):
    for comp in self._components_:
      yield getattr(self, comp)

  def __repr__(self):
    vals = ', '.join(
      str(getattr(self, component)) for component in self._components_)
    return f'{self.__class__.__name__}({vals})'

  def _map_comp(self, comp):

    if comp in self._components_:
      return comp

    return self._aliases_.get(comp)

  def _resolve(self, name):

    mapped = []
    comps = self._components_

    for c in name:
      m = self._map_comp(c)
      if m not in comps:
        return None
      mapped.append(m)

    return mapped

  def __getattr__(self, name):

    comps = self._resolve(name)

    if not comps:
      raise AttributeError(name)

    values = [getattr(self, comp) for comp in comps]
    k = len(values)

    match len(values):
      case 1:
        return values[0]
      case 2:
        return simd_float2(*values)
      case 3:
        return simd_float3(*values)
      case 4:
        return simd_float4(*values)
      case _:
        raise AttributeError(name)
    '''
    if k == 1:
      return values[0]

    if k == 2:
      return simd_float2(*values)

    if k == 3:
      return simd_float3(*values)

    if k == 4:
      return simd_float4(*values)

    raise AttributeError(name)
    '''

  def __setattr__(self, name, value):

    comps = self._resolve(name)

    if comps and len(comps) > 1:

      if len(set(comps)) != len(comps):
        raise ValueError('duplicate swizzle assignment')

      vals = list(value)

      if len(vals) != len(comps):
        raise ValueError('swizzle size mismatch')

      for c, v in zip(comps, vals):
        super().__setattr__(c, float(v))

      return

    super().__setattr__(name, value)


class simd_float2(_SimdBase):

  _components_ = 'xy'

  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
  ]


class simd_float3(_SimdBase):

  _components_ = 'xyz'

  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('_pad', ctypes.c_float),  # todo: padding
  ]


class simd_float4(_SimdBase):

  _components_ = 'xyzw'

  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]



Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)
Texture = (ctypes.c_float * 2)


class Vertex(ctypes.Structure):
  _fields_ = [
    ('position', Position),
    ('color', Color),
    ('texture', Texture),
  ]

