const createRootDiv = () => {
  const element = document.createElement('div');
  element.id = 'root';
  element.classList.add('scrollable');

  return element;
};

const createHeader = () => {
  const element = document.createElement('header');
  element.id = 'header';
  const h1Tag = document.createElement('h1');
  h1Tag.textContent = 'Safari Virtual Keyboard Demo';

  element.appendChild(h1Tag);
  return element;
};

const createP = (textContent) => {
  const element = document.createElement('p');
  element.textContent = textContent;
  return element;
};

const createFooter = () => {
  const element = document.createElement('footer');
  element.id = 'footer';
  return element;
};

const rootDiv = createRootDiv();
const header = createHeader();
const mainTag = document.createElement('main');
const divTag = document.createElement('div');
divTag.id = 'editor';

const darkred = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
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
culpa qui officia deserunt mollit anim id est laborum.`;

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

const footer = createFooter();

divTag.appendChild(createP(darkred));
divTag.appendChild(createP(darkgoldenrod));
divTag.appendChild(createP(darkolivegreen));
divTag.appendChild(createP(darkslateblue));
mainTag.appendChild(divTag);
rootDiv.appendChild(header);
rootDiv.appendChild(mainTag);
rootDiv.appendChild(footer);

document.addEventListener('DOMContentLoaded', (e) => {
  // console.log('hoge');
  document.body.appendChild(rootDiv);
});

(() => {
  const ua = window.navigator.userAgent;
  const iOS = !!ua.match(/iPad/i) || !!ua.match(/iPhone/i);
  if (!iOS) return;
  if (!self.visualViewport) return;
  let prevHeight = undefined;
  let prevOffsetTop = undefined;
  let timerId = undefined;
  const scrollElem = document.getElementById('root');
  function handleResize(e) {
    const height = self.visualViewport.height * self.visualViewport.scale;
    if (prevHeight !== height) {
      prevHeight = height;
      requestAnimationFrame(() => {
        document.documentElement.style.setProperty(
          '--svh',
          height * 0.01 + 'px'
        );
      });
    }
    if (prevOffsetTop !== self.visualViewport.offsetTop) {
      if (prevOffsetTop === undefined) {
        prevOffsetTop = self.visualViewport.offsetTop;
      } else {
        const scrollOffset = self.visualViewport.offsetTop - prevOffsetTop;
        prevOffsetTop = self.visualViewport.offsetTop;
        requestAnimationFrame(() => {
          if (e && e.type === 'resize') {
            scrollElem.scrollBy(0, scrollOffset);
          }
          document.documentElement.style.setProperty(
            '--visual-viewport-offset-top',
            self.visualViewport.offsetTop + 'px'
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
  handleResize();
  self.visualViewport.addEventListener('resize', handleResize);
  self.visualViewport.addEventListener('scroll', handleResize);
})();
