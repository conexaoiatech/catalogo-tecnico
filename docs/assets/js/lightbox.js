(function(){
  // Ampliacao de imagens marcadas com data-zoom. Sem JS a imagem continua visivel normalmente.
  var overlay = null, lastFocus = null;

  function close(){
    if(!overlay) return;
    document.body.classList.remove('lb-open');
    overlay.parentNode.removeChild(overlay);
    overlay = null;
    document.removeEventListener('keydown', onKey);
    if(lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function onKey(e){
    if(e.key === 'Escape' || e.key === 'Esc'){ e.preventDefault(); close(); }
  }

  function open(img){
    lastFocus = document.activeElement;
    overlay = document.createElement('div');
    overlay.className = 'lb-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', img.getAttribute('alt') || 'Imagem ampliada');

    var big = document.createElement('img');
    big.src = img.currentSrc || img.src;
    big.alt = img.getAttribute('alt') || '';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'lb-close';
    btn.setAttribute('aria-label', 'Fechar');
    btn.textContent = '×';

    overlay.appendChild(big);
    overlay.appendChild(btn);
    // clique fora da imagem ou no X fecha; clique na imagem nao fecha (permite pinch e arrasto)
    overlay.addEventListener('click', function(e){ if(e.target !== big) close(); });
    document.body.appendChild(overlay);
    document.body.classList.add('lb-open');
    document.addEventListener('keydown', onKey);
    btn.focus();
  }

  document.addEventListener('click', function(e){
    var t = e.target;
    if(t && t.tagName === 'IMG' && t.hasAttribute('data-zoom') && !overlay){
      e.preventDefault();
      open(t);
    }
  });
})();
