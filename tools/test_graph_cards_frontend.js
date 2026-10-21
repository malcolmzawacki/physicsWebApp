// Run with node tools/test_graph_cards_frontend.js. No browser or packages needed.
// Exercise the actual component script's selection/message behavior against a tiny DOM.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
let doc;
class Element {
  constructor(tag) {
    this.tagName=tag; this.children=[]; this.attrs={}; this.handlers={}; this.className='';
    this.style={setProperty(){}};
    this.classes=new Set();
    this.classList={toggle:(name, enabled)=>enabled ? this.classes.add(name) : this.classes.delete(name)};
  }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children=[...nodes]; }
  setAttribute(key,value) { this.attrs[key]=value; }
  addEventListener(key,fn) { this.handlers[key]=fn; }
  querySelectorAll(tag) { return this.children.flatMap(c=>[...(c.tagName===tag ? [c] : []),...c.querySelectorAll(tag)]); }
  querySelector(selector) { return this.children.flatMap(c=>[c,...c.descendants()]).find(c=>c.className.split(' ').includes(selector.slice(1))); }
  descendants() { return this.children.flatMap(c=>[c,...c.descendants()]); }
  getBoundingClientRect() { return {height:400}; }
  focus() { doc.activeElement=this; }
}
const board=new Element('div'), live=new Element('p');
doc={getElementById:id=>id==='board' ? board : live, createElement:tag=>new Element(tag),
     documentElement:new Element('html'), body:new Element('body'), activeElement:null};
const messages=[];
let onMessage;
const parent={postMessage:m=>messages.push(JSON.parse(JSON.stringify(m)))};
const window={parent,addEventListener:(type,fn)=>{if(type==='message') onMessage=fn;}};
const html=fs.readFileSync(path.join(__dirname,'../utils/graph_cards_frontend/index.html'),'utf8');
vm.runInNewContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],{
  document:doc,window,ResizeObserver:class {observe(){}},Set,Math,Number,Array,String,Boolean
});
const render=args=>onMessage({source:parent,data:{type:'streamlit:render',args}});
const buttons=()=>board.querySelectorAll('button');
const click=i=>buttons()[i].handlers.click();
const submitted=()=>messages.filter(m=>m.type==='streamlit:setComponentValue');
const multi={question_id:10,images:['a','b','c','d','e','f'],labels:['A','B','C','D','E','F'],
  selection:[],locked:false,layout:'Compact grid',has_reference:false,multi_select:true,
  option_name:'Motion',check_label:'Check motions',descriptions:['rest','coast','speed','slow','start','fall']};
render(multi);
assert.equal(buttons().length,6);
assert.equal(board.attrs['aria-label'],'Motion answer choices');
click(1); assert.deepEqual(submitted().at(-1).value,{question_id:10,indices:[1]});
click(4); assert.deepEqual(submitted().at(-1).value.indices,[1,4]);
click(1); assert.deepEqual(submitted().at(-1).value.indices,[4]);
click(4); assert.deepEqual(submitted().at(-1).value.indices,[]);
assert.equal(buttons()[4].attrs['aria-pressed'],'false');
render({...multi,selection:[0,2]});
assert.equal(buttons()[0].attrs['aria-pressed'],'true');
assert.equal(buttons()[2].classes.has('selected'),true);
assert.equal(buttons()[2].classes.has('correct'),false);
render({...multi,selection:[0,2],locked:true,correct_indices:[0,2]});
assert(buttons().every(b=>b.disabled));
assert.equal(buttons()[2].classes.has('correct'),true);
const before=submitted().length; click(4); assert.equal(submitted().length,before);
render({question_id:11,images:['reference','a','b','c'],labels:['A','B','C'],selection:null,
        locked:false,layout:'Compact grid'});
assert.equal(buttons().length,3);
click(2); assert.deepEqual(submitted().at(-1).value,{question_id:11,index:2});
click(0); assert.deepEqual(submitted().at(-1).value,{question_id:11,index:0});
assert.equal(buttons()[0].attrs['aria-pressed'],'true');
assert.equal(buttons()[2].attrs['aria-pressed'],'false');
assert(live.textContent.includes('Check Match'));
render({...multi,question_id:12,images:['reference','a','b','c','d'],labels:['A','B','C','D'],
        has_reference:true,layout:'Reference beside options',reference_label:'Before the change'});
assert.equal(board.className,'beside');
assert.equal(buttons().length,4);
click(3); assert.deepEqual(submitted().at(-1).value,{question_id:12,indices:[3]});
console.log('Graph-card frontend passed: multi-select toggle/deselect, backend restoration, no premature correctness, locking, and default single-choice reference indexing.');
