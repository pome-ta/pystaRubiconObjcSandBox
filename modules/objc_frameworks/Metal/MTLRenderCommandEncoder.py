from enum import IntEnum


class MTLPrimitiveType(IntEnum):
  #[doc(alias = "MTLPrimitiveTypePoint")]
  point = 0
  #[doc(alias = "MTLPrimitiveTypeLine")]
  line = 1
  #[doc(alias = "MTLPrimitiveTypeLineStrip")]
  lineStrip = 2
  #[doc(alias = "MTLPrimitiveTypeTriangle")]
  triangle = 3
  #[doc(alias = "MTLPrimitiveTypeTriangleStrip")]
  triangleStrip = 4

