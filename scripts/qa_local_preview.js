'use strict';
const fs=require('fs'),path=require('path');
const puppeteer=require('/home/slickkredd/.npm/_npx/4b4c857f6efdfb61/node_modules/puppeteer');
const url='http://127.0.0.1:4174';
const destination=process.env.HOME+'/GoreeCloud-Website-GitHub-Recovery-20261111/evidence';
fs.mkdirSync(destination,{recursive:true});
const tests=[
 ['/',1440,900,'light'],['/',390,844,'light'],['/',390,844,'dark'],['/',320,730,'light'],
 ['/design/',1440,900,'light'],['/design/',1440,900,'dark'],['/design/',390,844,'light'],['/design/',390,844,'dark'],
 ['/products/',390,844,'light'],['/ecosystem/',390,844,'light']
];
(async()=>{let browser,report={tests:[],errors:[],screenshots:[]};
try{
browser=await puppeteer.launch({headless:true,executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',args:['--disable-dev-shm-usage']});
for(const [route,width,height,theme]of tests){
 const page=await browser.newPage();
 await page.setViewport({width,height,deviceScaleFactor:1});
 await page.setCacheEnabled(false);
 const errors=[],failed=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('requestfailed',req=>failed.push(req.url()));
 page.on('request',req=>{if(!req.url().startsWith(url+'/'))external.push(req.url())});
 const response=await page.goto(url+route,{waitUntil:'networkidle0',timeout:18000});
 await page.evaluate(x=>document.documentElement.dataset.theme=x,theme);
 await page.evaluate(async()=>{ const imgs=[...document.querySelectorAll('img[src*="/assets/gc-ui/"]')].filter(x=>getComputedStyle(x).display!=='none'); await Promise.all(imgs.map(async x=>{x.loading='eager';try{await x.decode();}catch(e){}})); });
 const m=await page.evaluate(()=>{
 const assets=[...document.querySelectorAll('img[src*="/assets/gc-ui/"]')].filter(x=>getComputedStyle(x).display!=='none').map(x=>({src:x.getAttribute('src'),naturalWidth:x.naturalWidth,complete:x.complete}));
 const style=getComputedStyle(document.documentElement);
 return {scroll:document.documentElement.scrollWidth,viewport:innerWidth,assets,
    logoVisible:!!document.querySelector('.gcui-brand-heading img'),
    favicon:!!document.querySelector('link[rel=icon][href*="gc-ui"]'),
    bodyFont:getComputedStyle(document.body).fontSize,
    colorScheme:style.colorScheme};
 });
 if(response.status()!=200||errors.length||failed.length||external.length||m.scroll>m.viewport+2||
 m.assets.some(a=>!a.complete||a.naturalWidth===0))report.errors.push({route,width,theme,status:response.status(),errors,failed,external,metrics:m});
 if(route==='/design/'&&!m.favicon)report.errors.push('design missing GC UI favicon');
 if(route==='/'&&m.favicon)report.errors.push('global GoreeCloud site incorrectly using GC UI favicon');
 if((route==='/design/'&&width===1440)||(route==='/design/'&&width===390)||(route==='/'&&width===1440)){
    const name=(route==='/design/'?'design':'home')+'-'+width+'-'+theme+'.png';
    await page.screenshot({path:path.join(destination,name),fullPage:false});
    report.screenshots.push(name);
 }
 report.tests.push({route,width,theme,status:response.status(),metrics:m});
 await page.close();
}
}catch(e){report.errors.push('runner:'+e.message.slice(0,450))}
finally{
 if(browser)await browser.close();
 fs.writeFileSync(path.join(destination,'local-browser-qa.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({checked:report.tests.length,passed:report.errors.length===0,errors:report.errors,screenshots:report.screenshots}));
 if(report.errors.length)process.exitCode=1;
}
})();