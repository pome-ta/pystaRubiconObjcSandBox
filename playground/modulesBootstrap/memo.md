# 📝 2026/11/09

いや、root ディレクトリに`bootstrap.py` は、意味なさすぎ？
わざわざトップに顔を出す必要あるか？

a-shell で、`python -m app` 実行すると、親ディレクトリを拾う。


```
hoge
file_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/__main__.py
hoge_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/bootstrap.py

sys.path:
---
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python313.zip
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/lib-dynload
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/site-packages

```


```
hoge
file_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/__main__.py
hoge_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/bootstrap.py

sys.path:
---
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python313.zip
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/lib-dynload
---
/private/var/containers/Bundle/Application//a-Shell-mini.app/Library/lib/python3.13/site-packages

```



```
hoge
file_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/__main__.py
hoge_path:
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/bootstrap.py

sys.path:
---
/private/var/mobile/Containers/Shared/AppGroup//File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app
---
/private/var/mobile/Containers/Shared/AppGroup//Pythonista3/Documents/site-packages-3
---
/private/var/mobile/Containers/Shared/AppGroup//Pythonista3/Documents/site-packages
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages/pythonista
---
/var/containers/Bundle/Application//Pythonista3.app/Frameworks/Py3Kit.framework/pylib/site-packages/PIL_compat


```


# 📝 2026/11/08

`bootstrap.py` から、module をいい感じに取り回す。

今までは、`playground` としていだが、`app` ？`src` ？

UIKitCatalog なら、`catalog` とかにするかな？
