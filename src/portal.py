from common import *

PORTAL_CSS = """
.portal{max-width:520px}
.portal .tabs{display:flex;gap:0;margin:28px 0 22px;border-bottom:1px solid rgba(255,255,255,.12)}
.portal .tabs button{background:none;border:0;color:var(--muted);font-family:"Barlow Condensed";font-weight:600;text-transform:uppercase;letter-spacing:.18em;font-size:14px;padding:12px 18px 12px 0;margin-right:18px;cursor:pointer;border-bottom:2px solid transparent}
.portal .tabs button.on{color:#fff;border-color:#fff}
.portal form{display:grid;gap:14px}
.portal label{display:grid;gap:6px;font-family:"Barlow Condensed";font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:12.5px;letter-spacing:.2em;color:var(--muted)}
.portal input,.portal select{font:inherit;font-size:17px;color:#fff;background:var(--ink);border:1px solid rgba(255,255,255,.18);border-radius:0;padding:12px 14px;width:100%}
.portal input:focus,.portal select:focus{outline:none;border-color:#fff}
.portal .seg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.portal .seg input{display:none}
.portal .seg span{display:block;text-align:center;padding:12px;border:1px solid rgba(255,255,255,.18);border-radius:0;font-family:"Barlow Condensed";font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:15px;cursor:pointer;color:var(--muted)}
.portal .seg input:checked+span{border-color:#fff;background:#fff;color:var(--ink)}
.portal .err{color:#f3b2a6;font-size:14px;min-height:1.4em}
.portal .hint{font-size:13px;color:var(--muted)}
.files{display:grid;gap:12px;margin-top:22px}
.file{display:flex;gap:16px;align-items:center;background:var(--ink2);border:1px solid rgba(255,255,255,.08);padding:14px 16px;text-decoration:none;color:#fff}
.file .ic{flex:none;width:40px;height:40px;border:1px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-family:"Barlow Condensed";font-weight:600;font-size:11px;letter-spacing:.12em;color:#fff}
.file b{display:block;font-family:"Barlow Condensed";font-weight:500;font-size:19px;letter-spacing:.03em}
.file small{color:var(--muted);font-size:13px}
.file video{width:100%;max-height:420px;background:#000;margin-top:10px}
.file.video{display:block}
.file.video .row{display:flex;gap:16px;align-items:center}
.bikehead{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px;margin-top:10px}
.bikehead h2{font-size:clamp(34px,5vw,54px)}
.bikehead .num{font-family:"Barlow Condensed";font-weight:600;font-size:clamp(44px,7vw,80px);line-height:1}
"""

PORTAL_JS = r"""
(function(){
  var $=function(s){return document.querySelector(s)};
  var views={auth:$('#auth'),home:$('#home')};
  function show(v){for(var k in views)views[k].hidden=(k!==v);}
  function api(path,opts){return fetch('/api/'+path,Object.assign({credentials:'same-origin',headers:{'content-type':'application/json'}},opts||{})).then(function(r){return r.json().then(function(j){return {ok:r.ok,status:r.status,j:j}})}).catch(function(){return {ok:false,j:{error:'Could not reach the server. Try again in a moment.'}}})}
  // tabs
  var tabs=document.querySelectorAll('.tabs button');
  tabs.forEach(function(b){b.addEventListener('click',function(){tabs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');$('#login').hidden=b.dataset.t!=='login';$('#register').hidden=b.dataset.t!=='register';})});
  function vals(f){var o={};new FormData(f).forEach(function(v,k){o[k]=v});return o}
  $('#login').addEventListener('submit',function(e){e.preventDefault();var f=e.target,err=f.querySelector('.err');err.textContent='';f.querySelector('button').disabled=true;
    api('login',{method:'POST',body:JSON.stringify(vals(f))}).then(function(r){f.querySelector('button').disabled=false;if(r.ok){load();}else{err.textContent=r.j.error||'Sign-in failed.';}})});
  $('#register').addEventListener('submit',function(e){e.preventDefault();var f=e.target,err=f.querySelector('.err');err.textContent='';var v=vals(f);
    if(v.password!==v.password2){err.textContent='The two passwords don\'t match.';return}
    f.querySelector('button').disabled=true;
    api('register',{method:'POST',body:JSON.stringify(v)}).then(function(r){f.querySelector('button').disabled=false;if(r.ok){load();}else{err.textContent=r.j.error||'Registration failed.';}})});
  $('#logout').addEventListener('click',function(){api('logout',{method:'POST'}).then(function(){show('auth')})});
  // password reset
  function authView(v){['#login','#register','#resetreq','#resetform'].forEach(function(s){$(s).hidden=(s!==v)});$('.tabs').hidden=(v==='#resetreq'||v==='#resetform');}
  $('#to-reset').addEventListener('click',function(e){e.preventDefault();authView('#resetreq')});
  $('#to-login').addEventListener('click',function(e){e.preventDefault();authView('#login');tabs[0].classList.add('on');tabs[1].classList.remove('on')});
  $('#resetreq').addEventListener('submit',function(e){e.preventDefault();var f=e.target,err=f.querySelector('.err');err.textContent='';f.querySelector('button').disabled=true;
    api('reset-request',{method:'POST',body:JSON.stringify(vals(f))}).then(function(r){f.querySelector('button').disabled=false;if(r.ok){f.innerHTML='<p class="hint">'+(r.j.message||'If those details match our records, a reset link is on its way.')+'</p><p class="hint"><a href="owners.html" style="color:#fff">Back to sign in</a></p>';}else{err.textContent=r.j.error||'Could not send a reset link.';}})});
  var tok=new URLSearchParams(location.search).get('reset');
  if(tok){$('#resetform').token.value=tok;authView('#resetform');}
  $('#resetform').addEventListener('submit',function(e){e.preventDefault();var f=e.target,err=f.querySelector('.err'),v=vals(f);err.textContent='';
    if(v.password!==v.password2){err.textContent='The two passwords don\'t match.';return}
    f.querySelector('button').disabled=true;
    api('reset',{method:'POST',body:JSON.stringify({token:v.token,password:v.password})}).then(function(r){f.querySelector('button').disabled=false;if(r.ok){history.replaceState(null,'',location.pathname);load();}else{err.textContent=r.j.error||'That link didn\'t work.';}})});
  function size(n){return n>1048576?(n/1048576).toFixed(1)+' MB':Math.round(n/1024)+' KB'}
  function row(f){var isV=/^video\//.test(f.type),isP=f.type==='application/pdf',isI=/^image\//.test(f.type);var url='/api/file?key='+encodeURIComponent(f.key);
    if(isV){var d=document.createElement('div');d.className='file video';d.innerHTML='<div class="row"><span class="ic">VIDEO</span><div><b></b><small>'+size(f.size)+'</small></div></div><video controls preload="metadata" playsinline></video>';d.querySelector('b').textContent=f.title;d.querySelector('video').src=url;return d}
    var a=document.createElement('a');a.className='file';a.href=url;a.target='_blank';a.rel='noopener';a.innerHTML='<span class="ic">'+(isP?'PDF':isI?'IMG':'FILE')+'</span><div><b></b><small>'+size(f.size)+'</small></div>';a.querySelector('b').textContent=f.title;return a}
  function fill(id,list,empty){var el=$(id);el.innerHTML='';if(!list.length){el.innerHTML='<p class="hint">'+empty+'</p>';return}list.forEach(function(f){el.appendChild(row(f))})}
  function load(){api('me').then(function(r){if(!r.ok){show('auth');return}
    $('#owner-name').textContent=r.j.name?('Welcome back, '+r.j.name+'.'):'Welcome back.';$('#bike-model').textContent=r.j.modelName;$('#bike-num').textContent='No. '+r.j.number;
    fill('#mine',r.j.mine,'Nothing here yet – documents and videos for your motorcycle will appear as the build progresses.');
    fill('#shared',r.j.shared,'No shared documents yet.');show('home');})}
  load();
})();
"""

OWNERS = f"""
<section class="page-head" style="padding-bottom:0">
  <div class="wrap">
    <div class="kicker">Owners</div>
    <h1>Owners' portal</h1>
    <p class="lede">The build record, documents and videos for your motorcycle, from the people who made it.</p>
  </div>
</section>

<section id="auth" class="portal-wrap" hidden>
  <div class="wrap portal">
    <div class="tabs"><button type="button" class="on" data-t="login">Sign in</button><button type="button" data-t="register">First time here</button></div>
    <form id="login" autocomplete="on">
      <div class="seg"><label><input type="radio" name="model" value="lightspeed" checked><span>Lightspeed</span></label><label><input type="radio" name="model" value="two-stroke"><span>Two Stroke</span></label></div>
      <label>Build number<input name="number" inputmode="numeric" placeholder="e.g. 007" required autocomplete="username"></label>
      <label>Password<input name="password" type="password" required autocomplete="current-password"></label>
      <div class="err" aria-live="polite"></div>
      <button class="btn gold" type="submit">Sign in</button>
      <p class="hint">Forgotten your password? <a href="#" id="to-reset" style="color:#fff">Send yourself a reset link</a>, or email <a href="mailto:{MAIL}?subject=Owners%27%20portal%20%E2%80%93%20password%20reset" style="color:#fff">{MAIL}</a>.</p>
    </form>
    <form id="resetreq" autocomplete="on" hidden>
      <p class="hint">Enter your build number and the email address we hold for you. If they match, a link to choose a new password is on its way within a minute.</p>
      <div class="seg"><label><input type="radio" name="model" value="lightspeed" checked><span>Lightspeed</span></label><label><input type="radio" name="model" value="two-stroke"><span>Two Stroke</span></label></div>
      <label>Build number<input name="number" inputmode="numeric" placeholder="e.g. 007" required></label>
      <label>Email<input name="email" type="email" required autocomplete="email"></label>
      <div class="err" aria-live="polite"></div>
      <button class="btn gold" type="submit">Send reset link</button>
      <p class="hint"><a href="#" id="to-login" style="color:#fff">Back to sign in</a></p>
    </form>
    <form id="resetform" autocomplete="on" hidden>
      <p class="hint">Choose a new password for your motorcycle.</p>
      <input type="hidden" name="token">
      <label>New password<input name="password" type="password" minlength="10" required autocomplete="new-password"></label>
      <label>Repeat password<input name="password2" type="password" minlength="10" required autocomplete="new-password"></label>
      <div class="err" aria-live="polite"></div>
      <button class="btn gold" type="submit">Save and sign in</button>
    </form>
    <form id="register" autocomplete="on" hidden>
      <p class="hint">Your motorcycle came with an activation code. Enter it once here with your build number, choose a password, and you're in.</p>
      <div class="seg"><label><input type="radio" name="model" value="lightspeed" checked><span>Lightspeed</span></label><label><input type="radio" name="model" value="two-stroke"><span>Two Stroke</span></label></div>
      <label>Build number<input name="number" inputmode="numeric" placeholder="e.g. 007" required autocomplete="username"></label>
      <label>Activation code<input name="code" placeholder="From the card with your bike" required autocomplete="one-time-code"></label>
      <label>Choose a password<input name="password" type="password" minlength="10" required autocomplete="new-password"></label>
      <label>Repeat password<input name="password2" type="password" minlength="10" required autocomplete="new-password"></label>
      <div class="err" aria-live="polite"></div>
      <button class="btn gold" type="submit">Set up my access</button>
      <p class="hint">No code? Email <a href="mailto:{MAIL}?subject=Owners%27%20portal%20%E2%80%93%20activation%20code" style="color:#fff">{MAIL}</a> with your name and build number.</p>
    </form>
  </div>
</section>

<section id="home" hidden>
  <div class="wrap">
    <p class="lede" id="owner-name"></p>
    <div class="bikehead"><h2 id="bike-model"></h2><div class="num" id="bike-num"></div></div>
    <h3 style="font-size:20px;margin-top:44px;letter-spacing:.1em;font-weight:500">Your motorcycle</h3>
    <div class="files" id="mine"></div>
    <h3 style="font-size:20px;margin-top:44px;letter-spacing:.1em;font-weight:500">Owner documents</h3>
    <div class="files" id="shared"></div>
    <div class="btns" style="margin-top:40px"><a class="btn ghost" href="mailto:{MAIL}?subject=Owner%20question">Ask the team</a><button class="btn" type="button" id="logout">Sign out</button></div>
  </div>
</section>

<section class="light" id="press">
  <div class="wrap">
    <div class="kicker">Press</div>
    <h2 class="section-title">Press and media.</h2>
    <p class="lede">For interviews, test rides, images and the press kit, email the team directly. We answer quickly and we don't do holding statements.</p>
    <div class="btns" style="margin-top:24px"><a class="btn gold" href="{mailto('Press enquiry')}">Press enquiry</a></div>
  </div>
</section>
<style>.bar{{display:none}}body{{padding-bottom:0}}</style>
<script>{PORTAL_JS}</script>
"""
