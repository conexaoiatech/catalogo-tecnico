(function(){
  // Pagina do perfil: ?de={slug do sistema} ajusta trilha, botao voltar e anterior/proximo.
  // Sem JS, ou com ?de= ausente ou invalido, vale o padrao biblioteca gravado no HTML.
  var nav = document.getElementById('perfil-nav');
  if(!nav) return;
  var m = /[?&]de=([^&#]*)/.exec(window.location.search);
  if(!m) return;
  var slug;
  try { slug = decodeURIComponent(m[1]); } catch(e){ return; }
  var cats;
  try { cats = JSON.parse(nav.getAttribute('data-cats') || '{}'); } catch(e){ return; }
  if(!Object.prototype.hasOwnProperty.call(cats, slug)) return;

  var c = cats[slug];
  var base = nav.getAttribute('data-base') || '';
  var q = '?de=' + encodeURIComponent(slug);

  var niveis = document.querySelectorAll('#trilha a');
  if(niveis.length >= 3){
    niveis[1].textContent = c.nome;
    niveis[1].setAttribute('href', base + c.pagina);
    niveis[2].setAttribute('href', window.location.pathname.split('/').pop() + q);
  }
  var voltar = document.getElementById('voltar');
  if(voltar){
    voltar.textContent = '\u2190 Voltar para ' + c.nome;
    voltar.setAttribute('href', base + c.pagina);
  }

  function troca(id, alvo, texto, rel){
    var el = document.getElementById(id);
    if(!el) return;
    var novo;
    if(alvo){
      novo = document.createElement('a');
      novo.setAttribute('href', base + alvo.pagina + q);
      novo.setAttribute('rel', rel);
      novo.textContent = texto.replace('{c}', alvo.codigo);
    } else {
      novo = document.createElement('span');
      novo.className = 'pn-off';
      novo.textContent = texto.replace(' ({c})', '');
    }
    novo.id = id;
    el.parentNode.replaceChild(novo, el);
  }
  troca('pn-ant', c.ant, '\u2039 anterior ({c})', 'prev');
  troca('pn-prox', c.prox, 'pr\u00f3ximo \u203a ({c})', 'next');
})();
