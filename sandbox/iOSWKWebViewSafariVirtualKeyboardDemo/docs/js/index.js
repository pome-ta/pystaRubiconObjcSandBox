let prevHeight = undefined;
let prevOffsetTop = undefined;
let timerId = undefined;


function handleResize() {




  const height = window.visualViewport.height * window.visualViewport.scale;
}


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
  h1Tag.style.fontSize = '2rem';
  h1Tag.textContent = 'Safari Virtual Keyboard Demo';

  element.appendChild(h1Tag);
  element.style.top = '0';
  return element;
};

const createFooter = () => {
  const element = document.createElement('footer');
  element.id = 'footer';
  element.style.bottom = '0';
  element.style.height;
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
const divTag = document.createElement('div');
divTag.id = 'editor';

const darkred = ` Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
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

const stickyButton = createButton('stickyButton', 'Sticky');
const fixedButton = createButton('fixedButton', 'Fixed');
const clearButton = createButton('clearButton', 'Clear');

const footer = createFooter();
addHeaderFooterStyle([header, footer]);


footer.appendChild(stickyButton);
footer.appendChild(fixedButton);
footer.appendChild(clearButton);

divTag.appendChild(createP(darkred));
divTag.appendChild(createP(darkgoldenrod));
divTag.appendChild(createP(darkolivegreen));
divTag.appendChild(createP(darkslateblue));
mainTag.appendChild(divTag);
rootDiv.appendChild(header);
rootDiv.appendChild(mainTag);
rootDiv.appendChild(footer);

document.addEventListener('DOMContentLoaded', () => {
  document.body.appendChild(rootDiv);
});
