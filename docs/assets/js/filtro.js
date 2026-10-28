(function(){
  // Filtro por sistema e busca na biblioteca de perfis. Sem JS todos os cards ficam visiveis.
  var box = document.getElementById('bib-filtros');
  var grid = document.getElementById('bib-grid');
  if(!box || !grid) return;
  box.hidden = false;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.profile-card'));
  var botoes = Array.prototype.slice.call(box.querySelectorAll('.bib-btn'));
  var campo = document.getElementById('bib-busca');
  var contagem = document.getElementById('bib-contagem');
  var sistema = '';

  function norm(t){
    t = (t || '').toLowerCase();
    return t.normalize ? t.normalize('NFD').replace(/[\u0300-\u036f]/g, '') : t;
  }

  function aplica(){
    var q = norm(campo.value).trim();
    var n = 0;
    cards.forEach(function(c){
      var cats = (c.getAttribute('data-cats') || '').split(' ');
      var ok = (!sistema || cats.indexOf(sistema) !== -1) && (!q || norm(c.getAttribute('data-busca')).indexOf(q) !== -1);
      c.hidden = !ok;
      if(ok) n++;
    });
    contagem.textContent = n + ' de ' + cards.length + ' perfis';
  }

  botoes.forEach(function(b){
    b.addEventListener('click', function(){
      sistema = b.getAttribute('data-filtro');
      botoes.forEach(function(x){ x.classList.toggle('current', x === b); });
      aplica();
    });
  });
  campo.addEventListener('input', aplica);
  aplica();
})();
