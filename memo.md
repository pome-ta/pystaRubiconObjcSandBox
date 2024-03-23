# 📝 2024/03/23

## objc_util からrubicon-objc の書き換え

書き味が変わってくるので、一旦整理として

### Class

Python のclass の書き方で、継承についても、そのclass を引数で入れるだけ

objc 内での変数として定義したい場合には、`objc_property()` で、class の頭に書く（`__init__` は呼ばない）

 メソッドは、`@objc_method` とデコレータをつけてあげると、objc のメソッドとなる

 オーバーライドも、`super` 呼び出しもすんなりといける感じ

# 📝 2024/03/22

pyto との名前衝突回避のために`py` をつけた
