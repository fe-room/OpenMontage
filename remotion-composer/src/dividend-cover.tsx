import React from "react";
import {AbsoluteFill, Composition, Img, registerRoot, staticFile} from "remotion";

const C = {paper: "#F2EBDD", ink: "#18201D", red: "#A84432", blue: "#60727B", green: "#596B45", white: "#FFFDF7"};
const sans = '"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif';
const serif = '"Songti SC","STSong","SimSun",serif';
const mono = '"SFMono-Regular","Menlo","Consolas",monospace';

const Cover: React.FC = () => <AbsoluteFill style={{background:C.paper,color:C.ink,fontFamily:sans,overflow:"hidden"}}>
  <Img src={staticFile("cover_codex_bg_v1.png")} style={{position:"absolute",inset:0,width:"100%",height:"100%",objectFit:"cover"}}/>
  <div style={{position:"absolute",inset:"0 0 auto 0",height:505,background:"linear-gradient(180deg, #F3E8D2 0%, #F3E8D2F2 76%, #F3E8D200 100%)"}}/>
  <div style={{position:"absolute",left:62,right:62,top:50,display:"flex",justifyContent:"space-between",fontFamily:mono,fontSize:20,fontWeight:800,letterSpacing:3,color:C.blue}}>
    <span>DIVIDEND DOSSIER</span><span>两本账</span>
  </div>
  <div style={{position:"absolute",left:62,right:62,top:96,height:2,background:C.ink,opacity:.32}}/>
  <div style={{position:"absolute",left:62,right:50,top:145,fontFamily:serif,fontSize:102,fontWeight:900,lineHeight:1.04,letterSpacing:-4,textShadow:"0 1px 0 #FFF7E8"}}>
    只吃股息，<br/><span style={{color:C.red}}>真能不管股价？</span>
  </div>

  <div style={{position:"absolute",left:68,top:715,width:425,background:"#F8F0E1",borderLeft:`10px solid ${C.green}`,padding:"22px 26px 24px",boxShadow:"0 10px 24px #18201D22"}}>
    <div style={{fontSize:22,fontWeight:800,color:C.green,letterSpacing:2}}>分红收据</div>
    <div style={{marginTop:8,fontFamily:mono,fontSize:61,fontWeight:900,color:C.green,lineHeight:1}}>+5,000元</div>
    <div style={{marginTop:12,fontSize:27,fontWeight:800}}>照常到账 ✓</div>
  </div>
  <div style={{position:"absolute",right:52,top:760,width:425,background:"#E9DDC9",borderLeft:`10px solid ${C.red}`,padding:"22px 24px 24px",boxShadow:"0 10px 24px #18201D22"}}>
    <div style={{fontSize:22,fontWeight:800,color:C.red,letterSpacing:2}}>股票市值账</div>
    <div style={{marginTop:8,fontFamily:mono,fontSize:57,fontWeight:900,color:C.red,lineHeight:1}}>10万 → 5万</div>
    <div style={{marginTop:12,fontSize:27,fontWeight:800}}>本金只剩一半 ↓</div>
  </div>
  <div style={{position:"absolute",left:62,right:62,bottom:52,background:C.ink,color:C.paper,padding:"22px 28px",display:"flex",justifyContent:"space-between",alignItems:"center",boxShadow:"0 10px 26px #18201D28"}}>
    <span style={{fontFamily:serif,fontSize:34,fontWeight:800}}>分红和市值，同时都是真的</span>
    <span style={{fontFamily:mono,fontSize:19,color:"#D6E3B6",fontWeight:800}}>必须一起看</span>
  </div>
</AbsoluteFill>;

const DividendCoverRoot: React.FC = () => <Composition id="DividendPriceCover" component={Cover} durationInFrames={1} fps={30} width={1080} height={1440}/>;

registerRoot(DividendCoverRoot);
