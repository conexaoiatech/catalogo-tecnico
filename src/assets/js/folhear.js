/* Relação de peças folheável (biblioteca de perfis): livro de 2 páginas no computador (a primeira sozinha, como capa)
   e 1 página no celular, com a biblioteca StPageFlip (assets/js/vendor/page-flip.browser.js, MIT, sem CDN).
   Setas, contador, teclado (← →) e arrastar com o dedo. Sem JS o bloco fica oculto e o <noscript> mostra o link do PDF. */
(function () {
  var raiz = document.getElementById("folhear");
  var livro = document.getElementById("folhear-livro");
  if (!raiz || !livro || typeof St === "undefined") return;

  var paginas = livro.querySelectorAll(".folhear-pagina");
  var total = paginas.length;
  var contador = document.getElementById("folhear-contador");
  var ant = raiz.querySelector(".folhear-ant");
  var prox = raiz.querySelector(".folhear-prox");

  raiz.hidden = false; // a biblioteca mede o contêiner: ele precisa estar visível antes de iniciar

  var pf = new St.PageFlip(livro, {
    width: 500, height: 707,          // proporção A4 retrato
    size: "stretch", minWidth: 260, maxWidth: 520, minHeight: 368, maxHeight: 736,
    showCover: true, usePortrait: true, autoSize: true,
    maxShadowOpacity: 0.45, flippingTime: 700, swipeDistance: 30, mobileScrollSupport: true
  });
  pf.loadFromHTML(paginas);

  function atualiza() {
    var i = pf.getCurrentPageIndex();
    var duas = pf.getOrientation() === "landscape" && i > 0 && i + 1 < total;
    contador.textContent = (duas ? (i + 1) + "–" + (i + 2) : (i + 1)) + " / " + total;
    ant.disabled = i <= 0;
    prox.disabled = i >= total - 1;
  }

  ant.addEventListener("click", function () { pf.flipPrev(); });
  prox.addEventListener("click", function () { pf.flipNext(); });
  pf.on("flip", atualiza);
  pf.on("changeOrientation", atualiza);
  pf.on("init", atualiza);
  atualiza();

  // teclado: só com o livro à vista e fora de campos de texto
  document.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    var t = e.target && e.target.tagName;
    if (t === "INPUT" || t === "TEXTAREA" || t === "SELECT" || e.altKey || e.ctrlKey || e.metaKey) return;
    var r = raiz.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight) return;
    e.preventDefault();
    if (e.key === "ArrowLeft") pf.flipPrev(); else pf.flipNext();
  });
})();
