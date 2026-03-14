import ctypes
import operator


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

  @property
  def scalar_type(cls):
    return cls._fields_[0][1]


class _SimdMatrixMeta(type(ctypes.Structure)):

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
  def column_count(cls):
    return cls._fields_[0][1]._length_

  @property
  def vector_type(cls):
    return cls._fields_[0][1]._type_


class _SimdVector(ctypes.Structure, metaclass=_SimdMeta):

  _components_ = ''
  _aliases_ = {
    'r': 'x', 'g': 'y', 'b': 'z', 'a': 'w',
    's': 'x', 't': 'y', 'p': 'z', 'q': 'w',
  }  # yapf: disable


  def __init__(self, *values):
    component_count = len(self._components_)

    if len(values) == 1:
      components = [values[0]] * component_count
    else:
      components = list(values[:component_count])
      components += [0.0] * (component_count - len(components))

    if len(self._fields_) > component_count:
      components.append(0.0)

    super().__init__(*components)

  def _map_component(self, component):
    if component in self._components_:
      return component

    return self._aliases_.get(component)

  def _resolve(self, name):
    mapped = [self._map_component(char) for char in name]

    if any(component is None or component not in self._components_
           for component in mapped):
      return None

    return mapped

  def __len__(self):
    return len(self._components_)

  def __getitem__(self, index):
    return getattr(self, self._components_[index])

  def __setitem__(self, index, value):
    component = self._components_[index]
    setattr(self, component, float(value))

  def __iter__(self):
    for component in self._components_:
      yield getattr(self, component)

  def __repr__(self):

    values = ', '.join(
      str(getattr(self, component)) for component in self._components_)

    return f'{self.__class__.__name__}({values})'

  def __getattr__(self, name):
    if name.startswith('_'):
      raise AttributeError(name)

    components = self._resolve(name)

    if not components:
      raise AttributeError(name)

    values = [getattr(self, component) for component in components]

    vector_types = {
      2: simd_float2,
      3: simd_float3,
      4: simd_float4,
    }

    if len(values) == 1:
      return values[0]

    vector_type = vector_types.get(len(values))

    if vector_type:
      return vector_type(*values)

    raise AttributeError(name)

  def __setattr__(self, name, value):
    components = self._resolve(name)

    if not components or len(components) == 1:
      super().__setattr__(name, value)
      return

    if len(set(components)) != len(components):
      raise ValueError('duplicate swizzle assignment')

    values = list(value)

    if len(values) != len(components):
      raise ValueError('swizzle size mismatch')

    for component, component_value in zip(components, values):
      super().__setattr__(component, float(component_value))

  # --- vector math

  def _binary_op(self, other, op):
    if isinstance(other, self.__class__):
      values = [op(a, b) for a, b in zip(self, other)]

    elif isinstance(other, (int, float)):
      values = [op(a, other) for a in self]

    else:
      return NotImplemented

    return self.__class__(*values)

  def __add__(self, other):
    return self._binary_op(other, operator.add)

  def __sub__(self, other):
    return self._binary_op(other, operator.sub)

  def __mul__(self, other):
    return self._binary_op(other, operator.mul)

  def __truediv__(self, other):
    return self._binary_op(other, operator.truediv)

  def __rmul__(self, other):
    return self.__mul__(other)

  def __neg__(self):
    return self.__class__(*(-x for x in self))

# --- vectors
class simd_float2(_SimdVector):
  _components_ = 'xy'
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
  ]


class simd_float3(_SimdVector):
  _components_ = 'xyz'
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('_pad', ctypes.c_float),  # todo: padding
  ]


class simd_float4(_SimdVector):
  _components_ = 'xyzw'
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]


class simd_float4x4(ctypes.Structure):
  _fields_ = [
    ('columns', simd_float4 * 4),
  ]

