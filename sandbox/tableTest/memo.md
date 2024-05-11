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
