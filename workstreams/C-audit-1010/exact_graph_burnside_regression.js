function edgeOrbits(n,p){const visited=new Set(),E=n*(n-1)/2;let count=0;const key=(u,v)=>Math.min(u,v)*n+Math.max(u,v);for(let u=0;u<n;u++)for(let v=u+1;v<n;v++){let k=key(u,v);if(visited.has(k))continue;count++;while(!visited.has(k)){visited.add(k);let a=Math.floor(k/n),b=k%n;k=key(p[a],p[b])}}return count}

function enumeratePerm(n,visit){const p=Array.from({length:n},(_,i)=>i);function step(k){if(k===n){visit(p);return}for(let j=k;j<n;j++){[p[k],p[j]]=[p[j],p[k]];step(k+1);[p[k],p[j]]=[p[j],p[k]]}}step(0)}

function factorial(n){let x=1n;for(let i=2;i<=n;i++)x*=BigInt(i);return x}

function run(){const known=[1,1,2,4,11,34,156,1044,12346],rows=[];for(let n=3;n<=8;n++){let sum=0n,nonid=0n,perms=0;enumeratePerm(n,p=>{let k=edgeOrbits(n,p),fixed=1n<<BigInt(k);sum+=fixed;perms++;if(p.some((u,i)=>u!==i))nonid+=fixed});let g=sum/factorial(n),E=n*(n-1)/2; if(sum%factorial(n)!==0n||g!==BigInt(known[n]))throw Error("Burnside mismatch at "+n);let eps=Number(nonid)/2**E,trans=n*(n-1)/2*2**(-(n-2));rows.push({n,permutations:perms,unlabelledGraphs:Number(g),burnsideNonidentityCorrection:eps,transpositionContribution:trans})}return{method:"exact edge-orbit Burnside directly from all graph-edge permutations",result:"PASS",rows}}

console.log(JSON.stringify(run(),null,2));
