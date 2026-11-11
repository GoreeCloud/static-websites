import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const script = readFileSync(new URL('../site/assets/catalog-tools.js', import.meta.url), 'utf8');

function createElement(extra = {}) {
  const listeners = {};
  const attributes = new Map();
  return {
    dataset: {}, hidden: false, textContent: '', value: '',
    ...extra,
    addEventListener(type, listener) {
      (listeners[type] ||= []).push(listener);
    },
    dispatchEvent(event) {
      for (const callback of listeners[event.type] || []) callback(event);
      return true;
    },
    getAttribute(name) { return attributes.get(name) || null; },
    setAttribute(name, value) { attributes.set(name, String(value)); },
    async click() {
      return Promise.all((listeners.click || []).map(callback => callback()));
    }
  };
}

function buildFixture(kind, search = '', clipboardReady = true) {
  const path = ({ products:'/products/', github:'/github/', suite:'/suite/' })[kind];
  const origin = 'https://review.example';
  const window = {
    location: new URL(origin + path + search),
    events: {},
    addEventListener(type, callback) { this.events[type] = callback; }
  };
  const history = {
    state: {},
    replaceState(_state, _title, href) {
      window.location = new URL(href, window.location.origin);
    }
  };
  const input = createElement();
  const group = createElement({value:'all',options:['all','g0','g1','g2'].map(value=>({value}))});
  const categoryNames=['all','apps','design','platform','infrastructure'];
  const filters=categoryNames.map(category=>{
    const element=createElement({dataset:{filter:category}});
    element.setAttribute('aria-pressed',category==='all'?'true':'false');
    element.addEventListener('click',()=>{
      for(const item of filters) item.setAttribute('aria-pressed',String(item===element));
    });
    return element;
  });
  const share=createElement();
  const reset=createElement();
  const status=createElement();
  const link=createElement({hidden:true});
  const panel=createElement({dataset:{catalogActions:kind}});
  panel.querySelector=selector=>({
    '[data-catalog-share]':share, '[data-catalog-reset]':reset,
    '[data-catalog-status]':status, '[data-catalog-link]':link
  })[selector]||null;
  const selectors={
    '[data-catalog-actions]':panel, '[data-search]':kind==='products'?input:null,
    '[data-repo-search]':kind==='github'?input:null,
    '[data-suite-search]':kind==='suite'?input:null,
    '[data-suite-filter]':kind==='suite'?group:null
  };
  const document={
    querySelector:selector=>selectors[selector]||null,
    querySelectorAll:selector=>selector==='[data-filter]'&&kind==='products'?filters:[]
  };
  const copied=[];
  const navigator=clipboardReady
    ? {clipboard:{writeText:async text=>{copied.push(text)}}}
    : {};
  class Event {
    constructor(type, options = {}) { this.type=type; this.bubbles=!!options.bubbles; }
  }
  vm.runInNewContext(script,{document,window,history,navigator,URL,URLSearchParams,Event,Error},
    {filename:'catalog-tools.js',timeout:500});
  return {input,group,filters,share,reset,status,link,window,copied,
    category:()=>filters.find(x=>x.getAttribute('aria-pressed')==='true')?.dataset.filter};
}

test('Products restores bounded search/category and shares same-origin only on request',async()=>{
  const x=buildFixture('products','?q=Mesh&category=design');
  assert.equal(x.input.value,'Mesh');
  assert.equal(x.category(),'design');
  assert.equal(x.input.maxLength,120);
  assert.deepEqual(x.copied,[],'ordinary filtering must not invoke clipboard');
  await x.share.click();
  assert.equal(x.copied.length,1);
  assert.equal(x.copied[0],'https://review.example/products/?q=Mesh&category=design');
  assert.equal(x.link.hidden,false);
  assert.match(x.status.textContent,/Link copied/);
  await x.reset.click();
  assert.equal(x.input.value,'');
  assert.equal(x.category(),'all');
  assert.equal(x.window.location.search,'');
  assert.equal(x.link.hidden,true);
});

test('Invalid category safely falls back to All; enormous search terms are bounded',async()=>{
  const x=buildFixture('products','?category=unknown&q='+encodeURIComponent('<img src=x>'+('a'.repeat(150))));
  assert.equal(x.category(),'all');
  assert.equal(x.input.value.length,120);
  assert.ok(x.input.value.startsWith('<img src=x>'));
  await x.share.click();
  assert.equal(new URL(x.copied[0]).searchParams.get('q').length,120);
  assert.equal(new URL(x.copied[0]).searchParams.has('category'),false);
});

test('GitHub clipboard denial retains a selectable link; Escape resets',async()=>{
  const x=buildFixture('github','?q=calendar',false);
  assert.equal(x.input.value,'calendar');
  await x.share.click();
  assert.equal(x.copied.length,0);
  assert.equal(x.link.hidden,false);
  assert.equal(x.link.textContent,'https://review.example/github/?q=calendar');
  assert.match(x.status.textContent,/Copy it/);
  let prevented=false;
  x.input.dispatchEvent({type:'keydown',key:'Escape',preventDefault(){prevented=true}});
  assert.equal(prevented,true);
  assert.equal(x.input.value,'');
  assert.equal(x.window.location.search,'');
  assert.equal(x.link.hidden,true);
});

test('Suite restores allowed group, share link, and resets independently',async()=>{
  const x=buildFixture('suite','?group=g2&q=Notes');
  assert.equal(x.input.value,'Notes');
  assert.equal(x.group.value,'g2');
  await x.share.click();
  assert.equal(x.copied[0],'https://review.example/suite/?q=Notes&group=g2');
  await x.reset.click();
  assert.equal(x.group.value,'all');
  assert.equal(x.input.value,'');
  assert.equal(x.window.location.search,'');
});

test('Popstate restoration uses URL source and discards invalid groups',()=>{
  const x=buildFixture('suite','?q=Music&group=g1');
  x.window.location = new URL('https://review.example/suite/?q=Calendar&group=malicious');
  x.window.events.popstate();
  assert.equal(x.input.value,'Calendar');
  assert.equal(x.group.value,'all');
  assert.equal(x.link.hidden,true);
});
