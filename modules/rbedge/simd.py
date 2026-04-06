import ctypes
import operator
from math import sqrt


class _SimdVectorMeta(type(ctypes.Structure)):
  _VECTOR_TYPES = {}

  def __init__(cls, name, bases, namespace):
    super().__init__(name, bases, namespace)

    components = getattr(cls, '_components_', None)

    if components:
      self_dim = len(components)
      _SimdVectorMeta._VECTOR_TYPES[self_dim] = cls

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
  def component_type(cls):
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
  def column_vector_type(cls):
    return cls._fields_[0][1]._type_


class _SimdVector(ctypes.Structure, metaclass=_SimdVectorMeta):
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
    if not 0 <= index < len(self):
      raise IndexError
    return getattr(self, self._components_[index])

  def __setitem__(self, index, value):
    if not 0 <= index < len(self):
      raise IndexError
    component = self._components_[index]
    setattr(self, component, float(value))

  def __iter__(self):
    for component in self._components_:
      yield object.__getattribute__(self, component)

  def __repr__(self):
    values = ', '.join(f'{getattr(self, component):.4f}'
                       for component in self._components_)

    return f'{self.__class__.__name__}({values})'

  def __getattr__(self, name):
    if name.startswith('_'):
      raise AttributeError(name)

    components = self._resolve(name)

    if components is None:
      raise AttributeError(name)

    values = [getattr(self, c) for c in components]

    if len(values) == 1:
      return values[0]

    vector_type = type(self)._VECTOR_TYPES.get(len(values))

    if vector_type:
      return vector_type(*values)

    raise AttributeError(name)

  def __setattr__(self, name, value):
    if name.startswith('_'):
      super().__setattr__(name, value)
      return
    components = self._resolve(name)

    if not components or len(components) == 1:
      super().__setattr__(name, value)
      return

    if len(set(components)) != len(components):
      raise ValueError('duplicate swizzle assignment')

    try:
      values = list(value)
    except TypeError:
      raise TypeError('swizzle assignment requires iterable')

    if len(values) != len(components):
      raise ValueError('swizzle size mismatch')

    for component, component_value in zip(components, values):
      super().__setattr__(component, float(component_value))

  # --- vector math operator
  def _binary_op(self, other, op):
    if hasattr(other, 'value'):
      other = other.value

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

  # --- simd math

  def dot(self, other):
    if len(self) != len(other):
      raise ValueError('vector size mismatch')

    return sum(a * b for a, b in zip(self, other))

  def length_squared(self):
    return self.dot(self)

  def length(self):
    return sqrt(self.length_squared())

  def normalize(self):
    l = self.length()

    if l == 0:
      return self.__class__()

    return self / l


class _SimdMatrix(ctypes.Structure, metaclass=_SimdMatrixMeta):

  def __getitem__(self, index):
    if not 0 <= index < len(self):
      raise IndexError
    return self.columns[index]

  def __setitem__(self, index, value):
    if not 0 <= index < len(self):
      raise IndexError
    self.columns[index] = value

  def __len__(self):
    return type(self).column_count

  def __iter__(self):
    return iter(self.columns)

  def __repr__(self):
    cols = len(self.columns)
    rows = len(self.columns[0])

    lines = []

    for r in range(rows):
      row = []
      for c in range(cols):
        row.append(f'{self.columns[c][r]:.4f}')
      lines.append(' '.join(row))

    return '\n'.join(lines)


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
    ('_pad', ctypes.c_float),  # padding (SIMD alignment)
  ]


class simd_float4(_SimdVector):
  _components_ = 'xyzw'
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]
  #_align_ = 16


# --- matrix
class simd_float3x3(_SimdMatrix):
  _fields_ = [
    ('columns', simd_float3 * 3),
  ]


class simd_float4x4(_SimdMatrix):
  _fields_ = [
    ('columns', simd_float4 * 4),
  ]


def matrix_multiply(a: simd_float4x4, b: simd_float4x4) -> simd_float4x4:

  result = type(a)()

  for c in range(4):
    for r in range(4):

      result.columns[c][r] = (a.columns[0][r] * b.columns[c][0] +
                              a.columns[1][r] * b.columns[c][1] +
                              a.columns[2][r] * b.columns[c][2] +
                              a.columns[3][r] * b.columns[c][3])

  return result


if __name__ == '__main__':
  pass

