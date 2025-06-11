const ua = window.navigator.userAgent;
const iOS = !!ua.match(/iPad/i) || !!ua.match(/iPhone/i);

const replaceSyncs = [
  `body.virtual-keyboard-shown {
    margin-top: var(--visual-viewport-offset-top, 0px);
  }`,
  `.virtual-keyboard-shown #root,
    #root:has(input:focus),
    #root:has([contenteditable="true"]:focus) {
    overscroll-behavior-y: contain;
  }`,
  `#editor:has(:focus),
    .virtual-keyboard-shown #editor {
    min-height: calc(100 * var(--svh, 1svh) - 96px + 1px);
  }`,
];

let prevHeight = undefined;
let prevOffsetTop = undefined;
let timerId = undefined;

function handleResize(e) {
  const height = window.visualViewport.height * window.visualViewport.scale;
  if (prevHeight !== height) {
    prevHeight = height;
    requestAnimationFrame(() => {
      document.documentElement.style.setProperty('--svh', height * 0.01 + 'px');
    });
  }
  if (prevOffsetTop !== window.visualViewport.offsetTop) {
    if (prevOffsetTop === undefined) {
      prevOffsetTop = window.visualViewport.offsetTop;
    } else {
      const scrollOffset = window.visualViewport.offsetTop - prevOffsetTop;
      prevOffsetTop = window.visualViewport.offsetTop;
      requestAnimationFrame(() => {
        if (e && e.type === 'resize') {
          rootDiv.scrollBy(0, scrollOffset);
        }
        document.documentElement.style.setProperty(
          '--visual-viewport-offset-top',
          window.visualViewport.offsetTop + 'px'
        );
      });
    }
  }
  if (height + 10 < document.documentElement.clientHeight) {
    document.body.classList.add('virtual-keyboard-shown');
  } else {
    document.body.classList.remove('virtual-keyboard-shown');
  }
}

const createRootDiv = () => {
  const element = document.createElement('div');
  element.id = 'root';
  element.classList.add('scrollable');
  element.style.width = '100vw';
  // element.style.width = '100%';
  element.style.height = `calc(100 * var(--svh, 1svh))`;
  element.style.overflowY = 'scroll';
  element.style.overflowX = 'hidden';

  return element;
};

const createHeader = () => {
  const element = document.createElement('header');
  element.id = 'header';
  const h1Tag = document.createElement('h1');
  h1Tag.style.fontSize = '1.5rem';
  h1Tag.textContent = 'Safari Virtual Keyboard Demo';

  element.appendChild(h1Tag);
  // element.style.position = 'sticky';
  element.style.top = '0';
  return element;
};

const createEditorDiv = () => {
  const element = document.createElement('div');
  element.id = 'editor';
  element.contentEditable = 'true';
  element.style.minHeight = `calc(100 * var(--svh, 1svh) - 96px)`;
  element.style.fontSize = '1.5rem';
  return element;
};

const createFooter = () => {
  const element = document.createElement('footer');
  element.id = 'footer';
  // element.style.position = 'sticky';
  element.style.bottom = '0';
  return element;
};

const addHeaderFooterStyle = (headerFooter) => {
  [...headerFooter].forEach((element) => {
    element.style.position = 'sticky';
    element.style.display = 'flex';
    element.style.alignItems = 'center';
    element.style.justifyContent = 'stretch';
    element.style.width = '100%';
    element.style.height = '3rem';
  });
};

const createP = (textContent) => {
  const element = document.createElement('p');
  element.contentEditable = 'true';
  element.textContent = textContent;
  // element.style.fontSize = '1.1rem';
  return element;
};

const createButton = (id, textContent) => {
  const element = document.createElement('button');
  element.id = id;
  element.style.type = 'button';
  element.textContent = textContent;

  element.style.fontSize = '1rem';
  element.style.padding = '0.5rem';
  element.style.appearance = 'none';
  element.style.height = '100%';
  element.style.flex = '1';
  return element;
};

const rootDiv = createRootDiv();
const header = createHeader();
const mainTag = document.createElement('main');
const editorDiv = createEditorDiv();

const darkred = ` Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
 ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
 aliquip ex ea commodo consequat. Duis aute irure dolor in
 reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
 pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
 culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
 ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
 aliquip ex ea commodo consequat. Duis aute irure dolor in
 reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
 pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
 culpa qui officia deserunt mollit anim id est laborum.
  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
 ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
 aliquip ex ea commodo consequat. Duis aute irure dolor in
 reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
 pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
 culpa qui officia deserunt mollit anim id est laborum.`;

const darkgoldenrod = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nullaeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nullaeiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla`;

const darkolivegreen = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.`;

const darkslateblue = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.`;

const stickyButton = createButton('stickyButton', 'Sticky');
const fixedButton = createButton('fixedButton', 'Fixed');
const clearButton = createButton('clearButton', 'Clear');

const footer = createFooter();
addHeaderFooterStyle([header, footer]);

footer.appendChild(stickyButton);
footer.appendChild(fixedButton);
footer.appendChild(clearButton);

editorDiv.appendChild(createP(darkred));
editorDiv.appendChild(createP(darkgoldenrod));
editorDiv.appendChild(createP(darkolivegreen));
editorDiv.appendChild(createP(darkslateblue));
mainTag.appendChild(editorDiv);

rootDiv.appendChild(header);
rootDiv.appendChild(mainTag);
rootDiv.appendChild(footer);

document.addEventListener('DOMContentLoaded', () => {
  document.body.padding = 0;
  document.body.appendChild(rootDiv);

  const extraSheet = new CSSStyleSheet();
  extraSheet.replaceSync(replaceSyncs.join('\n'));
  document.adoptedStyleSheets = [extraSheet];

  if (!iOS) {
    return;
  }
  handleResize();
  self.visualViewport.addEventListener('resize', handleResize);
  self.visualViewport.addEventListener('scroll', handleResize);
});
