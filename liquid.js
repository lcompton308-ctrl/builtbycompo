/* Built by Compo: flowing "liquid" background.
   Red pools with yellow bands winding between them, drawn on the graphics chip (WebGL).
   Calmer in the middle of the screen so the text stays readable.
   If WebGL isn't available the page keeps its plain CSS background. */
(function () {
  var canvas = document.getElementById("liquid");
  if (!canvas) return;

  // Colours as 0-1 RGB. Change these to re-theme the background.
  var PRIMARY = [244 / 255, 41 / 255, 2 / 255];    // #F42902 red orange
  var SECONDARY = [200 / 255, 253 / 255, 2 / 255]; // #C8FD02 yellow
  var SPEED = 0.16;          // how fast the pattern flows
  var SCALE = 1.3;           // bigger number = smaller pools
  var RESOLUTION = 0.5;      // draws at half size and lets the browser smooth it (saves battery)

  var gl = canvas.getContext("webgl", { antialias: false, alpha: false, premultipliedAlpha: false, powerPreference: "low-power" });
  if (!gl) return;

  var vert = "attribute vec2 a;void main(){gl_Position=vec4(a,0.0,1.0);}";
  var frag = [
    "#ifdef GL_FRAGMENT_PRECISION_HIGH",
    "precision highp float;",
    "#else",
    "precision mediump float;",
    "#endif",
    "uniform vec2 u_res; uniform float u_t; uniform vec3 u_a; uniform vec3 u_b; uniform float u_scale; uniform float u_px;",
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
    // calm zone behind the text so the yellow wording stays readable
    " vec2 c=(gl_FragCoord.xy-0.5*u_res)/s; c.y+=0.02;",
    " float calm=smoothstep(0.16,0.62,length(c*vec2(0.95,1.5)));",
    " vec2 q=(gl_FragCoord.xy-vec2(u_res.x,0.0))/u_px;",
    // and calm in the bottom-right corner behind the email address
    " float calmE=smoothstep(0.6,1.25,length(q/vec2(250.0,85.0)));",
    " float k=band*mix(0.25,0.85,calm)*mix(0.12,1.0,calmE);",
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
  gl.uniform1f(gl.getUniformLocation(prog, "u_px"), RESOLUTION);

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var speed = reduce ? SPEED * 0.35 : SPEED;

  function resize() {
    var w = Math.max(1, Math.round(canvas.clientWidth * RESOLUTION));
    var h = Math.max(1, Math.round(canvas.clientHeight * RESOLUTION));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; gl.viewport(0, 0, w, h); }
    gl.uniform2f(uRes, w, h);
  }
  window.addEventListener("resize", resize);
  resize();

  var start = performance.now(), offset = Math.random() * 50;
  function frame(now) {
    resize();
    gl.uniform1f(uT, offset + (now - start) / 1000 * speed);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  canvas.classList.add("on");
})();
