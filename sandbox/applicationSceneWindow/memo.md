# 📝 2025/02/15

rubicon をa-shell でいい感じに起動したい

- 繰り返し呼んでも落ちない
- Pythonista3 と(なるべく)同じ挙動


## `UIWindowScene` を取得

[Xcode11以降で新しいUIWindowを追加する|U Log SugiyのLife Log](https://ulog.sugiy.com/xcode11uiwindow/) こんなことなので、取ってみる（もう、`sharedApplication.windows.firstObject()` ではないみたい）



a-shell(mini) は、`delegate` がある

### a-shell

```
<ObjCInstance: UIWindowScene at 0x11f8f39d0: <UIWindowScene: 0x1027c3440; role: UIWindowSceneSessionRoleApplication; activationState: UISceneActivationStateForegroundActive> {
    session = <UISceneSession: 0x30233df40; persistentIdentifier: B35E8616-120B-42BB-9AB4-A498AE0E5C8F> {
        configuration = <UISceneConfiguration: 0x3023d47c0; name: "Default Configuration">;
    };
    delegate = <a_Shell_mini.SceneDelegate: 0x1027ba880>;
    screen = <UIScreen: 0x1030c0640; bounds: {{0, 0}, {414, 896}}; mode: <UIScreenMode: 0x303632420; size = 828.000000 x 1792.000000>>;
    windows = {
        <UIWindow: 0x1027bc480; frame = (0 0; 414 896); autoresize = W+H; gestureRecognizers = <NSArray: 0x3036bd0e0>; layer = <UIWindowLayer: 0x303862700>>;
        <UITextEffectsWindow: 0x103261400; frame = (0 0; 414 896); opaque = NO; autoresize = W+H; layer = <UIWindowLayer: 0x303853630>>;
    }
}>
```

### Pythonista3

```
<ObjCInstance: UIWindowScene at 0x11e54d300: <UIWindowScene: 0x101118580; role: UIWindowSceneSessionRoleApplication; activationState: UISceneActivationStateForegroundActive> {
    session = <UISceneSession: 0x3027f9c80; persistentIdentifier: F13108D6-A3F8-4E52-B21A-E25E60F4E8B2> {
        configuration = <UISceneConfiguration: 0x3029b0440; name: 0x0>;
    };
    delegate = (nil);
    screen = <UIScreen: 0x102074640; bounds: {{0, 0}, {414, 896}}; mode: <UIScreenMode: 0x30320a740; size = 828.000000 x 1792.000000>>;
    windows = {
        <PA3PythonistaWindow: 0x10110de80; baseClass = UIWindow; frame = (0 0; 414 896); autoresize = W+H; gestureRecognizers = <NSArray: 0x3032df340>; layer = <UIWindowLayer: 0x303cac0c0>>;
        <UITextEffectsWindow: 0x102223700; frame = (0 0; 414 896); opaque = NO; autoresize = W+H; layer = <UIWindowLayer: 0x303c9f7e0>>;
    }
}>

```
