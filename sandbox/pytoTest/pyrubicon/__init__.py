# [Pyto/Lib/rubicon/__init__.py at main · ColdGrub1384/Pyto · GitHub](https://github.com/ColdGrub1384/Pyto/blob/main/Lib/rubicon/__init__.py)

try:
  # If we're on iOS, we won't have pkg-resources; but then,
  # we won't need to register the namespace package, either.
  # Ignore the error if it occurs.
  __import__("pkg_resources").declare_namespace(__name__)
except ImportError:
  pass

