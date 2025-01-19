# 📝 2025/01/19

## `0.5.0` と`0.4.9` のアプデ差分調査隊

[Commit f96b05f](https://github.com/pome-ta/pystaUIKitCatalogChallenge/commit/f96b05f1d457f171dc99933f24a7474fc1dcfa20)


### `api.py`


ここ意外は、Python のバージョン対応的な？

#### `get_method_family`

メソッド名からメソッドファミリーを返します。詳細は [https://clang.llvm.org/docs/AutomaticReferenceCounting.html#method-families](https://clang.llvm.org/docs/AutomaticReferenceCounting.html#method-families) を参照してください。


`ObjCMethod` 内部で呼び出してる



#### `autorelease` 落ちる原因のやつ？

[https://github.com/pome-ta/pystaUIKitCatalogChallenge/commit/f96b05f1d457f171dc99933f24a7474fc1dcfa20#diff-68c9a4c440f635fcd67968724f5042d016dc8ba6a8492eb0417357d3f095a7bfR99](https://github.com/pome-ta/pystaUIKitCatalogChallenge/commit/f96b05f1d457f171dc99933f24a7474fc1dcfa20#diff-68c9a4c440f635fcd67968724f5042d016dc8ba6a8492eb0417357d3f095a7bfR99)

- 0.4.9

つまり、「:meth:`alloc`」、「:meth:`new`」、「:meth:`copy`」、「:meth:`mutableCopy`」で始まるメソッドによって返され、「:meth:`release`」または「:meth:`autorelease`」を呼び出して明示的に解放されていない場合です。

- 0.5.0

Pythonラッパーのガベージコレクションに関するリファレンスをオートリリースします。ファクトリーメソッドからオブジェクトが返されたときに、ObjCがオブジェクトの所有権を取得できるようにするために、releaseの代わりにautoreleaseを使用します。







# 📝 2025/01/18

## `0.5.0` で画面遷移（戻る時）に落ちる



## スプレッドシート

[pystaUIKitCatalogChallenge - Google ドライブ](https://docs.google.com/spreadsheets/d/1T89HXVPCAcrjSLCM0LQtge9vifG3Hhu-VwMGDD1P4vw/htmlview#gid=0)


### ファイルリンク先

- [_main](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/_main.py)
  - Storyboard: 
- [outlineViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/outlineViewController.py)
  - Storyboard: 
- [caseElement](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/caseElement.py)
  - Storyboard: 
- [baseTableViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/baseTableViewController.py)
  - Storyboard: 
- [buttonViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/buttonViewController.py)
  - Storyboard: 
- [menuButtonViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/menuButtonViewController.py)
  - Storyboard: 
- [defaultPageControlViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/defaultPageControlViewController.py)
  - Storyboard: 
- [customPageControlViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/customPageControlViewController.py)
  - Storyboard: 
- [defaultSearchBarViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/defaultSearchBarViewController.py)
  - Storyboard: 
- [customSearchBarViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/customSearchBarViewController.py)
  - Storyboard: 
- [segmentedControlViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/segmentedControlViewController.py)
  - Storyboard: 
- [sliderViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/sliderViewController.py)
  - Storyboard: 
- [switchViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/switchViewController.py)
  - Storyboard: 
- [textFieldViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/textFieldViewController.py)
  - Storyboard: 
  - `property` 不要？
  - `UITextFieldDelegate` 不要？
- [stepperViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/stepperViewController.py)
  - Storyboard: 
- [activityIndicatorViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/activityIndicatorViewController.py)
  - Storyboard: 
- [alertControllerViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/alertControllerViewController.py)
  - Storyboard: 
- [textViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/textViewController.py)
  - Storyboard: 
- [imageViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/imageViewController.py)
  - Storyboard: 
- [symbolViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/symbolViewController.py)
  - Storyboard: 
- [progressViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/progressViewController.py)
  - Storyboard: 
- [stackViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/stackViewController.py)
  - Storyboard: 
- [defaultToolbarViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/defaultToolbarViewController.py)
  - Storyboard: 
- [tintedToolbarViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/tintedToolbarViewController.py)
  - Storyboard: 
- [customToolbarViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/customToolbarViewController.py)
  - Storyboard: 
- [visualEffectViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/visualEffectViewController.py)
  - Storyboard: 
- [webViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/webViewController.py)
  - Storyboard: 
- [datePickerController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/datePickerController.py)
  - Storyboard: 
- [colorPickerViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/colorPickerViewController.py)
  - Storyboard: 
- [fontPickerViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/fontPickerViewController.py)
  - Storyboard: 
- [imagePickerViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/imagePickerViewController.py)
  - Storyboard: 
- [pickerViewController](https://github.com/pome-ta/pystaRubiconObjcSandBox/blob/main/sandbox/rubiconUpdate050/pickerViewController.py)
  - Storyboard: 
