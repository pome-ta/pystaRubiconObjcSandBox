import ctypes


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

  def __len__(self):
    return len(self._components_)

  def __getitem__(self, index):
    return getattr(self, self._components_[index])

  def __iter__(self):
    for component_name in self._components_:
      yield getattr(self, component_name)

  def __repr__(self):
    values = ', '.join(
      str(getattr(self, component_name))
      for component_name in self._components_)

    return f'{self.__class__.__name__}({values})'

  def _map_component(self, component):
    if component in self._components_:
      return component

    return self._aliases_.get(component)

  def _resolve(self, name):
    mapped = [self._map_component(character) for character in name]

    if any(component is None or component not in self._components_
           for component in mapped):
      return None

    return mapped

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


class Vertex(ctypes.Structure):
  _fields_ = [
    ('position', simd_float3),
    ('color', simd_float4),
    ('texture', simd_float2),
  ]




if __name__ == '__main__':
  Vertices = Vertex * 4
  vertices = Vertices(
      Vertex(  # v0
        position=(-1.0,  1.0,  0.0), color=(1.0, 0.0, 0.0, 1.0), texture=(0.0, 1.0)),
      Vertex(  # v1
        position=(-1.0, -1.0,  0.0), color=(0.0, 1.0, 0.0, 1.0), texture=(0.0, 0.0)),
      Vertex(  # v2
        position=( 1.0, -1.0,  0.0), color=(0.0, 0.0, 1.0, 1.0), texture=(1.0, 0.0)),
      Vertex(  # v3
        position=( 1.0,  1.0,  0.0), color=(1.0, 0.0, 1.0, 1.0), texture=(1.0, 1.0)),
    )  # yapf: disable

  print(ctypes.sizeof(vertices))
