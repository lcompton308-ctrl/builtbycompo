/* Built by Compo: flowing "liquid" background for the hero and footer.
   Red pools with yellow bands winding between them, drawn on the graphics chip (WebGL).
   The yellow is kept soft (STRENGTH) so it reads as a glow, not a stripe.
   If WebGL isn't available the page keeps its plain CSS background. */
function bbcLiquid(canvas) {

  // Colours as 0-1 RGB. Change these to re-theme the background.
  var PRIMARY = [244 / 255, 41 / 255, 2 / 255];    // #F42902 red orange
  var SECONDARY = [200 / 255, 253 / 255, 2 / 255]; // #C8FD02 yellow
  var SPEED = 0.16;          // how fast the pattern flows
  var SCALE = 1.3;           // bigger number = smaller pools
  var STRENGTH = 0.42;        // how strong the yellow is (0 to 1)
  // Firefox on Android struggles with this effect, so it gets a lighter version
  var LITE = /Android/i.test(navigator.userAgent) && /Firefox/i.test(navigator.userAgent);
  var RESOLUTION = LITE ? 0.25 : 0.4;   // draws smaller and lets the browser smooth it (saves battery)
  var INTERVAL = LITE ? 55 : 40;        // milliseconds between pictures

  var gl = canvas.getContext("webgl", { antialias: false, alpha: true, premultipliedAlpha: true, powerPreference: "low-power" });
  if (!gl) return;

  var vert = "attribute vec2 a;void main(){gl_Position=vec4(a,0.0,1.0);}";
  var frag = [
    "#ifdef GL_FRAGMENT_PRECISION_HIGH",
    "precision highp float;",
    "#else",
    "precision mediump float;",
    "#endif",
    "uniform vec2 u_res; uniform float u_t; uniform vec3 u_a; uniform vec3 u_b; uniform float u_scale; uniform float u_k;",
    // 3D simplex noise by Ian McEwan and Stefan Gustavson (MIT licence)
    "vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}",
    "vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}",
    "vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}",
    "vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}",
    "float snoise(vec3 v){",
    " const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0);",
    " vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);",
    " vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);",
    " vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy;",
    " i=mod289(i);",
    " vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));",
    " float n_=0.142857142857; vec3 ns=n_*D.wyz-D.xzx;",
    " vec4 j=p-49.0*floor(p*ns.z*ns.z); vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_);",
    " vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y);",
    " vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);",
    " vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0));",
    " vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;",
    " vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);",
    " vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));",
    " p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;",
    " vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m;",
    " return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));",
    "}",
    "void main(){",
    " float s=min(u_res.x,u_res.y);",
    " vec2 p=gl_FragCoord.xy/s*u_scale;",
    " float t=u_t;",
    // warp the space with slow noise so the shapes ooze rather than slide
    " vec2 w=vec2(snoise(vec3(p*0.7,t*0.8)),snoise(vec3(p*0.7+vec2(5.2,1.3),t*0.8)));",
    " float v=snoise(vec3(p+w*0.6,t));",
    // bands of the second colour along the noise contours, like the reference video
    " float band=1.0-smoothstep(0.0,0.46,abs(v));",
    " float k=band*u_k;",
    " vec3 col=mix(u_a,u_b,k);",
    " col*=1.0-0.10*smoothstep(0.45,0.95,abs(v));",
    " gl_FragColor=vec4(col,1.0);",
    "}"
  ].join("\n");

  function shader(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); }
    return s;
  }
  var prog;
  try {
    prog = gl.createProgram();
    gl.attachShader(prog, shader(gl.VERTEX_SHADER, vert));
    gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, frag));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  } catch (e) { return; }
  gl.useProgram(prog);

  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(prog, "a");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

  var uRes = gl.getUniformLocation(prog, "u_res"), uT = gl.getUniformLocation(prog, "u_t");
  gl.uniform3fv(gl.getUniformLocation(prog, "u_a"), PRIMARY);
  gl.uniform3fv(gl.getUniformLocation(prog, "u_b"), SECONDARY);
  gl.uniform1f(gl.getUniformLocation(prog, "u_scale"), SCALE);
  gl.uniform1f(gl.getUniformLocation(prog, "u_k"), parseFloat(canvas.dataset.strength) || STRENGTH);

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var speed = reduce ? SPEED * 0.35 : SPEED;

  function resize() {
    var w = Math.max(1, Math.round(canvas.clientWidth * RESOLUTION));
    var h = Math.max(1, Math.round(canvas.clientHeight * RESOLUTION));
    // Changing the size wipes the picture, so mark it to be drawn again straight away
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; gl.viewport(0, 0, w, h); needDraw = true; }
    gl.uniform2f(uRes, w, h);
  }
  var needDraw = true, lost = false;
  window.addEventListener("resize", function () { if (!lost) { resize(); draw(); } });
  // If the phone takes the graphics chip away, show the plain red (never black) and start again when it comes back
  canvas.addEventListener("webglcontextlost", function (e) { e.preventDefault(); lost = true; canvas.classList.remove("on"); });
  canvas.addEventListener("webglcontextrestored", function () { bbcLiquid(canvas); });
  resize();

  // Only draw while it is on screen. It holds still while the page is being scrolled, but is always
  // redrawn after a size change (phones resize as the address bar hides) so it can't be left black.
  var visible = false, t = Math.random() * 50, last = 0, sized = 0;
  if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) needDraw = true; }).observe(canvas);
  else visible = true;
  function draw() { gl.uniform1f(uT, t); gl.drawArrays(gl.TRIANGLES, 0, 6); needDraw = false; }
  function frame(now) {
    if (lost) return;
    requestAnimationFrame(frame);
    if (now - last < INTERVAL) return;
    var dt = Math.min(0.1, (now - (last || now)) / 1000); last = now;
    if (!visible) return;
    if (!sized || now - sized > 500) { resize(); sized = now; }
    if (needDraw) { draw(); return; }
    if (window.BBC_SCROLLING || window.BBC_PAUSED) return;
    t += dt * speed; draw();
  }
  requestAnimationFrame(frame);
  canvas.classList.add("on");
}
Array.prototype.forEach.call(document.querySelectorAll("canvas.liquid"), bbcLiquid);
