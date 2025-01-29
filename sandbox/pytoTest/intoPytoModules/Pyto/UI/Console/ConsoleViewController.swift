//
//  ConsoleViewController.swift
//  Pyto
//
//  Created by Emma Labbé on 9/8/18.
//  Copyright © 2018-2021 Emma Labbé. All rights reserved.
//

import UIKit
import WebKit
import Pipable
import AVKit
import QuickLook
#if MAIN
import InputAssistant
import SavannaKit
import SourceEditor
import SwiftUI
#endif

/// A View controller containing Python script output.
@objc open class ConsoleViewController: UIViewController, WKNavigationDelegate, WKScriptMessageHandler, PictureInPictureDelegate, ParserDelegate, QLPreviewControllerDataSource, QLPreviewControllerDelegate, UIDropInteractionDelegate {
            
    #if MAIN
    static func set(theme: Theme, for userInterfaceStyle: UIUserInterfaceStyle) {
        let themeID: Int
        
        switch theme {
        case is XcodeLightTheme:
            if userInterfaceStyle == .light {
                themeID = 0
            } else {
                themeID = -1
            }
        case is XcodeDarkTheme:
            if userInterfaceStyle == .dark {
                themeID = 0
            } else {
                themeID = 1
            }
        case is BasicTheme:
            themeID = 2
        case is DuskTheme:
            themeID = 3
        case is LowKeyTheme:
            themeID = 4
        case is MidnightTheme:
            themeID = 5
        case is SunsetTheme:
            themeID = 6
        case is WWDC16Theme:
            themeID = 7
        case is CoolGlowTheme:
            themeID = 8
        case is SolarizedLightTheme:
            themeID = 9
        case is SolarizedDarkTheme:
            themeID = 10
        default:
            themeID = -2
        }
        
        if themeID == -2 {
            UserDefaults.standard.set(theme.data, forKey: "theme\(userInterfaceStyle == .dark ? ".dark" : ".light")")
            UserDefaults.standard.synchronize()
        } else {
            UserDefaults.standard.set(themeID, forKey: "theme\(userInterfaceStyle == .dark ? ".dark" : ".light")")
            UserDefaults.standard.synchronize()
        }
        
        var _theme: Theme?
        
        for scene in UIApplication.shared.connectedScenes {
            guard let style = (scene.delegate as? UIWindowSceneDelegate)?.window??.traitCollection.userInterfaceStyle else {
                continue
            }
            _theme = self.theme(for: style)
            (scene.delegate as? UIWindowSceneDelegate)?.window??.tintColor = _theme?.tintColor
            (scene.delegate as? UIWindowSceneDelegate)?.window??.overrideUserInterfaceStyle = (_theme ?? theme).userInterfaceStyle
        }
        
        NotificationCenter.default.post(name: ThemeDidChangeNotification, object: _theme ?? theme)
    }
    
    static func theme(for userInterfaceStyle: UIUserInterfaceStyle) -> Theme {
        if let data = UserDefaults.standard.data(forKey: "theme\(userInterfaceStyle == .dark ? ".dark" : ".light")"), let theme = ThemeFromData(data) {
            return theme
        }
        
        switch UserDefaults.standard.integer(forKey: "theme\(userInterfaceStyle == .dark ? ".dark" : ".light")") {
        case -1:
            return XcodeLightTheme()
        case 0:
            if userInterfaceStyle == .dark {
                return XcodeDarkTheme()
            } else {
                return XcodeLightTheme()
            }
        case 1:
            return XcodeDarkTheme()
        case 2:
            return BasicTheme()
        case 3:
            return DuskTheme()
        case 4:
            return LowKeyTheme()
        case 5:
            return MidnightTheme()
        case 6:
            return SunsetTheme()
        case 7:
            return WWDC16Theme()
        case 8:
            return CoolGlowTheme()
        case 9:
            return SolarizedLightTheme()
        case 10:
            return SolarizedDarkTheme()
        default:
            return XcodeLightTheme()
        }
    }
    
    private static var previousTheme: Theme?
    
    static var choosenTheme: Theme {
        get {
            
            let style = UIWindow().traitCollection.userInterfaceStyle
            
            let theme = self.theme(for: style)
            
            if previousTheme?.data != theme.data {
                for scene in UIApplication.shared.connectedScenes {
                    guard let _window = (scene.delegate as? UIWindowSceneDelegate)?.window, let window = _window else {
                        continue
                    }
                    
                    if window.tintColor != theme.tintColor {
                        window.tintColor = theme.tintColor
                    }
                    
                    if window.traitCollection.userInterfaceStyle != theme.userInterfaceStyle {
                        window.overrideUserInterfaceStyle = theme.userInterfaceStyle
                    }
                }
            }
            
            previousTheme = theme
            
            return theme
        }
        
        set {
            var style = UITraitCollection.current.userInterfaceStyle
            
            for scene in UIApplication.shared.connectedScenes {
                guard let _style = (scene.delegate as? UIWindowSceneDelegate)?.window??.traitCollection.userInterfaceStyle else {
                    continue
                }
                
                style = _style
                break
            }
            
            set(theme: newValue, for: style)
        }
    }
    
    /// The `EditorSplitViewController` associated with this console.
    @objc weak var editorSplitViewController: EditorSplitViewController?
    #endif
    
    
    /// Clears screen.
    @objc static func clearConsoleForPath(_ path: String?) {
        DispatchQueue.main.sync {
            #if MAIN
            for console in visibles {
                if console.editorSplitViewController?.editor?.document?.fileURL.path == path || path == nil {
                    console.clear()
                }
            }
            #else
            ConsoleViewController.visibles.first?.clear()
            #endif
        }
    }
    
    /// Clears screen.
    @objc func clear() {
        text = ""
        images = []
        print("\u{001b}[2J\u{001b}[H\u{001b}[3J")
    }
        
    /// The Web view showing the terminal.
    @objc public var webView = WebView()
    
    /// Load the terminal into the web view.
    func loadTerminal() {
        guard let url = Bundle.main.url(forResource: "terminal", withExtension: nil) else {
            return
        }
        webView.loadFileURL(url.appendingPathComponent("index.html"), allowingReadAccessTo: url)
    }
        
    /// The text contained in the terminal.
    public var text = ""
    
    /// The images displayed in the terminal.
    public var images = [UIImage]()
    
    /// If set to `true`, the user will not be able to input.
    var ignoresInput = false
    
    /// If set to `true`, the user will not be able to input.
    static var ignoresInput = false
    
    /// Get the console as plain text, without terminal stuff.
    ///
    /// - Parameters:
    ///     - completion: A block called when the text is ready. Takes the result as parameter.
    func getPlainText(_ completion: @escaping ((String) -> Void)) {
        class Delegate: ParserDelegate {
                        
            var completion: ((String) -> Void)?
            
            func parser(_ parser: Parser, didReceiveString string: NSAttributedString) {
                completion?(string.string)
            }
            
            func parserDidEndTransmission(_ parser: Parser) {
                
            }
        }
        
                    
        let delegate = Delegate()
        delegate.completion = completion
        
        let parser = Parser()
        parser.delegate = delegate
        parser.parse(text.data(using: .utf8) ?? Data())
        
    }
    
    /// Adds text to the terminal.
    ///
    /// - Parameters:
    ///     - text: The text to add.
    func print(_ text: String) {
        self.text += text
        
        let semaphore: DispatchSemaphore?
        if !Thread.isMainThread {
            semaphore = DispatchSemaphore(value: 0)
        } else {
            semaphore = nil
        }
        
        DispatchQueue.main.async { [weak self] in
            self?.webView.evaluateJavaScript("print('\(text.replacingOccurrences(of: "\n", with: "\n\r").data(using: .utf8)?.base64EncodedString() ?? "")')", completionHandler: { _, _ in
                if #available(iOS 15.0, *) {
                    self?.updatePIP()
                }
                semaphore?.signal()
            })
        }
    }
    
    /// Prints a link.
    ///
    /// - Parameters:
    ///     - text: The text to add.
    ///     - link: The link to add.
    func printLink(text: String, link: String) {
        self.text += "\u{1B}[32m"+text+"\u{1B}[39m"
        let _text = text.replacingOccurrences(of: "\n", with: "\n\r").data(using: .utf8)?.base64EncodedString() ?? ""
        let _link = link.replacingOccurrences(of: "\n", with: "\n\r").data(using: .utf8)?.base64EncodedString() ?? ""
        
        let semaphore: Python.Semaphore?
        if !Thread.isMainThread {
            semaphore = Python.Semaphore(value: 0)
        } else {
            semaphore = nil
        }
        
        PyWrapper.set { [weak self] in
            self?.webView.evaluateJavaScript("printLink('\(_text)', '\(_link)')", completionHandler: { _, _ in
                
                DispatchQueue.main.asyncAfter(deadline: .now()+0.1) {
                    if #available(iOS 15.0, *) {
                        self?.updatePIP()
                    }
                }
            })
            
            semaphore?.signal()
        }
    }
    
    /// Displays an image inline.
    ///
    /// - Parameters:
    ///     - image: The image to display.
    ///     - completionHandler: The code called after the image is displayed.
    func display(image: UIImage, completionHandler: ((Any?, Error?) -> Void)?) {
        guard let data = image.data?.base64EncodedString() else {
            return
        }
        
        let semaphore: Python.Semaphore?
        if !Thread.isMainThread {
            semaphore = Python.Semaphore(value: 0)
        } else {
            semaphore = nil
        }
        
        webView.evaluateJavaScript("showImage('data:image/png;base64,\(data)')", completionHandler: { a, b in
            
            self.images.append(image)
            
            self.webView.evaluateJavaScript("t.io.print(' '); sendHeight();") { (_, _) in
                completionHandler?(a, b)
                if #available(iOS 15.0, *) {
                    self.updatePIP()
                }
                
                semaphore?.signal()
            }
            
        })
    }
    
    #if MAIN
    private var scriptPath: String? {
        return editorSplitViewController?.editor?.document?.fileURL.path
    }
    #endif
    
    /// The text field used for sending input.
    var movableTextField: MovableTextField?
    
    /// Prompt sent by Python `input(prompt)` function.
    var prompt: String?
    
    /// Returns `false` if input should be ignored.
    var shouldRequestInput: Bool {
        #if MAIN
        let condition = (!self.ignoresInput && !ConsoleViewController.ignoresInput || self.parent is REPLViewController)
        #else
        let condition = (!ignoresInput && !ConsoleViewController.ignoresInput)
        #endif
        
        guard condition else {
            self.ignoresInput = false
            ConsoleViewController.ignoresInput = false
            return false
        }
        
        return true
    }
    
    var highlightInput = false
    
    func completeCode() {
        guard !input.isEmpty else {
            suggestions = []
            completions = []
            return
        }
        
        guard inputIndex >= input.count-1 else {
            suggestions = []
            completions = []
            return
        }
        
        guard self.highlightInput || isShellInput else {
            suggestions = []
            completions = []
            return
        }
        
        let url = (self.parent as? LocalsAndGlobalsREPLViewController)?.url ?? (self.parent as! EditorSplitViewController).editor?.document!.fileURL
        
        let completeCode: String
        if #available(iOS 15.0, *), isShellInput {
            completeCode = """
            completion = complete_shell_command(command\(editorSplitViewController?.editor?.shellID == nil ? "" : ", '\(editorSplitViewController!.editor!.shellID!)'"))
                suggestions = completion[0]
                completions = completion[1]
            """
        } else if self.highlightInput { // Yes, the indentation is good
            completeCode = """
            namespace = console.__repl_namespace__['\(url?.path.replacingOccurrences(of: "'", with: "\\'") ?? "")']
                script = jedi.Interpreter(command, [namespace])
                
                for completion in script.complete():
                    suggestions.append(completion.name)
                    completions.append(completion.complete)
            """
        } else {
            
            return
        }
        
        let code =
        """
        import threading
        threading.current_thread().script_path = '\(self.editorSplitViewController!.editor!.document!.fileURL.path.replacingOccurrences(of: "'", with: "\\'"))'
        try:
            import jedi
            import console
            import pyto
            from _codecompletion import complete_shell_command
        
            command = '\(input.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "'", with: "\\'"))'
            
            suggestions = []
            completions = []
        
            \(completeCode)
            pyto.ConsoleViewController.suggestions = suggestions
            pyto.ConsoleViewController.completions = completions
        except Exception:
            pass
        """
        
        func complete() {
            DispatchQueue.global().async { [weak self] in
                self?.isCompleting = true
                
                Thread {
                    Python.pythonShared?.perform(#selector(PythonRuntime.runCode(_:)), with: code)
                    self?.isCompleting = false
                }.start()
            }
        }
        
        if self.isCompleting { // A timer so it doesn't block the main thread
            self.codeCompletionTimer?.invalidate()
            self.codeCompletionTimer = Timer.scheduledTimer(withTimeInterval: 0.001, repeats: true, block: { [weak self] (timer) in
                if self?.isCompleting == false && timer.isValid {
                    complete()
                    timer.invalidate()
                }
            })
        } else {
            complete()
        }
    }
    
    var input = "" {
        didSet {
            completeCode()
        }
    }
    
    var inputIndex = 0
    
    var secureTextEntry = false
    
    var isShellInput = false
    
    /// Requests the user for input.
    ///
    /// - Parameters:
    ///     - prompt: The prompt from the Python function.
    ///     - highlight: A boolean indicating whether the line should be syntax colored.
    func input(prompt: String, highlight: Bool, shell: Bool) {
        highlightInput = highlight
        secureTextEntry = false
        isShellInput = shell
        self.prompt = text.components(separatedBy: "\n").last ?? prompt
    }
    
    /// Requests the user for a password.
    ///
    /// - Parameters:
    ///     - prompt: The prompt from the Python function
    func getpass(prompt: String) {
        self.prompt = prompt
        highlightInput = false
        secureTextEntry = true
    }
    
    /// Closes the View controller and stops script.
    @objc func close() {
        
        #if MAIN
        extensionContext?.completeRequest(returningItems: nil, completionHandler: nil)
        
        if navigationController != nil {
            dismiss(animated: true, completion: {
                self.editorSplitViewController?.editor?.stop()
                DispatchQueue.main.asyncAfter(deadline: .now()+0.5, execute: { [weak self] in
                    
                    guard let self = self else {
                        return
                    }
                    
                    if let line = self.editorSplitViewController?.editor?.lineNumberError {
                        self.editorSplitViewController?.editor?.lineNumberError = nil
                        self.editorSplitViewController?.editor?.showErrorAtLine(line)
                    }
                })
            })
        }
        #else
        exit(0)
        #endif
    }
    
    #if MAIN
    /// Enables `'Done'` if Pip is running.
    @objc static func enableDoneButton() {
        DispatchQueue.main.async {
            for console in self.visibles {
                guard let doneButton = console.editorSplitViewController?.navigationItem.leftBarButtonItem else {
                    return
                }
                
                if #available(iOS 13.0, *) {
                    console.editorSplitViewController?.isModalInPresentation = false
                }
                
                (console.editorSplitViewController as? PipInstallerViewController)?.done = true
                
                if doneButton.action == #selector(PipInstallerViewController.closeViewController) {
                    doneButton.isEnabled = true
                }
            }
        }
    }
    #endif
    
    private static var shared = ConsoleViewController()
    
    /// All visible instances.
    @objc static let objcVisibles = NSMutableArray()
        
    private class DismisallDelegate: NSObject, UIAdaptivePresentationControllerDelegate {
        
        static var instances = [DismisallDelegate]() // Store them here so they aren't released
        
        override init() {
            super.init()
            Self.instances.append(self)
        }
        
        var semaphore: Python.Semaphore?
        
        func presentationControllerDidDismiss(_ presentationController: UIPresentationController) {
            semaphore?.signal()
        }
    }
    
    /// Returns when the passed view controller is dismissed.
    @objc static func waitForViewController(_ vc: UIViewController) {
        guard !Thread.isMainThread else {
            return
        }
        
        var delegate: DismisallDelegate!
        
        PyWrapper.set {
            delegate = vc.presentationController?.delegate as? DismisallDelegate
        }
        
        guard delegate != nil else {
            return
        }
        
        delegate.semaphore?.wait()
        
        if let i = DismisallDelegate.instances.firstIndex(of: delegate) {
            DismisallDelegate.instances.remove(at: i)
        }
    }
    
    /// All visible instances.
    @objc static var visibles: [ConsoleViewController] {
        get {
            var visibles = [ConsoleViewController]()
            
            func get() {
                for visible in objcVisibles {
                    if let console = visible as? ConsoleViewController, (console.view.window != nil || console.editorSplitViewController?.editor?.shouldRun == true) || console.editorSplitViewController is RunModuleViewController {
                        visibles.append(console)
                    }
                }
            }
            if !Thread.current.isMainThread {
                let semaphore = DispatchSemaphore(value: 0)
                DispatchQueue.main.async {
                    get()
                    semaphore.signal()
                }
                semaphore.wait()
            } else {
                get()
            }
            return visibles
        }
        
        set {
            objcVisibles.removeAllObjects()
            
            for element in newValue {
                if element.view.window != nil || element.editorSplitViewController?.editor?.shouldRun == true || element.editorSplitViewController is RunModuleViewController {
                    objcVisibles.add(element)
                }
            }
        }
    }
    
    // MARK: - Theme
    
    #if MAIN
    /// Setups the View controller interface for given theme.
    ///
    /// - Parameters:
    ///     - theme: The theme to apply.
    func setup(theme: Theme) {
        
        guard view.window?.windowScene?.activationState != .background && view.window?.windowScene?.activationState != .unattached && view.window != nil else {
            return
        }
        
        movableTextField?.theme = theme
        
        let backgroundColor: UIColor
        if parent?.superclass?.isSubclass(of: EditorSplitViewController.self) == true { // Is a subclass, use the default background color
            backgroundColor = theme.sourceCodeTheme.backgroundColor
        } else {
            backgroundColor = theme.consoleBackgroundColor
        }
        
        webView.backgroundColor = backgroundColor
        view.backgroundColor = backgroundColor
        
        if #available(iOS 13.0, *) {
            guard view.window?.windowScene?.activationState != .background else {
                return
            }
        }
        
        let foreground = theme.sourceCodeTheme.color(for: .plain)
        var red: CGFloat = 0
        var green: CGFloat = 0
        var blue: CGFloat = 0
        foreground.getRed(&red, green: &green, blue: &blue, alpha: nil)
        
        webView.evaluateJavaScript("""
        t.prefs_.set('foreground-color', '\(foreground.hexString)');
        t.prefs_.set('background-color', '\(backgroundColor.resolvedColor(with: traitCollection).hexString)');
        t.prefs_.set('cursor-color', 'rgba(\(red*255), \(green*255), \(blue*255), 0.5');
        t.prefs_.set('font-size', \(theme.sourceCodeTheme.font.pointSize));
        t.prefs_.set('font-family', '\(theme.sourceCodeTheme.font.familyName)');
        t.document_.body.style.color = '\(backgroundColor.hexString)';
        """, completionHandler: nil)
    }
    
    /// Called when the user choosed a theme.
    @objc func themeDidChange(_ notification: Notification?) {
        setup(theme: ConsoleViewController.choosenTheme)
    }
    
    deinit {
        NotificationCenter.default.removeObserver(self)
    }
    #endif
    
    /// The title of the terminal.
    var terminalTitle = ""
    
    /// The size of the terminal
    var terminalSize = (columns: 0, rows: 0)
    
    /// Sets `terminalSize`.
    func updateSize(_ columns: Int, _ rows: Int) {
        terminalSize = (columns: columns, rows: rows)
        (editorSplitViewController as? RunModuleViewController)?.setTitle(terminalTitle)
    }
    
    /// Returns the terminal size of the console with the given 
    @objc static func getTerminalSize(_ scriptPath: String?, fallback: NSArray) -> NSArray {
        guard let scriptPath = scriptPath else {
            return fallback
        }
        
        for console in visibles {
            if console.editorSplitViewController?.editor?.document?.fileURL.path == scriptPath {
                return NSArray(array: [console.terminalSize.columns, console.terminalSize.rows])
            }
        }
        
        return fallback
    }
    
    // MARK: - UI Presentation
    
    @available(iOS 13.0, *)
    class ViewController: UIViewController {
    
        func forAllSubviews(_ parent: UIView? = nil, execute: (UIView, inout Bool) -> ()) {
            guard let _parent = parent ?? view.subviews.first else {
                return
            }
            
            var stop = false
            execute(_parent, &stop)
            if stop {
                return
            }
            
            for view in _parent.subviews {
                forAllSubviews(view, execute: execute)
            }
        }
        
        var hasFirstResponder: Bool {
            var isFirstResponder = false
            
            forAllSubviews { view, stop in
                if view.isFirstResponder {
                    isFirstResponder = true
                    stop = true
                }
            }
            
            return isFirstResponder
        }
        
        override var canBecomeFirstResponder: Bool {
            true
        }
        
        @objc func close() {
            dismiss(animated: true, completion: nil)
        }
        
        func appear() {
            if let view = self.view.subviews.first {
                PyView.values[view]?.appearAction?.call(parameter: PyView.values[view]?.pyValue)
            }
        }
        
        func disappear() {
            if let view = self.view.subviews.first {
                PyView.values[view]?.disappearAction?.call(parameter: PyView.values[view]?.pyValue)
            }
        }
        
        override func pressesBegan(_ presses: Set<UIPress>, with event: UIPressesEvent?) {
            super.pressesBegan(presses, with: event)
            
            guard let first = presses.first, first.key != nil else {
                return
            }
            
            forAllSubviews { view, stop in
                guard let pyView = PyView.values[view] else {
                    return
                }
                
                if pyView.keyPressBegan != nil {
                    view.keyPressBegan(first)
                    stop = true
                }
            }
        }
        
        override func pressesEnded(_ presses: Set<UIPress>, with event: UIPressesEvent?) {
            super.pressesEnded(presses, with: event)
            
            guard let first = presses.first, first.key != nil else {
                return
            }
            
            forAllSubviews { view, stop in
                guard let pyView = PyView.values[view] else {
                    return
                }
                
                if pyView.keyPressEnded != nil {
                    view.keyPressEnded(first)
                    stop = true
                }
            }
        }
        
        override func viewDidLoad() {
            super.viewDidLoad()
            
            NotificationCenter.default.addObserver(self, selector: #selector(keyboardDidShow(notification:)), name: UIResponder.keyboardWillShowNotification, object: nil)
            NotificationCenter.default.addObserver(self, selector: #selector(keyboardDidShow(notification:)), name: UIResponder.keyboardDidShowNotification, object: nil)
            NotificationCenter.default.addObserver(self, selector: #selector(keyboardDidHide(notification:)), name: UIResponder.keyboardDidHideNotification, object: nil)
            NotificationCenter.default.addObserver(self, selector: #selector(keyboardDidShow(notification:)), name: UIResponder.keyboardWillChangeFrameNotification, object: nil)
            
            NotificationCenter.default.addObserver(forName: UIScene.didEnterBackgroundNotification, object: nil, queue: nil) { [weak self] (notif) in
                
                if let scene = self?.view.window?.windowScene, let object = notif.object as? NSObject, object == scene {
                    self?.disappear()
                }
            }
            
            NotificationCenter.default.addObserver(forName: UIScene.willEnterForegroundNotification, object: nil, queue: nil) { [weak self] (notif) in
                
                if let scene = self?.view.window?.windowScene, let object = notif.object as? NSObject, object == scene {
                    self?.appear()
                }
            }
            
            edgesForExtendedLayout = []
        }
        
        override func viewWillAppear(_ animated: Bool) {
            super.viewWillAppear(animated)
            
            view.subviews.first?.frame = view.safeAreaLayoutGuide.layoutFrame
            view.backgroundColor = view.subviews.first?.backgroundColor
            
            navigationItem.leftItemsSupplementBackButton = true
            navigationItem.leftBarButtonItems = view.subviews.first?.leftButtonItems as? [UIBarButtonItem]
            navigationItem.rightBarButtonItems = view.subviews.first?.rightButtonItems as? [UIBarButtonItem]
        }
        
        override func viewWillDisappear(_ animated: Bool) {
            super.viewWillDisappear(animated)
            
            let navVC = navigationController as? NavigationController
            if let uiView = view.subviews.first, let view = PyView.values[uiView], let i = navVC?.pyViews.firstIndex(of: view) {
                navVC?.pyViews.remove(at: i)
            }
            
            if let view = self.view.subviews.first, (navigationController?.viewControllers.count == 1 || navigationController?.viewControllers == nil) {
                PyView.values[view]?.isPresented = false
            }
        }
        
        override func viewDidDisappear(_ animated: Bool) {
            super.viewDidDisappear(animated)
            
            disappear()
        }
        
        override func viewDidAppear(_ animated: Bool) {
            super.viewDidAppear(animated)
            
            view.subviews.first?.frame = view.bounds
            
            if let uiView = view.subviews.first, let view = PyView.values[uiView] {
                let navVC = navigationController as? NavigationController
                if navVC?.pyViews.contains(view) == false {
                    navVC?.pyViews.append(view)
                }
                
                if let childNavView = view as? PyNavigationView, childNavView.view.backgroundColor == nil {
                    childNavView.view.backgroundColor = .systemBackground
                }
            }
            
            appear()
            
            if !hasFirstResponder {
                becomeFirstResponder()
            }
        }
        
        override func viewWillTransition(to size: CGSize, with coordinator: UIViewControllerTransitionCoordinator) {
            super.viewWillTransition(to: size, with: coordinator)
            
            coordinator.animate(alongsideTransition: { (_) in
            }) { (_) in
                if self.view.window?.windowScene?.activationState == .foregroundActive || self.view.window?.windowScene?.activationState == .foregroundInactive {
                    
                    self.view.subviews.first?.frame = self.view.bounds
                }
            }
        }
        
        override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
            super.traitCollectionDidChange(previousTraitCollection)
            
            /*if let view = self.view.subviews.first {
                PyView.values[view]?.updateBorderColor()
            }*/
        }
        
        @objc func keyboardDidShow(notification: NSNotification) {
            
            guard self == navigationController?.viewControllers.last && presentedViewController == nil else {
                return
            }
            
            guard let userInfo = notification.userInfo else { return }
            
            guard let r = (userInfo[UIResponder.keyboardFrameEndUserInfoKey] as? NSValue)?.cgRectValue else { return }
            
            guard r.origin.y > 0 else {
                self.view.subviews.first?.frame = self.view.bounds
                return
            }
            
            let point = (view.window)?.convert(r.origin, to: view) ?? r.origin
            
            view.subviews.first?.frame.size.height = point.y
        }
        
        @objc func keyboardDidHide(notification: NSNotification) {
            
            guard self == navigationController?.viewControllers.last && presentedViewController == nil else {
                return
            }
            
            self.view.subviews.first?.frame = self.view.bounds
        }
    }
    
    /// A Navigation Controller containing PytoUI views.
    @available(iOS 13.0, *)
    class NavigationController: UINavigationController {
        
        var pyViews = [PyView]() {
            didSet {
                let duplicates = pyViews.filter({ $0.view == pyViews.last?.view })
                if duplicates.count > 1, let i = pyViews.firstIndex(of: duplicates[0]) {
                    let original = pyViews.remove(at: i)
                    duplicates.last?.title = original.title
                    return
                }
                
                viewControllers.last?.title = pyViews.last?.title
            }
        }
        
        func setBarColor() {
            navigationBar.backgroundColor = pyViews.last?.backgroundColor?.color
            view.backgroundColor = pyViews.last?.backgroundColor?.color
        }
        
        override func viewWillAppear(_ animated: Bool) {
            super.viewWillAppear(animated)
            
            setBarColor()
        }
    }
    
    /// Returns `true` if any console is presenting an ui.
    @objc public static var isPresentingView: Bool {
        if #available(iOS 13.0, *) {
            for visibile in self.visibles {
                var presenting: Bool {
                    return (visibile.presentedViewController as? NavigationController) != nil
                }
                if Thread.current.isMainThread && presenting {
                    return true
                } else {
                    let semaphore = DispatchSemaphore(value: 0)
                    var flag = false
                    DispatchQueue.main.async {
                        flag = presenting
                        semaphore.signal()
                    }
                    semaphore.wait()
                    if flag {
                        return true
                    }
                }
            }
        }
        return false
    }
    
    /// Shows a view controller.
    ///
    /// - Parameters:
    ///     - viewController: The view controller to present.
    ///     - path: The path of the script that called this method.
    @available(iOS 13.0, *) @objc public static func showVC(_ viewController: UIViewController, onConsoleForPath path: String?) {
        
        let delegate = DismisallDelegate()
        delegate.semaphore = Python.Semaphore(value: 0)
        viewController.presentationController?.delegate = delegate
        
        #if WIDGET
        ConsoleViewController.visible.present(viewController, animated: true, completion: completion)
        #elseif !MAIN
        ConsoleViewController.visibles.first?.present(viewController, animated: true, completion: completion)
        #else
        for console in visibles {
            
            guard console.view.window != nil else {
                continue
            }
            
            func showView() {
                console.view.window?.topViewController?.present(viewController, animated: true, completion: nil)
            }
            
            if path == nil {
                showView()
                break
            } else if console.editorSplitViewController?.editor?.document?.fileURL.path == path {
                if console.presentedViewController != nil && !((console.presentedViewController as? UINavigationController)?.viewControllers.first is ScriptRunnerViewController) {
                    console.dismiss(animated: true) {
                        showView()
                    }
                    break
                } else {
                    showView()
                    break
                }
            }
        }
        #endif
    }
    
    /// Shows a given view initialized from Python.
    ///
    /// - Parameters:
    ///     - view: The view to present.
    ///     - path: The path of the script that called this method.
    @available(iOS 13.0, *) @objc public static func showView(_ view: Any, onConsoleForPath path: String?) {
        
        (view as? PyView)?.isPresented = true
        
        DispatchQueue.main.async {
            
            if let navView = view as? PyNavigationView, navView.view.backgroundColor == nil {
                navView.view.backgroundColor = .systemBackground
            }
            
            let size = CGSize(width: ((view as? PyView)?.width) ?? Double((view as! UIView).frame.width), height: ((view as? PyView)?.height) ?? Double((view as! UIView).frame.height))
            let vc = self.viewController((view as? PyView) ?? PyView(managed: view as! UIView), forConsoleWithPath: path)
            
            if vc.modalPresentationStyle == .pageSheet {
                if size == CGSize(width: 1, height: 1) {
                    vc.modalPresentationStyle = .formSheet
                } else if size == CGSize(width: 2, height: 2) {
                    vc.modalPresentationStyle = .pageSheet
                } else {
                    vc.preferredContentSize = size
                    vc.modalPresentationStyle = .formSheet
                }
            }
            
            let newScene = ((view as? PyView)?.presentationMode == PyView.PresentationModeNewScene)
            
            if newScene {
                if UIApplication.shared.supportsMultipleScenes {
                    SceneDelegate.viewControllerToShow = vc
                    let userActivity = NSUserActivity(activityType: "pytoui")
                    userActivity.addUserInfoEntries(from: ["scriptPath" : path ?? ""])
                    UIApplication.shared.requestSceneSessionActivation(nil, userActivity: userActivity, options: nil)
                    return
                } else {
                    (view as? PyView)?.presentationMode = PyView.PresentationModeFullScreen
                }
            }
            
            if path == nil || (newScene && UIApplication.shared.supportsMultipleScenes) {
               for scene in UIApplication.shared.connectedScenes {
                   
                   if newScene || (scene.userActivity?.userInfo!["scriptPath"] as? String) != path {
                       continue
                   }
                   
                   let window = (scene as? UIWindowScene)?.windows.first
                   if window?.isKeyWindow == true {
                       window?.topViewController?.present(vc, animated: true, completion: nil)
                       break
                   }
               }
            } else {
                self.showViewController(vc, scriptPath: path, completion: nil)
            }
        }
    }
    
    /// Shows a view controller from Python code.
    ///
    /// - Parameters:
    ///     - viewController: View controller to present.
    ///     - completion: Code called to setup the interface.
    @objc static func showViewController(_ viewController: UIViewController, scriptPath: String? = nil, completion: (() -> Void)?) {
        
        #if WIDGET
        ConsoleViewController.visible.present(viewController, animated: true, completion: completion)
        #elseif !MAIN
        ConsoleViewController.visibles.first?.present(viewController, animated: true, completion: completion)
        #else
        for console in visibles {
            
            guard viewController.presentingViewController == nil else {
                break
            }
            
            guard console.view.window != nil else {
                continue
            }
            
            guard console.view.window?.windowScene?.activationState == UIScene.ActivationState.foregroundActive || console.view.window?.windowScene?.activationState == UIScene.ActivationState.foregroundInactive else {
                continue
            }
            
            func showView() {
                console.view.window?.topViewController?.present(viewController, animated: true, completion: completion)
            }
            
            if scriptPath == nil {
                showView()
                break
            } else if console.editorSplitViewController?.editor?.document?.fileURL.path == scriptPath {
                if console.presentedViewController != nil && !((console.presentedViewController as? UINavigationController)?.viewControllers.first is ScriptRunnerViewController) {
                    console.dismiss(animated: true) {
                        showView()
                    }
                    break
                } else {
                    showView()
                    break
                }
            }
        }
        #endif
    }
    
    /// Creates a View controller to present
    ///
    /// - Parameters:
    ///     - view: The View to present initialized from Python.
    ///     - path: The script requesting for the View controller.
    ///
    /// - Returns: A ready to present View controller.
    @available(iOS 13.0, *) @objc public static func viewController(_ view: PyView, forConsoleWithPath path: String?) -> UIViewController {
        
        let vc = ViewController()
        vc.view.addSubview(view.view)
        
        #if MAIN
        if view.presentationMode == PyView.PresentationModeFullScreen {
            vc.modalPresentationStyle = .overFullScreen
        } else if view.presentationMode == PyView.PresentationModeWidget, let viewController = UIStoryboard(name: "Widget Simulator", bundle: Bundle.main).instantiateInitialViewController() {
            
            let widget = (viewController as? UINavigationController)?.viewControllers.first as? WidgetSimulatorViewController
            
            vc.modalPresentationStyle = .pageSheet
            widget?.pyView = view
            
            if let path = path {
                widget?.scriptURL = URL(fileURLWithPath: path)
            }
            
            return viewController
        }
        
        return vc
        #else
        view.viewController = vc
        return vc
        #endif
    }
    
    /// Closes the View controller presented by code.
    @objc func closePresentedViewController() {
        dismiss(animated: true, completion: nil)
    }
    
    private static func editor(in window: UIWindow) -> EditorSplitViewController? {
        [
            ((window.topViewController?.children.first as? UINavigationController)?.visibleViewController?.children.first as? EditorSplitViewController), // Debugger
        
            (window.topViewController as? EditorSplitViewController),
        
            (window.topViewController as? UINavigationController)?.visibleViewController as? EditorSplitViewController,
        
            ((window.windowScene?.delegate as? SceneDelegate)?.sidebarSplitViewController?.sidebar?.repl?.vc as? REPLViewController),
            
            ((window.windowScene?.delegate as? SceneDelegate)?.sidebarSplitViewController?.sidebar?.moduleRunner?.vc as? RunModuleViewController),
        
            (window.windowScene?.delegate as? SceneDelegate)?.sidebarSplitViewController?.sidebar?.editor?.vc as? EditorSplitViewController
        ].filter({
            $0?.view.window != nil
        }).first ?? nil
    }
    
    #if MAIN
    /// Code completions for the REPL.
    @objc static var completions = NSMutableArray() {
        didSet {
            if #available(iOS 13.0, *) {
                DispatchQueue.main.async {
                    for scene in UIApplication.shared.connectedScenes {
                        if let window = (scene as? UIWindowScene)?.windows.first {
                            if let vc = editor(in: window) {
                                vc.console?.completions = self.completions as? [String] ?? []
                            }
                        }
                    }
                }
            }
        }
    }
    
    /// Code suggestions for the REPL.
    @objc static var suggestions = NSMutableArray() {
        didSet {
            if #available(iOS 13.0, *) {
                DispatchQueue.main.async {
                    for scene in UIApplication.shared.connectedScenes {
                        if let window = (scene as? UIWindowScene)?.windows.first {
                            if let vc = editor(in: window) {
                                vc.console?.suggestions = self.suggestions as? [String] ?? []
                            }
                        }
                    }
                }
            }
        }
    }
    
    /// Returns suggestions for current word.
    @objc var suggestions: [String] {
        
        get {
            
            if _suggestions.indices.contains(currentSuggestionIndex) {
                var completions = _suggestions
                
                let completion = completions[currentSuggestionIndex]
                completions.remove(at: currentSuggestionIndex)
                completions.insert(completion, at: 0)
                return completions
            }
            
            return _suggestions
        }
        
        set {
            
            currentSuggestionIndex = -1
            
            _suggestions = newValue
        }
    }
    
    private var _completions = [String]()
    
    private var _suggestions = [String]()
    
    /// Completions corresponding to `suggestions`.
    @objc var completions: [String] {
        get {
            if _completions.indices.contains(currentSuggestionIndex) {
                var completions = _completions
                
                let completion = completions[currentSuggestionIndex]
                completions.remove(at: currentSuggestionIndex)
                completions.insert(completion, at: 0)
        
                return completions
            }
            
            return _completions
        }
        
        set {
            _completions = newValue
        
            DispatchQueue.main.async { [weak self] in
                self?.movableTextField?.inputAssistant.reloadData()
            }
        }
    }
    
    var currentSuggestionIndex = -1 {
        didSet {
            DispatchQueue.main.async { [weak self] in
                self?.movableTextField?.inputAssistant.reloadData()
            }
        }
    }
    #endif
    
    private var isCompleting = false
    
    private var codeCompletionTimer: Timer?
        
    private var wasFirstResponder = false
    
    @objc static var codeToHighlight: String?
    
    /// Handles the input.
    func handleInput(_ text: String) {
        #if MAIN
        if self.currentSuggestionIndex != -1 {
            return self.inputAssistantView(self.movableTextField!.inputAssistant, didSelectSuggestionAtIndex: 0)
        }
                    
        #endif

        self.movableTextField?.currentInput = nil
        self.movableTextField?.setPrompt("")

        let secureTextEntry = self.movableTextField?.textField.isSecureTextEntry ?? false
        self.movableTextField?.textField.isSecureTextEntry = false

        self.movableTextField?.textField.text = ""

        if !secureTextEntry && self.addToHistory {
            #if MAIN
            
            if let i = self.movableTextField?.history.firstIndex(of: text) {
                self.movableTextField?.history.remove(at: i)
            }
            self.movableTextField?.history.insert(text, at: 0)
            self.movableTextField?.historyIndex = -1
            
            self.completions = []
            #endif
        }

        self.addToHistory = true

        if !secureTextEntry {
            Python.shared.output += text
        }
        
        self.print("\n")

        #if MAIN
        DispatchQueue.main.asyncAfter(deadline: .now()+(self.highlightInput ? 0.1 : 0)) {
            PyInputHelper.userInput[self.editorSplitViewController?.editor?.document?.fileURL.path ?? ""] = text
        }
        #else
        PyInputHelper.userInput[""] = text
        #endif
    }
    
    // MARK: - View controller
    
    override open func viewDidLoad() {
        super.viewDidLoad()
        
        #if MAIN
        NotificationCenter.default.addObserver(self, selector: #selector(themeDidChange(_:)), name: ThemeDidChangeNotification, object: nil)
        
        NotificationCenter.default.addObserver(forName: UIScene.didActivateNotification, object: nil, queue: nil) { [weak self] (notif) in
            self?.themeDidChange(notif)
            
            if self?.wasFirstResponder == true {
                self?.wasFirstResponder = false
                self?.movableTextField?.textField.becomeFirstResponder()
            }
            self?.movableTextField?.applyTheme()
        }
        
        NotificationCenter.default.addObserver(forName: UIScene.didEnterBackgroundNotification, object: nil, queue: nil) { [weak self] (notif) in
            self?.wasFirstResponder = self?.movableTextField?.textField.isFirstResponder ?? false
        }
        #endif
        
        edgesForExtendedLayout = []
        
        title = NSLocalizedString("console", comment: "'Console' tab")
        
        webView.console = self
        webView.frame.size = view.frame.size
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight, .flexibleTopMargin, .flexibleBottomMargin, .flexibleLeftMargin, .flexibleRightMargin]
        webView.backgroundColor = .clear
        webView.isOpaque = false
        webView.configuration.userContentController.add(self, name: "pyto")
        webView.navigationDelegate = self
        webView.scrollView.alwaysBounceVertical = false
        webView.scrollView.bounces = false
        webView.scrollView.showsVerticalScrollIndicator = false
        webView.scrollView.showsHorizontalScrollIndicator = false
        view.addSubview(webView)
        
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillShow), name: UIResponder.keyboardWillShowNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillHide), name:UIResponder.keyboardWillHideNotification, object: nil)
        
        loadTerminal()
    }
    
    #if MAIN
    override open func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
        super.traitCollectionDidChange(previousTraitCollection)
        
        themeDidChange(nil)
        movableTextField?.applyTheme()
    }
    #endif
        
    open override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        
        guard view.window?.windowScene?.activationState == .foregroundActive || view.window?.windowScene?.activationState == .foregroundInactive else {
            return
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now()+0.5) {
            if self.view.window == nil {
                self.movableTextField?.inputAssistant.delegate = nil
                self.movableTextField?.textField.inputAccessoryView = nil
                self.movableTextField = nil
            }
        }
    }
    
    var addToHistory = true
    
    private var dropInteractionContainingView: UIView? = nil
    private var defaultDropInteractionToRemove: UIDropInteraction? = nil
    
    override open func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
                
        if !ConsoleViewController.visibles.contains(self) {
            ConsoleViewController.visibles.append(self)
        }
                
        if movableTextField == nil {
            movableTextField = MovableTextField(console: self)
            movableTextField?.setPrompt(prompt ?? "")
        }
        //movableTextField?.show()
        #if MAIN
        movableTextField?.inputAssistant.delegate = self
        movableTextField?.inputAssistant.dataSource = self
        #endif
        movableTextField?.handler = handleInput
        
        var items = [UIBarButtonItem]()
        func appendStop() {
            items.append(UIBarButtonItem(barButtonSystemItem: .stop, target: self, action: #selector(close)))
        }
        #if MAIN
        if !(parent is REPLViewController) {
            appendStop()
        }
        #else
        appendStop()
        #endif
        
        navigationItem.rightBarButtonItems = items
        
        #if MAIN
        setup(theme: ConsoleViewController.choosenTheme)
        #endif

        if dropInteractionContainingView == nil {
            for subview in webView.scrollView.subviews {
                for interaction in subview.interactions {
                    if let dropInteraction = interaction as? UIDropInteraction {
                        dropInteractionContainingView = subview
                        defaultDropInteractionToRemove = dropInteraction
                        break
                    }
                }
            }
            
            if let dropInteractionContainingView = dropInteractionContainingView, let defaultDropInteractionToRemove = defaultDropInteractionToRemove {
                let customDropInteraction = UIDropInteraction(delegate: self)
                dropInteractionContainingView.removeInteraction(defaultDropInteractionToRemove)
                dropInteractionContainingView.addInteraction(customDropInteraction)
            }
        }
    }
    
    override open func dismiss(animated flag: Bool, completion: (() -> Void)? = nil) {
        super.dismiss(animated: flag, completion: completion)
        
        #if MAIN
        themeDidChange(nil)
        #else
        if #available(iOS 13.0, *) {
            view.backgroundColor = .systemBackground
            navigationController?.view.backgroundColor = .systemBackground
        }
        #endif
    }
        
    open override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
                
        movableTextField?.toolbar.frame.size.width = view.safeAreaLayoutGuide.layoutFrame.width
        movableTextField?.toolbar.frame.origin.x = view.safeAreaInsets.left
        
        webView.frame.size = view.frame.size
        webView.frame.origin.y = 0
        webView.frame.origin.x = 0
        webView.subviews.first?.bounds.origin = .zero
        
        movableTextField?.toolbar.isHidden = (view.frame.size.height == 0)
        #if MAIN
        movableTextField?.applyTheme()
        #endif
        
        editorSplitViewController?.editor?.setToggleTerminalItemTitle()
    }
    
    // MARK: - Keyboard
    
    @objc func keyboardWillShow(_ notification:Notification) {
        webView.evaluateJavaScript("sendSize()", completionHandler: nil)
    }
    
    @objc func keyboardWillHide(_ notification:Notification) {
        webView.evaluateJavaScript("sendSize()", completionHandler: nil)
    }
    
    /// Overrides the input to the given string.
    func setInput(input: String) {
        self.input = input
        inputIndex = input.count
        self.print("\u{001b}[2K\r\(self.prompt ?? "")\(input)")
    }
    
    var printInputAfterSettingHistoryIndex = true
    
    /// The current command that is not in the history.
    var currentInput: String?
    
    /// The index of current input in the history. `-1` if the command is not in the history.
    var historyIndex = -1 {
        didSet {
            if historyIndex == -1 && printInputAfterSettingHistoryIndex {
                setInput(input: currentInput ?? "")
            } else if history.indices.contains(historyIndex) {
                setInput(input: history[historyIndex])
            }
            
            printInputAfterSettingHistoryIndex = true
        }
    }
    
    /// The history of input. This array is reversed. The first command in the history is the last in this array.
    var history: [String] {
        get {
            return (UserDefaults.standard.array(forKey: "inputHistory") as? [String]) ?? []
        }
        
        set {
            UserDefaults.standard.set(newValue, forKey: "inputHistory")
        }
    }

    @objc func doNothing() {
        Swift.print("Do nothing")
    }
    
    /// Selects a suggestion from hardware tab key.
    @objc func nextSuggestion() {
        
        #if MAIN
        guard numberOfSuggestionsInInputAssistantView() != 0 else {
            return
        }
                
        let new = currentSuggestionIndex+1
        
        if suggestions.indices.contains(new) {
            currentSuggestionIndex = new
        } else {
            currentSuggestionIndex = -1
        }
        #else
        fatalError("Not implemented")
        #endif
    }
    
    // MARK: - Preview controller data source
    
    var previewingImages = [ConsoleImagePreviewItem]()
    
    var previewController: QLPreviewController?
    
    public func numberOfPreviewItems(in controller: QLPreviewController) -> Int {
        previewingImages.count
    }
    
    public func previewController(_ controller: QLPreviewController, previewItemAt index: Int) -> QLPreviewItem {
        previewingImages[index]
    }
    
    // MARK: - Preview controller delegate
    
    public func previewControllerDidDismiss(_ controller: QLPreviewController) {
        previewingImages = []
    }
    
    // MARK: - Message handler
    
    public func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        
        if let title = (message.body as? [String:String])?["title"], let terminal = editorSplitViewController as? RunModuleViewController {
            terminalTitle = title
            terminal.setTitle(title)
            return
        }
        
        if let images = (message.body as? [String:Any]), let index = images["index"] as? Int, let sources = images["images"] as? [String] {
            
            var i = 0
            previewingImages = sources.compactMap({
                i += 1
                return ConsoleImagePreviewItem(base64EncodedString: $0, title: "\(i)")
            })
            previewController = QLPreviewController()
            previewController?.dataSource = self
            previewController?.delegate = self
            previewController?.currentPreviewItemIndex = index
            present(previewController!, animated: true)
        }
        
        guard let msg = message.body as? String else {
            return
        }
        
        switch msg {
        case "\u{001b}[D":
            webView.back()
        case "\u{001b}[C":
            webView.forward()
        case "\u{001b}[A":
            webView.up()
        case "\u{001b}[B":
            webView.down()
        case "\u{7f}":
            webView.backspace()
        case "\r":
            webView.enter()
        default:
            if msg.hasPrefix("size:"), let sizeData = msg.components(separatedBy: "size:").last?.data(using: .utf8) {
                
                do {
                    guard let info = try JSONSerialization.jsonObject(with: sizeData, options: []) as? [String : Float] else {
                        return
                    }
                    guard let columns = info["width"], let lines = info["height"] else {
                        return
                    }
                    updateSize(Int(columns), Int(lines))
                } catch {
                    Swift.print(error.localizedDescription)
                }
            } else if msg.hasPrefix("openlink:"), let link = msg.components(separatedBy: "openlink:").last, let url = URL(string: link) {
                
                UIApplication.shared.open(url, options: [:], completionHandler: nil)
            } else if msg == "\u{001b}[1;9D" {
                webView.previousTab()
            } else if msg == "\u{001b}[1;9C" {
                webView.nextTab()
            } else {
                webView.insert(chars: msg.replacingOccurrences(of: "\u{001b}", with: ""))
            }
        }        
    }
    
    // MARK: - Navigation delegate
    
    public func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        
        webView.evaluateJavaScript("window.voiceOver = \(UIAccessibility.isVoiceOverRunning); t.setAccessibilityEnabled(window.voiceOver)", completionHandler: nil)
        setup(theme: ConsoleViewController.choosenTheme)
        
        var isFirstResponder = webView.isFirstResponder
        for contentView in webView.scrollView.subviews {
            if contentView.classForCoder.description() == [
                "W",
                "K",
                "Con",
                "te",
                "nt",
                "View"
            ].joined(separator: "") {
                if contentView.isFirstResponder {
                    isFirstResponder = true
                }
                break
            }
        }
        
        if !isFirstResponder {
            webView.evaluateJavaScript("t.document_.activeElement.blur()")
        }
    }
    
    // MARK: - Color picker
    
    static fileprivate var colorPickerSemaphore: DispatchSemaphore?
    
    static fileprivate var pickedColor: UIColor?
    
    static private let colorPickerDelegate = ColorPickerDelegate()

    private class ColorPickerDelegate: NSObject, UIColorPickerViewControllerDelegate {
        
        @available(iOS 14.0, *)
        func colorPickerViewControllerDidFinish(_ viewController: UIColorPickerViewController) {
            ConsoleViewController.pickedColor = viewController.selectedColor
            ConsoleViewController.colorPickerSemaphore?.signal()
        }
        
        @available(iOS 14.0, *)
        func colorPickerViewControllerDidSelectColor(_ viewController: UIColorPickerViewController) {
            ConsoleViewController.pickedColor = viewController.selectedColor
        }
    }
    
    @available(iOS 14.0, *)
    @objc public static func pickColor(scriptPath: String?) -> PyColor? {
        
        if Thread.current.isMainThread {
            return nil
        }
        
        colorPickerSemaphore = DispatchSemaphore(value: 0)
        
        DispatchQueue.main.async {
            let picker = UIColorPickerViewController()
            picker.delegate = colorPickerDelegate
            
            #if WIDGET
            ConsoleViewController.visible.present(picker, animated: true, completion: nil)
            #elseif !MAIN
            ConsoleViewController.visibles.first?.present(picker, animated: true, completion: nil)
            #else
            for console in ConsoleViewController.visibles {
                
                if scriptPath == nil {
                    (console.presentedViewController ?? console).present(picker, animated: true, completion: nil)
                    break
                }
                
                if console.editorSplitViewController?.editor?.document?.fileURL.path == scriptPath {
                    (console.presentedViewController ?? console).present(picker, animated: true, completion: nil)
                    break
                }
            }
            #endif
        }
        
        colorPickerSemaphore?.wait()
        return pickedColor == nil ? nil : PyColor(managed: pickedColor!)
    }
    
    // MARK: - Font picker
    
    static fileprivate var fontPickerSemaphore: DispatchSemaphore?
    
    static fileprivate var pickedFont: UIFont?
    
    static private let fontPickerDelegate = FontPickerDelegate()

    private class FontPickerDelegate: NSObject, UIFontPickerViewControllerDelegate {
        
        func fontPickerViewControllerDidCancel(_ viewController: UIFontPickerViewController) {
            ConsoleViewController.pickedFont = nil
            ConsoleViewController.fontPickerSemaphore?.signal()
        }
        
        func fontPickerViewControllerDidPickFont(_ viewController: UIFontPickerViewController) {
            if let font = viewController.selectedFontDescriptor {
                ConsoleViewController.pickedFont = UIFont(descriptor: font, size: font.pointSize)
            }
            
            ConsoleViewController.fontPickerSemaphore?.signal()
        }
    }
    
    @objc public static func pickFont(scriptPath: String?) -> UIFont? {
        
        if Thread.current.isMainThread {
            return nil
        }
        
        fontPickerSemaphore = DispatchSemaphore(value: 0)
        
        DispatchQueue.main.async {
            let picker = UIFontPickerViewController()
            picker.delegate = fontPickerDelegate
            
            #if WIDGET
            ConsoleViewController.visible.present(picker, animated: true, completion: nil)
            #elseif !MAIN
            ConsoleViewController.visibles.first?.present(picker, animated: true, completion: nil)
            #else
            for console in ConsoleViewController.visibles {
                
                if scriptPath == nil {
                    (console.presentedViewController ?? console).present(picker, animated: true, completion: nil)
                    break
                }
                
                if console.editorSplitViewController?.editor?.document?.fileURL.path == scriptPath {
                    (console.presentedViewController ?? console).present(picker, animated: true, completion: nil)
                    break
                }
            }
            #endif
        }
        
        fontPickerSemaphore?.wait()
        return pickedFont
    }
    
    // MARK: - Picture in Picture
    
    let pipTextView = PipTextView()
    
    let pipVC = UIHostingController(rootView: ConsolePipView())
    
    class PipTextView: UITextView, Pipable {
        
        var pictureInPictureDelegate: PictureInPictureDelegate?
        
        var previewSize: CGSize {
            CGSize(width: 1024, height: 1024)
        }
        
        func willTakeSnapshot() {
            isHidden = false
        }
        
        func didTakeSnapshot() {
            isHidden = true
        }
    }
    
    func parser(_ parser: Parser, didReceiveString string: NSAttributedString) {
        let attr = NSMutableAttributedString(attributedString: string)
        attr.addAttributes([NSAttributedString.Key.font: EditorViewController.font.withSize(40),
                            NSAttributedString.Key.backgroundColor : UIColor.clear,
                            NSAttributedString.Key.foregroundColor : UIColor.label], range: NSRange(location: 0, length: attr.length))
        pipTextView.attributedText = attr
        if #available(iOS 15.0, *) {
            pipTextView.updatePictureInPictureSnapshot()
        }
    }
    
    func parserDidEndTransmission(_ parser: Parser) {
    }
    
    @available(iOS 15.0, *)
    func updatePIP(force: Bool = false) {
        
        if !force {
            guard pipTextView.pictureInPictureController?.isPictureInPictureActive == true else {
                return
            }
        }
        
        if let data = text.data(using: .utf8) {
            let parser = Parser()
            parser.delegate = self
            parser.parse(data)
        }
    }
    
    func togglePIP() {
        guard #available(iOS 15.0, *), let pip = pipTextView.pictureInPictureController else {
            return
        }
        
        if pipVC.parent == nil {
            pipVC.view.frame = view.frame
            pipVC.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
            pipVC.view.isHidden = true
            
            addChild(pipVC)
            view.addSubview(pipVC.view)
        }
        
        if pipTextView.superview == nil {
            pipTextView.frame.size = pipTextView.previewSize
            pipTextView.isEditable = false
            pipTextView.isHidden = true
            view.addSubview(pipTextView)
        }
        
        updatePIP(force: true)
        
        pipTextView.pictureInPictureDelegate = self
        
        if pip.isPictureInPictureActive {
            
            do {
                if BackgroundTask.count == 0 {
                    try AVAudioSession.sharedInstance().setActive(false, options: [])
                }
            } catch {
                print(error.localizedDescription)
            }
            
            pip.stopPictureInPicture()
        } else {
            
            pipTextView.pictureInPictureController?.invalidatePlaybackState()
            
            do {
                if BackgroundTask.count == 0 {
                    try AVAudioSession.sharedInstance().setCategory(.playback, options: .mixWithOthers)
                    try AVAudioSession.sharedInstance().setActive(true, options: [])
                }
            } catch {
                print(error.localizedDescription)
            }
            
            DispatchQueue.main.asyncAfter(deadline: .now()+0.1) {
                pip.startPictureInPicture()
            }
        }
    }
    
    public func didEnterPictureInPicture() {
        editorSplitViewController?.editor?.pipItem?.image = UIImage(systemName: "pip.exit")
        editorSplitViewController?.editor?.pipItem.title = NSLocalizedString("pip.exit", comment: "'Exit PIP'")
        editorSplitViewController?.editor?.setBarItems()
        pipVC.view.isHidden = false
    }
    
    public func didExitPictureInPicture() {
        editorSplitViewController?.editor?.pipItem?.image = UIImage(systemName: "pip.enter")
        editorSplitViewController?.editor?.pipItem.title = NSLocalizedString("pip.enter", comment: "'Enter PIP'")
        editorSplitViewController?.editor?.setBarItems()
        pipVC.view.isHidden = true
    }
    
    public func didFailToEnterPictureInPicture(error: Error) {
        Swift.print(error.localizedDescription)
    }
    
    public func didPause() {
        guard let path = editorSplitViewController?.editor?.document?.fileURL.path else {
            return
        }
        
        Python.shared.stop(script: path)
    }
    
    public func didResume() {
        editorSplitViewController?.editor?.run()
    }
    
    public var isPlaying: Bool {
        guard let path = editorSplitViewController?.editor?.document?.fileURL.path else {
            return false
        }
        
        return Python.shared.isScriptRunning(path)
    }
    
    // MARK: - Drop interaction delegate
    
    public func dropInteraction(_ interaction: UIDropInteraction, canHandle session: UIDropSession) -> Bool {
        #if MAIN
        session.items.first?.localObject is FileBrowserViewController.LocalFile || session.hasItemsConforming(toTypeIdentifiers: [UTType.text.identifier]) || session.hasItemsConforming(toTypeIdentifiers: [UTType.fileURL.identifier])
        #else
        false
        #endif
    }
    
    public func dropInteraction(_ interaction: UIDropInteraction, sessionDidUpdate session: UIDropSession) -> UIDropProposal {
        UIDropProposal(operation: .copy)
    }
        
    public func dropInteraction(_ interaction: UIDropInteraction, performDrop session: UIDropSession) {
        
        #if MAIN
        if let file = session.items.first?.localObject as? FileBrowserViewController.LocalFile {
            
            guard self.prompt != nil else {
                return
            }
            
            for char in "'\(file.url.path)'" {
                self.webView.insert(chars: String(char))
            }
            
            return
        }
        #endif
        
        if session.hasItemsConforming(toTypeIdentifiers: [UTType.fileURL.identifier]) {
            _ = session.loadObjects(ofClass: URL.self) { [weak self] urls in
                
                guard let self = self, let url = urls.first else {
                    return
                }
                
                guard self.prompt != nil else {
                    return
                }
                
                for char in url.path {
                    self.webView.insert(chars: String(char))
                }
            }
        } else if session.hasItemsConforming(toTypeIdentifiers: [UTType.plainText.identifier]) {
            _ = session.loadObjects(ofClass: String.self) { [weak self] strings in
                
                guard let self = self, let str = strings.first else {
                    return
                }
                
                guard self.prompt != nil else {
                    return
                }
                
                for char in str {
                    self.webView.insert(chars: String(char))
                }
            }
        }
    }
}

// MARK: - REPL Code Completion

#if MAIN
extension ConsoleViewController: InputAssistantViewDelegate, InputAssistantViewDataSource {
    
    public func inputAssistantView(_ inputAssistantView: InputAssistantView, didSelectSuggestionAtIndex index: Int) {
        
        guard let textField = movableTextField?.textField else {
            currentSuggestionIndex = -1
            return
        }
        
        guard completions.indices.contains(index), suggestions.indices.contains(index) else {
            currentSuggestionIndex = -1
            return
        }
        
        let completion = completions[index]
        let suggestion = suggestions[index]
        
        guard let range = textField.selectedTextRange else {
            currentSuggestionIndex = -1
            return
        }
        let _location = textField.offset(from: textField.beginningOfDocument, to: range.start)
        let _length = textField.offset(from: range.start, to: range.end)
        let selectedRange = NSRange(location: _location, length: _length)
                
        let location = selectedRange.location-(suggestion.count-completion.count)
        let length = suggestion.count-completion.count
        
        /*
         
         hello_w HELLO_WORLD ORLD
         
         */
        
        let iDonTKnowHowToNameThisVariableButItSSomethingWithTheSelectedRangeButFromTheBeginingLikeTheEntireSelectedWordWithUnderscoresIncluded = NSRange(location: location, length: length)
        
        textField.selectedTextRange = iDonTKnowHowToNameThisVariableButItSSomethingWithTheSelectedRangeButFromTheBeginingLikeTheEntireSelectedWordWithUnderscoresIncluded.toTextRange(textInput: textField)
        
        DispatchQueue.main.asyncAfter(deadline: .now()+0.1) { [weak self] in
            textField.insertText(suggestion)
            if completion.hasSuffix("(") {
                let range = textField.selectedTextRange
                textField.insertText(")")
                textField.selectedTextRange = range
            }
            self?.suggestions = []
            self?.completions = []
        }
                
        currentSuggestionIndex = -1
    }
    
    public func textForEmptySuggestionsInInputAssistantView() -> String? {
        return nil
    }
    
    public func numberOfSuggestionsInInputAssistantView() -> Int {
        if movableTextField?.textField.selectedTextRange?.end == movableTextField?.textField.endOfDocument {
            return completions.count
        } else {
            return 0
        }
    }
    
    public func inputAssistantView(_ inputAssistantView: InputAssistantView, nameForSuggestionAtIndex index: Int) -> String {
        let suffix: String = ((currentSuggestionIndex != -1 && index == 0) ? " ⤶" : "")
        
        guard suggestions.indices.contains(index) else {
            return ""
        }
        
        if suggestions[index].hasSuffix("(") {
            return "()"+suffix
        }
        
        return suggestions[index]+suffix
    }
    
}
#endif
