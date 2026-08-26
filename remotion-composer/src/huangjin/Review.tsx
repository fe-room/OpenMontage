import React from 'react';
import {AbsoluteFill, Composition, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio, Video} from '@remotion/media';

const C={bg:'#11100E',paper:'#F1EBDD',gold:'#C9A45C',teal:'#5E9C93',red:'#B45A45',graph:'#292723',gray:'#9C978D'};
const font="PingFang SC, Noto Sans CJK SC, Arial, sans-serif";

export const scenes=[
 ['反弹之后，问题才开始','黄金又反弹了'],['四种选择，同一个名字','金条｜积存金｜黄金ETF｜黄金股'],['黄金涨 10%','它们都会涨 10% 吗？'],['先看你买到什么权利','实物｜账户｜基金｜股权'],['入口相似，底层权利不同','四种资产形态'],['积存金不是普通存款','本金固定？｜随金价变化'],['便利背后还有规则','手续费｜兑换｜门槛'],['前三种更接近黄金本身','黄金股是公司股权'],['黄金股背后是一家公司','公司经营'],['利润由多种变量共同决定','产量｜能源｜人工｜品位｜债务｜估值'],['实验一：成本不变','售价 100→110｜利润 20→30'],['金价 +10%','单位利润 +50%'],['实验二：成本上升','成本 80→100｜利润只剩 10'],['方向甚至可能相反','金价只是利润的一项变量'],['这次只看国内三组数据','Au99.99｜518880｜517520'],['再把起点统一为 100','100 个共同交易日'],['国内阶段 A','2025-05-14—2025-10-09'],['同一阶段，黄金股明显放大','Au99.99 +20.19%｜518880 +19.95%｜517520 +61.10%'],['国内阶段 B','2024-07-11—2024-12-06'],['金价上涨，黄金股仍可能亏','Au99.99 +9.31%｜518880 +8.97%｜517520 -13.51%'],['再看一次下跌有多深','最大回撤'],['黄金股这一路更颠簸','Au99.99 -7.17%｜518880 -7.49%｜517520 -23.59%'],['报价不动，也可能先亏费用','买入费 + 赎回费'],['刚买再卖，约先少 1%','机制示意｜规则以银行最新为准'],['实物回购先看类别与验金','称重｜成色｜检测'],['同是黄金，参考回购会分档','不同类别存在差异'],['四种工具，四类偏离源','溢价｜规则｜跟踪｜经营'],['结论','不会自动同涨 10%'],['以后先问这四个问题','权利｜收益｜成本｜偏离'],['研究边界','历史展示 ≠ 未来预测'],['本视频仅作知识分享，不构成任何投资建议。','市场有风险，投资需谨慎。'],
] as const;

const base:React.CSSProperties={fontFamily:font,color:C.paper};
const line=(pts:string,color=C.gold,w=10)=><polyline points={pts} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round"/>;
const Axis=()=> <svg viewBox="0 0 900 600" style={{width:'100%'}}><path d="M90 40V520H830" stroke={C.gray} strokeWidth="4" opacity=".55"/>{[0,1,2,3].map(i=><path key={i} d={`M90 ${120+i*110}H830`} stroke={C.gray} strokeWidth="2" opacity=".16"/>)}</svg>;
const Pill=({children,color=C.gold}:{children:React.ReactNode;color?:string})=><div style={{border:`2px solid ${color}`,borderRadius:999,padding:'15px 25px',fontSize:28,color,whiteSpace:'nowrap'}}>{children}</div>;
const Stamp=({children}:{children:React.ReactNode})=><div style={{border:`4px double ${C.gold}`,color:C.gold,padding:'18px 24px',fontWeight:800,fontSize:34,transform:'rotate(-2deg)',background:'#11100Ecc'}}>{children}</div>;
const Paper=({children}:{children:React.ReactNode})=><div style={{background:C.paper,color:C.bg,borderRadius:6,padding:48,boxShadow:'0 22px 70px #0008',width:'84%',minHeight:720,position:'relative',overflow:'hidden'}}>{children}<div style={{position:'absolute',inset:0,opacity:.06,backgroundImage:'repeating-linear-gradient(0deg,#000 0,#000 1px,transparent 1px,transparent 7px)',pointerEvents:'none'}}/></div>;
const Bars=({vals,labels,colors}:{vals:number[];labels:string[];colors?:string[]})=><div style={{display:'flex',alignItems:'flex-end',gap:35,height:610,width:'82%',borderBottom:`3px solid ${C.gray}`}}>{vals.map((v,i)=><div key={labels[i]} style={{flex:1,textAlign:'center'}}><div style={{height:v,background:colors?.[i]||C.gold,borderRadius:'8px 8px 0 0',display:'flex',alignItems:'flex-start',justifyContent:'center',paddingTop:20,color:C.bg,fontWeight:900,fontSize:28}}>{labels[i].split('|')[1]}</div><div style={{marginTop:18,fontSize:27}}>{labels[i].split('|')[0]}</div></div>)}</div>;

export const Visual=({id}:{id:number})=>{
 const four=['金条','积存金','黄金 ETF','黄金股'];
 if(id===1)return <div style={{position:'relative',width:'88%'}}><Axis/><svg viewBox="0 0 900 600" style={{position:'absolute',inset:0,width:'100%'}}>{line('90,470 190,450 290,480 390,370 500,390 610,250 720,210 820,120')}</svg><Stamp>黄金又反弹了</Stamp></div>;
 if(id===2)return <div style={{display:'grid',gap:24,width:'82%'}}>{four.map((x,i)=><div key={x} style={{background:i===3?C.graph:C.paper,color:i===3?C.paper:C.bg,padding:'27px 36px',fontSize:40,borderLeft:`12px solid ${i===3?C.teal:C.gold}`}}>{String(i+1).padStart(2,'0')}　{x}</div>)}</div>;
 if(id===3)return <div style={{textAlign:'center'}}><div style={{fontSize:170,fontWeight:900,color:C.gold}}>+10%</div><div style={{fontSize:62,fontWeight:800}}>都会一样吗？</div><div style={{display:'flex',gap:15,marginTop:70}}>{four.map(x=><Pill key={x}>{x}</Pill>)}</div></div>;
 if(id===4)return <Paper><div style={{borderLeft:`5px solid ${C.gold}`,paddingLeft:38,display:'grid',gap:35}}>{[['金条','实物所有权'],['积存金','银行账户份额'],['黄金ETF','基金份额'],['黄金股','公司股权']].map(x=><div><small style={{color:C.gray,fontSize:25}}>{x[0]}</small><div style={{fontSize:44,fontWeight:800}}>{x[1]}</div></div>)}</div></Paper>;
 if(id===5)return <div style={{width:'88%',display:'grid',gridTemplateColumns:'1fr 1fr',gap:30}}>{four.map((x,i)=><div style={{height:280,border:`3px solid ${i===3?C.teal:C.gold}`,display:'grid',placeItems:'center',fontSize:40,background:C.graph}}>{x}<div style={{fontSize:24,color:C.gray}}>{['金属','账户','基金','股权'][i]}</div></div>)}</div>;
 if(id===6)return <div style={{display:'flex',gap:30,width:'88%'}}>{[['普通存款',false],['积存金',true]].map(([x,w]:any)=><div style={{flex:1,background:C.paper,color:C.bg,padding:35}}><h2>{x}</h2><svg viewBox="0 0 350 420">{line(w?'20,250 90,180 160,280 230,120 330,205':'20,220 330,220',w?C.gold:C.gray,8)}</svg><b>{w?'随金价变化':'本金路径较稳定'}</b></div>)}</div>;
 if(id===7)return <Paper><div style={{fontSize:42,fontWeight:900}}>积存金账户</div><div style={{height:40,background:C.gold,width:'72%',margin:'60px 0'}}/><div style={{display:'flex',gap:18}}>{['手续费','兑换','门槛'].map(x=><Pill>{x}</Pill>)}</div><p style={{marginTop:90,color:C.gray}}>以银行最新规则为准</p></Paper>;
 if(id===8)return <div style={{width:'88%',textAlign:'center'}}><div style={{display:'flex',justifyContent:'center',gap:18}}>{four.slice(0,3).map(x=><Pill>{x}</Pill>)}</div><div style={{height:180,borderLeft:`5px solid ${C.gold}`,marginLeft:'50%'}}/><div style={{display:'flex',justifyContent:'space-around'}}><Stamp>黄金本身</Stamp><div style={{borderTop:`5px solid ${C.teal}`,paddingTop:20,fontSize:36}}>黄金股 → 公司经营</div></div></div>;
 if(id===9||id===25)return <div style={{width:'100%',height:'100%',position:'relative'}}><Img src={staticFile(id===9?'review/sc09.jpg':'review/sc25.jpg')} style={{width:'100%',height:'100%',objectFit:'cover',filter:'brightness(.72) saturate(.75)'}}/><div style={{position:'absolute',inset:0,background:'linear-gradient(transparent 42%,#11100Edd 78%)'}}/><div style={{position:'absolute',left:70,bottom:120}}><Stamp>{id===9?'公司经营':'实物回购要看类别与验金'}</Stamp></div></div>;
 if(id===10)return <div style={{position:'relative',width:800,height:800,display:'grid',placeItems:'center'}}><div style={{width:220,height:220,borderRadius:'50%',border:`8px solid ${C.gold}`,display:'grid',placeItems:'center',fontSize:42,fontWeight:800}}>利润</div>{['产量','能源','人工','品位','债务','估值'].map((x,i)=><div style={{position:'absolute',left:330+300*Math.cos(i*Math.PI/3),top:330+300*Math.sin(i*Math.PI/3)}}><Pill color={i%2?C.teal:C.gold}>{x}</Pill></div>)}</div>;
 if(id===11)return <Bars vals={[530,410,120]} labels={['售价|110','成本|80','利润|30']} colors={[C.paper,C.red,C.gold]}/>;
 if(id===12)return <div style={{display:'flex',gap:55,alignItems:'center'}}><div style={{fontSize:86,fontWeight:900}}>金价<br/><b style={{color:C.gold}}>+10%</b></div><div style={{fontSize:90,color:C.gray}}>→</div><div style={{fontSize:86,fontWeight:900}}>利润<br/><b style={{color:C.gold}}>+50%</b></div></div>;
 if(id===13)return <Bars vals={[530,485,45]} labels={['售价|110','成本|100','利润|10']} colors={[C.paper,C.red,C.gold]}/>;
 if(id===14)return <div style={{display:'grid',gridTemplateColumns:'1fr auto 1fr',alignItems:'center',gap:30}}><Stamp>金价 ↑</Stamp><div style={{fontSize:90,color:C.red}}>＋成本 ↑</div><Stamp>利润 ↓</Stamp></div>;
 if(id===15)return <div style={{width:'84%',display:'grid',gap:40}}>{['Au99.99','518880 黄金ETF','517520 黄金股ETF'].map((x,i)=><div key={x} style={{display:'flex',alignItems:'center',gap:25}}><Pill color={[C.gold,C.paper,C.teal][i]}>{x}</Pill><div style={{height:5,background:[C.gold,C.paper,C.teal][i],flex:1}}/><Stamp>共同交易日</Stamp></div>)}</div>;
 if(id===16)return <div style={{width:'84%'}}><div style={{fontSize:150,fontWeight:900,color:C.gold,textAlign:'center'}}>100</div><div style={{display:'flex',justifyContent:'space-between',borderTop:`4px solid ${C.gray}`,paddingTop:35}}>{['Au99.99','518880','517520'].map((x,i)=><Pill key={x} color={[C.gold,C.paper,C.teal][i]}>{x}</Pill>)}</div></div>;
 if(id===17||id===19)return <div style={{position:'relative',width:'88%'}}><Axis/><svg viewBox="0 0 900 600" style={{position:'absolute',inset:0,width:'100%'}}>{line(id===17?'90,452 194,436 299,444 403,437 507,438 611,442 716,399 820,333':'90,234 194,231 299,213 403,218 507,182 611,104 716,163 820,134',C.gold,7)}{line(id===17?'90,452 194,436 299,444 403,439 507,438 611,444 716,400 820,334':'90,234 194,230 299,215 403,222 507,190 611,105 716,166 820,137',C.paper,7)}{line(id===17?'90,452 194,408 299,413 403,391 507,391 611,373 716,222 820,90':'90,234 194,313 299,351 403,470 507,355 611,301 716,392 820,379',C.teal,9)}</svg></div>;
 if(id===18)return <Bars vals={[200,198,590]} labels={['Au99.99|+20.19%','518880|+19.95%','517520|+61.10%']} colors={[C.gold,C.paper,C.teal]}/>;
 if(id===20)return <Bars vals={[300,292,120]} labels={['Au99.99|+9.31%','518880|+8.97%','517520|-13.51%']} colors={[C.gold,C.paper,C.red]}/>;
 if(id===21)return <div style={{width:'80%',height:760,position:'relative'}}><div style={{position:'absolute',left:80,top:80,right:120,borderTop:`8px solid ${C.gold}`}}/><div style={{position:'absolute',right:120,top:80,height:500,borderRight:`8px solid ${C.red}`}}/><div style={{position:'absolute',right:70,top:280,fontSize:42,color:C.red}}>最大回撤</div><svg viewBox="0 0 800 700">{line('80,80 190,160 310,110 440,270 560,240 680,580',C.paper,10)}</svg></div>;
 if(id===22)return <Bars vals={[210,220,600]} labels={['Au99.99|-7.17%','518880|-7.49%','517520|-23.59%']} colors={[C.gold,C.paper,C.red]}/>;
 if(id===23)return <div style={{display:'flex',alignItems:'center',gap:24,width:'88%'}}><div style={{height:105,width:250,background:C.gold,color:C.bg,display:'grid',placeItems:'center',fontSize:35,fontWeight:900}}>100 份价值</div>{['买入费','赎回费'].map(x=><><div style={{fontSize:65}}>→</div><div style={{width:120,height:260,border:`8px solid ${C.red}`,display:'grid',placeItems:'center',fontSize:27,writingMode:'vertical-rl'}}>{x}</div></>)}</div>;
 if(id===24)return <div style={{textAlign:'center'}}><div style={{fontSize:36,color:C.gray}}>报价保持不变</div><div style={{fontSize:180,fontWeight:900,color:C.red,margin:'60px 0'}}>约 -1%</div><Stamp>双边费用机制示意</Stamp></div>;
 if(id===26)return <Paper><div style={{fontSize:35,color:C.gray}}>工行参考回购分类</div><div style={{marginTop:70,display:'grid',gap:38}}>{['品牌金','其他 Au99 及以上黄金'].map((x,i)=><div><b style={{fontSize:38}}>{x}</b><div style={{height:24,width:i?'69%':'76%',background:i?C.teal:C.gold,marginTop:16}}/></div>)}</div><p style={{marginTop:90}}>不同类别的参考回购存在差异</p></Paper>;
 if(id===27)return <div style={{width:'88%',display:'grid',gap:24}}>{[['金条','溢价 / 回购'],['积存金','费用 / 规则'],['黄金ETF','费用 / 跟踪'],['黄金股','经营 / 估值']].map((x,i)=><div style={{display:'grid',gridTemplateColumns:'1fr 1.5fr',alignItems:'center',borderBottom:`2px solid ${C.graph}`,padding:20}}><b style={{fontSize:34}}>{x[0]}</b><div style={{height:55,background:[C.gold,C.paper,C.teal,C.red][i],color:C.bg,padding:'10px 20px',fontSize:28}}>{x[1]}</div></div>)}</div>;
 if(id===28)return <div style={{textAlign:'center'}}><div style={{fontSize:56}}>不会自动</div><div style={{fontSize:140,fontWeight:900,color:C.gold}}>同涨 10%</div><div style={{height:8,background:C.red,transform:'rotate(-3deg)',marginTop:-70}}/></div>;
 if(id===29)return <Paper><div style={{fontSize:32,color:C.gray,marginBottom:40}}>黄金产品检验单</div>{['买到什么权利？','收益来自哪里？','完整成本是什么？','何时偏离金价？'].map((x,i)=><div style={{fontSize:41,fontWeight:800,padding:'27px 0',borderBottom:`2px solid ${C.gray}`}}><span style={{color:C.gold,marginRight:25}}>0{i+1}</span>{x}</div>)}</Paper>;
 if(id===30)return <div style={{width:'88%',display:'grid',gridTemplateColumns:'1fr 1fr',gap:30}}><Paper><div style={{fontSize:34}}>历史证据</div><svg viewBox="0 0 500 500">{line('20,400 110,300 210,340 310,180 460,120',C.gold,10)}</svg><Stamp>已发生</Stamp></Paper><div style={{border:`3px dashed ${C.gray}`,display:'grid',placeItems:'center',fontSize:80,color:C.gray}}>未来<br/>…</div></div>;
 return <div style={{width:'86%',padding:'80px 55px',borderTop:`5px solid ${C.gold}`,borderBottom:`5px solid ${C.gold}`,textAlign:'center'}}><div style={{fontSize:55,fontWeight:800,lineHeight:1.55}}>本视频仅作知识分享，<br/>不构成任何投资建议。</div><div style={{fontSize:42,color:C.gold,marginTop:55}}>市场有风险，投资需谨慎。</div></div>;
};

export const ReviewFilmstrip=()=>{
 const frame=useCurrentFrame(); const idx=Math.max(0,Math.min(30,frame)); const [title,sub]=scenes[idx];
 return <AbsoluteFill style={{...base,background:C.bg,overflow:'hidden'}}>
  <div style={{position:'absolute',inset:0,opacity:.035,backgroundImage:'repeating-linear-gradient(0deg,#fff 0,#fff 1px,transparent 1px,transparent 8px)'}}/>
  {idx+1!==9&&idx+1!==25&&<><div style={{position:'absolute',left:70,top:75,fontSize:24,letterSpacing:5,color:C.gray}}>GOLD / ASSAY NOTE　{String(idx+1).padStart(2,'0')}</div><div style={{position:'absolute',left:70,right:70,top:135,borderTop:`2px solid ${C.graph}`}}/></>}
  <div style={{position:'absolute',inset:'175px 0 380px',display:'grid',placeItems:'center'}}><Visual id={idx+1}/></div>
  {idx+1!==31&&<div style={{position:'absolute',left:70,right:70,bottom:90}}><div style={{fontSize:53,fontWeight:850,lineHeight:1.12,maxWidth:900}}>{title}</div><div style={{fontSize:27,color:C.gold,marginTop:23,letterSpacing:1}}>{sub}</div></div>}
 </AbsoluteFill>;
};

const timeline=[
 [0,6.971],[6.971,13.07],[13.07,17.427],[17.427,25.513],[25.513,32.128],
 [32.128,38.556],[38.556,44.341],[44.341,50.245],[50.245,53.935],[53.935,58.363],
 [58.363,66],[66,71.554],[71.554,78.764],[78.764,84.007],[84.007,92.009],
 [92.009,101.154],[101.154,110.117],[110.117,116.092],[116.092,125.645],[125.645,132.013],
 [132.013,139.212],[139.212,146.411],[146.411,154.699],[154.699,160.727],[160.727,165.284],
 [165.284,172.12],[172.12,180.709],[180.709,187.458],[187.458,198.337],[198.337,206.496],
 [206.496,216.496],
] as const;

const captions=[
  {start:0.435,end:4.135,text:"最近黄金又走出一波反弹，身边不少人也开始重新看黄金。"},
  {start:4.655,end:9.465,text:"可真要买，选项一下就多了：金条、积存金、黄金ETF、黄金股。"},
  {start:10.169,end:13.149,text:"名字里都有黄金，可如果金价涨百分之十……"},
  {start:13.263,end:14.783,text:"它们会不会也差不多涨百分之十？"},
  {start:15.292,end:16.982,text:"我顺着这个问题查了下去。"},
  {start:17.427,end:18.907,text:"先看买到的到底是什么。"},
  {start:19.476,end:20.446,text:"金条是真黄金；"},
  {start:20.817,end:22.937,text:"积存金是银行账户里的黄金克数或份额；"},
  {start:23.419,end:26.389,text:"实物黄金ETF是基金份额，通常跟踪金价；"},
  {start:26.882,end:28.772,text:"黄金股则是一家矿业公司的股权。"},
  {start:29.231,end:31.461,text:"入口不同只是表面，底层权利已经不同。"},
  {start:32.128,end:33.638,text:"积存金最容易被名字误导。"},
  {start:34.374,end:38.204,text:"这里的“存”是积累黄金，不是本金固定、按期拿利息。"},
  {start:38.655,end:40.475,text:"金价跌，账户价值也会跌。"},
  {start:40.979,end:44.189,text:"至于手续费、兑换和门槛，要看银行当时的规则。"},
  {start:44.341,end:48.831,text:"这样一分就清楚了：前三种更靠近黄金本身，只是持有方式不同；"},
  {start:49.279,end:50.539,text:"黄金股买的是公司。"},
  {start:51.201,end:57.941,text:"它除了金价，还受产量、能源、人工、矿石品位、债务和市场估值影响。"},
  {start:58.363,end:62.403,text:"举个简单例子：黄金售价一百元，成本八十元，利润二十元。"},
  {start:63.205,end:67.195,text:"金价涨百分之十到一百一十元，成本不变，利润就变成三十元。"},
  {start:67.694,end:69.384,text:"金价只涨百分之十……"},
  {start:69.479,end:70.839,text:"利润却多了百分之五十。"},
  {start:71.554,end:73.634,text:"但……成本不会永远不动。"},
  {start:74.067,end:79.807,text:"如果售价还是一百一十元，成本却从八十元涨到一百元，利润反而只剩十元。"},
  {start:80.434,end:83.414,text:"于是金价涨了百分之十，公司单位利润却少了一半。"},
  {start:84.007,end:86.437,text:"这个例子讲得通，市场却不一定照着演。"},
  {start:87.239,end:95.929,text:"这次只看国内：上金所 Au 九九点九九、华安黄金 ETF 五一八八八零，和永赢黄金股 ETF 五一七五二零。"},
  {start:96.699,end:100.899,text:"只比较三者都有报价的交易日，统一从一百出发。"},
  {start:101.154,end:104.074,text:"第一段是二零二五年五月十四日到十月九日。"},
  {start:104.309,end:109.469,text:"Au 九九点九九涨百分之二十点一九，五一八八八零涨百分之十九点九五，两者几乎贴着走；"},
  {start:109.95,end:112.25,text:"五一七五二零却涨百分之六十一点一零。"},
  {start:112.943,end:115.393,text:"这次，利润放大的效果确实很明显。"},
  {start:116.092,end:119.112,text:"可换到二零二四年七月十一日到十二月六日，"},
  {start:119.475,end:123.115,text:"结果马上反过来：Au 九九点九九涨百分之九点三一，"},
  {start:123.722,end:125.852,text:"五一八八八零涨百分之八点九七，"},
  {start:126.474,end:128.554,text:"五一七五二零却跌百分之十三点五一。"},
  {start:129.279,end:131.599,text:"金价上涨，黄金股照样可能亏。"},
  {start:132.013,end:133.343,text:"而且不只是终点不同。"},
  {start:133.989,end:142.029,text:"第二段里，Au 九九点九九的最大回撤约百分之七点一七，五一八八八零约百分之七点四九，五一七五二零却达到百分之二十三点五九。"},
  {start:142.219,end:146.029,text:"也就是从阶段高点往下掉时，黄金股这一路明显更颠簸。"},
  {start:146.411,end:147.261,text:"再看积存金。"},
  {start:147.576,end:153.896,text:"查到的工行数据显示，主动积存价和赎回价同为每克九百九十三点七九元。"},
  {start:154.788,end:160.588,text:"即使报价没变，如果买入和赎回都按百分之零点五手续费示意，刚买再卖也大约先少百分之一。"},
  {start:160.727,end:161.787,text:"实物金也有交易摩擦。"},
  {start:161.942,end:166.912,text:"工行的参考回购数据里，不同类别的黄金，参考回购价就存在差异。"},
  {start:167.319,end:171.879,text:"但这只是不同类别的回购价差，不是同一根金条的即时买卖价差。"},
  {start:172.12,end:175.12,text:"所以答案很明确：不会自动同涨百分之十。"},
  {start:176.883,end:180.913,text:"金条和积存金更直接跟金价，但会扣掉溢价、手续费和回购差异；"},
  {start:181.262,end:183.642,text:"实物黄金ETF还有费用与跟踪误差；"},
  {start:184.105,end:187.125,text:"黄金股则多了一整套公司经营和估值变量。"},
  {start:187.458,end:191.718,text:"以后再看带“黄金”的产品，我会先问四件事：买到的是什么权利？"},
  {start:192.037,end:193.737,text:"收益来自金价还是公司经营？"},
  {start:194.639,end:197.169,text:"买入、持有、卖出各有什么成本？"},
  {start:197.418,end:198.678,text:"什么情况下会偏离金价？"},
  {start:199.33,end:203.01,text:"这两段历史只能证明偏离发生过，不能预测下一段行情。"},
  {start:203.294,end:205.874,text:"银行规则也会变，交易前要再核对。"},
] as const;

const SceneFrame=({id,durationInFrames}:{id:number;durationInFrames:number})=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const [title,sub]=scenes[id-1];
 const enter=spring({frame,fps,config:{damping:24,stiffness:125,mass:1.05}});
 const exit=interpolate(frame,[Math.max(0,durationInFrames-12),durationInFrames-1],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.quad)});
 const drift=interpolate(frame,[0,durationInFrames],[0,id%2===0?-10:10],{extrapolateRight:'clamp'});
 const chartReveal=[17,19].includes(id)?interpolate(frame,[4,Math.min(durationInFrames-8,42)],[0,100],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.out(Easing.cubic)}):100;
 const isBroll=id===9||id===25;
 return <AbsoluteFill style={{...base,background:C.bg,overflow:'hidden',opacity:exit}}>
  <div style={{position:'absolute',inset:0,opacity:.035,backgroundImage:'repeating-linear-gradient(0deg,#fff 0,#fff 1px,transparent 1px,transparent 8px)'}}/>
  {!isBroll&&<><div style={{position:'absolute',left:70,top:75,fontSize:24,letterSpacing:5,color:C.gray}}>GOLD / ASSAY NOTE　{String(id).padStart(2,'0')}</div><div style={{position:'absolute',left:70,right:70,top:135,borderTop:`2px solid ${C.graph}`}}/></>}
  <div style={{position:'absolute',inset:id===31?'175px 0 180px':'175px 0 500px',display:'grid',placeItems:'center',transform:`translateY(${(1-enter)*34+drift}px) scale(${0.965+enter*.035})`,opacity:enter,clipPath:`inset(0 ${100-chartReveal}% 0 0)`}}>
   {isBroll?<><Video src={staticFile(id===9?'video/sc09-mine.mp4':'video/sc25-gold-assay.mp4')} muted loop style={{width:'100%',height:'100%',objectFit:'cover',filter:'brightness(.66) saturate(.78)',transform:`scale(${1+frame/durationInFrames*.045})`}}/><div style={{position:'absolute',inset:0,background:'linear-gradient(transparent 38%,#11100Eee 88%)'}}/></>:<Visual id={id}/>} 
  </div>
  {id!==31&&<div style={{position:'absolute',left:70,right:70,bottom:260,opacity:enter,transform:`translateY(${(1-enter)*24}px)`}}><div style={{fontSize:53,fontWeight:850,lineHeight:1.12,maxWidth:900}}>{title}</div><div style={{fontSize:27,color:C.gold,marginTop:23,letterSpacing:1}}>{sub}</div></div>}
 </AbsoluteFill>;
};

const PhraseCaption=()=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const t=frame/fps;
 if(t>=206.496)return null;
 const item=captions.find(c=>t>=c.start&&t<=c.end); if(!item)return null;
 const p=interpolate(t,[item.start,Math.min(item.start+.18,item.end)],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <div style={{position:'absolute',left:70,right:70,bottom:70,display:'flex',justifyContent:'center',zIndex:20,opacity:p}}><div style={{fontFamily:font,fontSize:42,fontWeight:650,lineHeight:1.35,color:C.paper,background:'#11100Edd',padding:'14px 22px 17px',borderRadius:8,boxShadow:'0 8px 28px #0009',textAlign:'center',maxWidth:940}}>{item.text}</div></div>;
};

export const HuangjinDomesticVideo=()=>{
 const {fps}=useVideoConfig();
 return <AbsoluteFill style={{background:C.bg}}>
  {timeline.map(([start,end],i)=>{const from=Math.round(start*fps); const to=Math.round(end*fps); return <Sequence key={i} from={from} durationInFrames={to-from} premountFor={fps}><SceneFrame id={i+1} durationInFrames={to-from}/></Sequence>;})}
  <Audio src={staticFile('audio/narration_full_cn_v2.mp3')} volume={1}/>
  <PhraseCaption/>
 </AbsoluteFill>;
};

export const HuangjinCover=()=> <AbsoluteFill style={{...base,background:C.bg,overflow:'hidden'}}>
 <Img src={staticFile('images/cover-bg-codex-v2.png')} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover'}}/>
 <div style={{position:'absolute',inset:0,background:'linear-gradient(180deg,#080807ed 0%,#080807bf 31%,transparent 57%,#08080745 76%,#080807d9 100%)'}}/>
 <div style={{position:'absolute',inset:0,boxShadow:'inset 0 0 120px #000b'}}/>
 <div style={{position:'absolute',left:66,right:66,top:62}}>
  <div style={{fontSize:21,letterSpacing:6,color:'#B8B1A5'}}>GOLD / DOMESTIC ASSAY</div>
  <div style={{marginTop:54,fontSize:96,fontWeight:900,lineHeight:1.03,letterSpacing:-3,textShadow:'0 5px 24px #000'}}>黄金涨 <span style={{color:'#E1B75D'}}>10%</span><br/>它们都涨 10% 吗？</div>
  <div style={{marginTop:34,display:'inline-block',border:'3px double #D8AD55',color:'#E0B65D',padding:'13px 20px',fontWeight:800,fontSize:30,transform:'rotate(-1.5deg)',background:'#090908bd'}}>同名 ≠ 同涨</div>
 </div>
 <div style={{position:'absolute',left:60,right:60,bottom:54}}>
  <div style={{display:'flex',gap:13,flexWrap:'wrap'}}>{['金条','积存金','518880','517520'].map((x,i)=><div key={x} style={{border:`2px solid ${[C.gold,C.paper,C.paper,C.teal][i]}`,borderRadius:999,padding:'11px 19px',fontSize:24,color:[C.gold,C.paper,C.paper,C.teal][i],background:'#080807cf'}}>{x}</div>)}</div>
  <div style={{marginTop:21,borderTop:'2px solid #6D675E',paddingTop:17,fontSize:21,color:'#BBB3A6'}}>国内数据实验 · Au99.99 / 黄金ETF / 黄金股ETF</div>
 </div>
</AbsoluteFill>;

export const HuangjinFullRoot=()=> <><Composition id="HuangjinDomestic" component={HuangjinDomesticVideo} durationInFrames={6495} fps={30} width={1080} height={1920}/><Composition id="HuangjinDomesticCover" component={HuangjinCover} durationInFrames={1} fps={30} width={1080} height={1440}/></>;

export const HuangjinReviewRoot=()=> <Composition id="HuangjinReview" component={ReviewFilmstrip} durationInFrames={31} fps={30} width={1080} height={1920}/>;
