# 📝 2024/05/12

## `send_super` 調査


### 自作の場合

[自作呼び出し](https://github.com/pome-ta/pystaUIKitCatalogChallenge/blob/0c70d878ce5da71a0c2df4385f1309e6df1909f9/storyboard_ButtonViewController.py#L19)では、なんとかなってる？

```.py
objc_msgSendSuper = c.objc_msgSendSuper
objc_msgSendSuper.argtypes = [
  ctypes.c_void_p,  # super
  ctypes.c_void_p,  # selector
  ctypes.c_void_p,
  ctypes.c_void_p,
]
objc_msgSendSuper.restype = ctypes.c_void_p


class objc_super(ctypes.Structure):
  #ref: [id | Apple Developer Documentation](https://developer.apple.com/documentation/objectivec/id?language=objc)
  # ref: [Class | Apple Developer Documentation](https://developer.apple.com/documentation/objectivec/class?language=objc)
  _fields_ = [
    ('receiver', ctypes.c_void_p),  # encoding(b"@")
    ('super_class', ctypes.c_void_p),  # encoding(b"#")
  ]

def initWithStyle_reuseIdentifier_(_self, _cmd, _style, _reuseIdentifier):
  super_cls = class_getSuperclass(self.tableViewCell_instance)
  super_struct = objc_super(_self, super_cls)
  super_sel = sel('initWithStyle:reuseIdentifier:')

  _args = [
    ctypes.byref(super_struct),
    super_sel,
    _style,
    _reuseIdentifier,
  ]
  _this = objc_msgSendSuper(*_args)
  this = ObjCInstance(_this)
  self.init_cell(this)
  return _this
```

まずは、自作ので動かしてみるか？

### Rubicon のソースコード調査

#### `runtime.py` => `send_super`

- `libobjc = load_library("objc")`



↓ リンク死んでる

http://developer.apple.com/mac/library/documentation/cocoa/conceptual/objectivec/Articles/ocDefiningClasses.html#//apple_ref/doc/uid/TP30001163-CH12-BAJHDGAC

# 📝 2024/05/11

`0.4.9`


## アノテーション

``` .py
@objc_method
def tableView_numberOfRowsInSection_(self, tableView,
                                     section: NSInteger) -> NSInteger:

  return 1
```


- 引数`section`
  - `int` でも`NSInteger` でも可？
  - アノテーションを付けないと、`None` となる
- 返り型`NSInteger`
  - `int` でも、`NSInteger` でも可？
  - 返りの型を付けないと、cell が表示されない
    - `ctypes.c_void_p`
      - 問題なさそう？
    - `str`
      - そんな型は無いと怒られる
    - `float`
      - 出てくるcell がめちゃ増える

- 引数`tableView`
  - 型入れなくても可？
    - `UITableView` が入ってる
  - `int`, `ctypes.c_void_p`
    - 整数値が出るけど、桁数が違う

- `*` の型だと、不要とかある？
  - 必要なパターン確かあった気がしてる

``` str の型エラー
encoding_for_ctype
    return b"^" + encoding_for_ctype(ctype._type_)
AttributeError: type object 'str' has no attribute '_type_'

```
