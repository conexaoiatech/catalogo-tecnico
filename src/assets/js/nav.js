(function(){
  var raiz = document.documentElement;

  // ---- Menu em gaveta (celular/tablet) ----
  var botao = document.getElementById('menu-toggle');
  var menu = document.getElementById('menu-sistemas');
  var fundo = document.getElementById('menu-fundo');

  function abre(){
    raiz.classList.add('menu-aberto');
    botao.setAttribute('aria-expanded', 'true');
    botao.setAttribute('aria-label', 'Fechar menu');
    if(fundo) fundo.hidden = false;
    var primeiro = menu.querySelector('a');
    if(primeiro) primeiro.focus();
  }
  function fecha(devolveFoco){
    raiz.classList.remove('menu-aberto');
    botao.setAttribute('aria-expanded', 'false');
    botao.setAttribute('aria-label', 'Abrir menu');
    if(fundo) fundo.hidden = true;
    if(devolveFoco) botao.focus();
  }

  if(botao && menu){
    botao.addEventListener('click', function(){
      if(botao.getAttribute('aria-expanded') === 'true') fecha(true); else abre();
    });
    if(fundo) fundo.addEventListener('click', function(){ fecha(true); });
    menu.addEventListener('click', function(e){ if(e.target.tagName === 'A') fecha(false); });
    document.addEventListener('keydown', function(e){
      if((e.key === 'Escape' || e.key === 'Esc') && botao.getAttribute('aria-expanded') === 'true'){
        e.preventDefault();
        fecha(true);
      }
    });
    window.addEventListener('resize', function(){
      if(window.innerWidth > 1100 && botao.getAttribute('aria-expanded') === 'true') fecha(false);
    });
  }

  // ---- Sub-navegacao por secoes (paginas de sistema) ----
  var subNavGroups = Array.prototype.slice.call(document.querySelectorAll('.section-nav'));
  function setActiveSub(){
    subNavGroups.forEach(function(nav){
      var links = Array.prototype.slice.call(nav.querySelectorAll('a'));
      var targets = links.map(function(a){ return document.getElementById(a.getAttribute('href').substring(1)); }).filter(Boolean);
      var scrollY = window.scrollY + 160;
      var currentIdx = -1;
      targets.forEach(function(t, i){ if(t.offsetTop <= scrollY) currentIdx = i; });
      links.forEach(function(a, i){ a.classList.toggle('current', i === currentIdx); });
    });
  }
  if(subNavGroups.length){
    window.addEventListener('scroll', setActiveSub, {passive:true});
    setActiveSub();
  }

  // ---- Revelacao ao rolar (so se o usuario nao pediu menos movimento) ----
  var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!reduz && 'IntersectionObserver' in window){
    var alvos = document.querySelectorAll('.card-sistema, .profile-card, .diff-card, .block-head, .sealant-card, .cert-item, .capa-stats > div, .moldura-ficha, .perfil-dados');
    var io = new IntersectionObserver(function(entradas){
      entradas.forEach(function(en){
        if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, {threshold: 0.08});
    Array.prototype.forEach.call(alvos, function(el){ el.classList.add('reveal'); io.observe(el); });
  }
})();
