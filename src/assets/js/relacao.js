/* Relação de peças: filtro por sistema (esconde as linhas que não pertencem ao sistema) e ?de= do link da linha. */
(function () {
  var linhas = document.querySelectorAll(".rel-linha");
  var botoes = document.querySelectorAll(".rel-filtro");
  if (!linhas.length || !botoes.length) return;

  function aplica(slug) {
    botoes.forEach(function (b) {
      var ativo = b.getAttribute("data-filtro") === slug;
      b.classList.toggle("ativo", ativo);
      b.setAttribute("aria-pressed", ativo ? "true" : "false");
    });
    linhas.forEach(function (l) {
      var sistemas = (l.getAttribute("data-sistemas") || "").split(" ");
      var mostra = slug === "todos" || sistemas.indexOf(slug) !== -1;
      l.hidden = !mostra;
      // mantém a navegação ?de=: com filtro ativo o link volta para o sistema filtrado
      var link = l.querySelector(".rel-esticado");
      if (link && mostra) link.href = link.getAttribute("data-base") + "?de=" + (slug === "todos" ? sistemas[0] : slug);
    });
  }

  botoes.forEach(function (b) {
    b.addEventListener("click", function () { aplica(b.getAttribute("data-filtro")); });
  });
})();
