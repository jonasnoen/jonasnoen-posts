function guy(x,y,s,t,o={}){g.save();g.translate(x,y);g.scale(s,s);
  const bob=Math.sin(t*3)*4;g.translate(0,bob);
  // body: black t-shirt
  rr(-118,-40,236,260,80);g.fillStyle='#1c1b21';g.fill();g.strokeStyle='rgba(185,166,255,.45)';g.lineWidth=5;g.stroke();
  g.fillStyle=C.skin;g.beginPath();g.moveTo(-40,-42);g.quadraticCurveTo(0,-5,40,-42);g.closePath();g.fill();
  g.strokeStyle='#2c2a33';g.lineWidth=8;g.beginPath();g.moveTo(-44,-42);g.quadraticCurveTo(0,0,44,-42);g.stroke();
  // arms: short black sleeve + skin forearm
  const ang=o.point? -0.9+Math.sin(t*6)*.05 : (o.wave? -1.6+Math.sin(t*9)*.45 : 0.45);
  g.lineCap='round';
  g.strokeStyle=C.skin;g.lineWidth=36;
  g.beginPath();g.moveTo(-100,40);g.lineTo(-152,158);g.stroke();
  g.beginPath();g.moveTo(100,40);g.lineTo(100+140*Math.cos(ang),40+140*Math.sin(ang));g.stroke();
  g.strokeStyle='#1c1b21';g.lineWidth=50;
  g.beginPath();g.moveTo(-100,30);g.lineTo(-118,78);g.stroke();
  g.beginPath();g.moveTo(100,30);g.lineTo(100+50*Math.cos(ang),40+50*Math.sin(ang));g.stroke();
  g.fillStyle=C.skin;g.beginPath();g.arc(100+150*Math.cos(ang),40+150*Math.sin(ang),24,0,7);g.arc(-158,168,24,0,7);g.fill();
  // neck
  g.fillStyle='#e6b893';g.fillRect(-32,-70,64,40);
  // ears
  g.fillStyle=C.skin;g.beginPath();g.ellipse(-98,-140,20,30,0,0,7);g.ellipse(98,-140,20,30,0,0,7);g.fill();
  g.fillStyle='#e0a988';g.beginPath();g.ellipse(-98,-140,9,17,0,0,7);g.ellipse(98,-140,9,17,0,0,7);g.fill();
  // head: slim, longer oval with defined jaw
  g.fillStyle=C.skin;g.beginPath();g.moveTo(-96,-190);g.bezierCurveTo(-100,-80,-70,-50,0,-42);g.bezierCurveTo(70,-50,100,-80,96,-190);g.bezierCurveTo(90,-300,-90,-300,-96,-190);g.fill();
  // stubble (jaw + upper lip)
  g.fillStyle='rgba(92,70,58,.2)';g.beginPath();g.moveTo(-90,-125);g.bezierCurveTo(-88,-70,-60,-48,0,-44);g.bezierCurveTo(60,-48,88,-70,90,-125);g.bezierCurveTo(60,-95,40,-112,0,-110);g.bezierCurveTo(-40,-112,-60,-95,-90,-125);g.fill();
  // faded sides
  g.fillStyle='rgba(58,42,34,.55)';g.beginPath();g.ellipse(-88,-200,18,46,.15,0,7);g.ellipse(88,-200,18,46,-.15,0,7);g.fill();
  // hair: textured top, receding M-hairline, tufts pointing up/right
  g.fillStyle=C.hair;g.beginPath();
  g.moveTo(-92,-205);g.bezierCurveTo(-96,-260,-70,-300,-20,-308);
  g.lineTo(-10,-330);g.lineTo(10,-310);g.lineTo(35,-338);g.lineTo(48,-306);g.lineTo(80,-322);g.lineTo(78,-292);g.lineTo(108,-290);g.lineTo(92,-262);
  g.bezierCurveTo(100,-240,96,-220,92,-205);
  g.bezierCurveTo(80,-235,62,-252,45,-250);   // right temple recess
  g.bezierCurveTo(30,-265,-25,-265,-40,-250);  // front hairline
  g.bezierCurveTo(-60,-252,-82,-235,-92,-205); // left temple recess
  g.fill();
  g.strokeStyle='#4d3a2e';g.lineWidth=5;g.lineCap='round';
  [[-50,-270,-30,-300],[-10,-272,10,-305],[25,-270,50,-300],[55,-262,82,-285]].forEach(([a,b,c2,d])=>{g.beginPath();g.moveTo(a,b);g.lineTo(c2,d);g.stroke();});
  // eyes
  const blink=(t%3.7)<.12;g.fillStyle=C.ink;
  if(blink){g.fillRect(-50,-163,30,5);g.fillRect(20,-163,30,5);} else {g.beginPath();g.ellipse(-35,-160,10,o.shock?16:12,0,0,7);g.ellipse(35,-160,10,o.shock?16:12,0,0,7);g.fill();g.fillStyle='#6f8fae';g.beginPath();g.arc(-35,-160,5,0,7);g.arc(35,-160,5,0,7);g.fill();g.fillStyle='#fff';g.beginPath();g.arc(-32,-164,3,0,7);g.arc(38,-164,3,0,7);g.fill();}
  // brows: straight, slightly heavy
  g.strokeStyle='#4a3628';g.lineWidth=8;g.lineCap='round';const bt=o.frown?7:-2;
  g.beginPath();g.moveTo(-60,-195+bt);g.lineTo(-16,-197-bt);g.moveTo(16,-197-bt);g.lineTo(60,-195+bt);g.stroke();
  // glasses: thin silver rectangles with double bridge
  g.strokeStyle='#b8bcc6';g.lineWidth=5;
  rr(-74,-186,66,52,12);g.stroke();rr(8,-186,66,52,12);g.stroke();
  g.beginPath();g.moveTo(-8,-168);g.quadraticCurveTo(0,-174,8,-168);g.moveTo(-60,-186);g.lineTo(60,-186);
  g.moveTo(-74,-176);g.lineTo(-96,-170);g.moveTo(74,-176);g.lineTo(96,-170);g.stroke();
  g.fillStyle='rgba(220,235,255,.12)';rr(-72,-184,62,48,10);g.fill();rr(10,-184,62,48,10);g.fill();
  // nose
  g.strokeStyle='#d69c7c';g.lineWidth=5;g.beginPath();g.moveTo(-4,-150);g.quadraticCurveTo(-10,-118,4,-114);g.stroke();
  // mouth
  g.fillStyle='#7a2f3a';const talk=o.talk&&speaking(t)?(5+Math.abs(Math.sin(t*22))*13):0;
  if(o.frown&&!talk){g.strokeStyle='#8a3d44';g.lineWidth=6;g.beginPath();g.arc(0,-70,20,1.2*Math.PI,1.8*Math.PI);g.stroke();}
  else if(talk){g.beginPath();g.ellipse(0,-88,18,talk,0,0,7);g.fill();}
  else{g.strokeStyle='#8a3d44';g.lineWidth=6;g.beginPath();g.arc(0,-104,20,.25*Math.PI,.75*Math.PI);g.stroke();}
  g.restore();}
