// Simulation d'équilibrage : reprend les formules de combat de valdor/index.html
const rnd=(a,b)=>a+Math.random()*(b-a),clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),pick=a=>a[Math.floor(Math.random()*a.length)];
const RM=[1,1.25,1.55,1.9,2.4];
function gear(L0,r,type){const COV=+(process.env.COV||.65),L=Math.max(1,L0-2),m=RM[r]*COV,s={atk:0,def:0,hp:0,spd:0,crit:0};
  s.atk+=(4+L*2.2)*m*(type==="hammer"?1.15:type==="axe"?1.05:type==="flail"?1.1:1);if(type==="sword")s.spd+=1+r;
  s.def+=(1+L*.8)*m;s.hp+=(6+L*4)*m;s.hp+=(12+L*8)*m;s.def+=(2+L*1.1)*m;s.crit+=(2+L*.35)*m;s.spd+=(1+L*.25)*m;
  if(r>=1){s.hp+=4*(5+L*3)*r*.6*.2;s.atk+=4*(1+L*.4)*r*.6*.2;s.def+=4*(1+L*.4)*r*.6*.2}return s}
function hero(L,r,type){const s={hp:90+L*18,atk:8+L*2.5,def:2+L*.9,spd:10+L*.15,crit:5},g=gear(L,r,type);for(const k in s)s[k]=Math.round(s[k]+g[k]);return s}
const P=JSON.parse(process.env.P||'{}');
const BB=Object.assign({hp0:100,hpL:24,atk0:8,atkL:2.5,def0:2,defL:1},P);
const MOD=Object.assign({goblin:{hp:.8,atk:.95,spd:1.35},troll:{hp:1.6,atk:1,spd:.75,def:1.25},spectre:{hp:1,atk:1.1,spd:1.4},dragon:{hp:1.9,atk:1.1,def:1.2,spd:.9}},P.MOD||{});
function boss(kind,L){const b={hp:BB.hp0+L*BB.hpL,atk:BB.atk0+L*BB.atkL,def:BB.def0+L*BB.defL,spd:10+L*.15,crit:6};for(const k in MOD[kind])b[k]*=MOD[kind][k];for(const k in b)b[k]=Math.round(b[k]);return b}
const MV={sword:[[1],[.45,.45,.65],[.45,.45,.65],[.95],[.6,.8]],hammer:[[1.45],[1.45],[.6,.8],[.95],[1]],axe:[[1.45],[1],[.45,.45,.65],[.95],[.6,.8]],flail:[[1.45],[.45,.45,.65],[.6,.8],[1],[.95]],
  troll:[[1.45],[1.45],[1],[.95]],spectre:[[1.1],[1.1],[.45,.45,.65],[1]],dragon:[[1.15],[1.25]],goblin:[[1.45],[1],[.45,.45,.65],[.95],[.6,.8]]};
function fight(A,B,akind,bkind){const F=[{s:A,hp:A.hp,max:A.hp,atb:Math.random()*40,mv:MV[akind],kind:akind,en:false},{s:B,hp:B.hp,max:B.hp,atb:Math.random()*40,mv:MV[bkind],kind:bkind,en:false}];
  for(let t=0;t<4000;t++){for(const f of F)f.atb+=f.s.spd;const a=F.find(f=>f.atb>=100*3.4/3.4*10);if(!a)continue;a.atb-=1000;const d=a===F[0]?F[1]:F[0];
    for(const frac of pick(a.mv)){const s=a.s,ds=d.s;
      if(Math.random()<clamp(.05+(ds.spd-s.spd)*.006+(d.kind==="spectre"?.08:0),.03,.28))continue;
      let dmg=s.atk*rnd(.88,1.12)*frac;if(a.en)dmg*=1.3;const crit=Math.random()*100<s.crit;if(crit)dmg*=1.8;
      const block=!crit&&d.kind!=="dragon"&&Math.random()<clamp(.07+(ds.def-s.atk*.25)*.008,.04,.22);
      dmg=Math.max(1,Math.round(dmg-ds.def*.6*frac));if(block)dmg=Math.max(1,Math.round(dmg*.4));
      d.hp-=dmg;if(["troll","spectre","dragon","goblin"].includes(d.kind)&&!d.en&&d.hp<d.max*.5)d.en=true;
      if(d.hp<=0)return a===F[0]}}return false}
function rate(fn,n=3000){let w=0;for(let i=0;i<n;i++)if(fn())w++;return Math.round(w/n*100)}
const arenaK=P.arena||[.82,.3];
console.log("ARÈNE (même niveau, adversaire = héros ×k)");
for(const L of [1,5,10,15])console.log(`  niv ${L}: équipement commun ${rate(()=>{const h=hero(L,0,"sword"),k=arenaK[0]+Math.random()*arenaK[1],o={};for(const x in h)o[x]=Math.round(h[x]*(x==="spd"?rnd(.9,1.1):k));return fight(h,o,"sword",pick(["sword","axe","hammer","flail"]))})}% victoires`);
console.log("BOSS (héros au niveau indiqué, équipement de rareté r)");
for(const [kind,BL] of [["goblin",3],["troll",6],["spectre",10],["dragon",15]])
  for(const [hl,r] of [[BL-2,0],[BL-2,1],[BL,1],[BL+2,1],[BL+2,2]])console.log(`  ${kind} niv ${BL} | héros niv ${hl}, rareté ${r}: ${rate(()=>fight(hero(hl,r,"sword"),boss(kind,BL),"sword",kind))}%`);
