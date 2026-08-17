/**
 * NEXT PRO — JS do template
 * Vanilla JS, sem dependência de jQuery ou frameworks. Objetivo: manter o
 * bundle mínimo (performance em hospedagem compartilhada).
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    initHeaderScrollState();
    initSubmenuKeyboardAccess();
    initRevealOnScroll();
    initContadores();
    initFiltroAssistencias();
  });

  /** Menu off-canvas mobile: abre/fecha, trava scroll do body, fecha com ESC */
  function initMobileNav() {
    var toggle = document.querySelector("[data-np-nav-toggle]");
    var nav = document.querySelector("[data-np-mobile-nav]");
    var closeBtn = document.querySelector("[data-np-nav-close]");
    if (!toggle || !nav) return;

    function openNav() {
      nav.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      var firstLink = nav.querySelector("a");
      if (firstLink) firstLink.focus();
    }
    function closeNav() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      toggle.focus();
    }

    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.contains("is-open");
      isOpen ? closeNav() : openNav();
    });
    if (closeBtn) closeBtn.addEventListener("click", closeNav);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) closeNav();
    });
  }

  /** Header ganha classe ao rolar a página, permitindo estado visual diferente via CSS */
  function initHeaderScrollState() {
    var header = document.querySelector("[data-np-header]");
    if (!header) return;
    var lastState = false;
    function onScroll() {
      var scrolled = window.scrollY > 12;
      if (scrolled !== lastState) {
        header.classList.toggle("is-scrolled", scrolled);
        lastState = scrolled;
      }
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /**
   * Entrada suave dos blocos ao rolar. Uma vez só por elemento, e só se o
   * usuário não pediu movimento reduzido no sistema.
   */
  function initRevealOnScroll() {
    var alvos = document.querySelectorAll(".np-reveal");
    if (!alvos.length) return;

    var semMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (semMovimento || !("IntersectionObserver" in window)) return; // fica tudo visível

    // só agora o CSS passa a esconder os blocos para animá-los
    document.documentElement.classList.add("np-anim");

    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("is-visivel");
        observador.unobserve(entrada.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    alvos.forEach(function (el) { observador.observe(el); });
  }

  /**
   * Contagem animada dos números institucionais. O valor final já está no HTML
   * (data-numero), então quem não tem JS continua vendo o número certo.
   */
  function initContadores() {
    var numeros = document.querySelectorAll("[data-numero]");
    if (!numeros.length || !("IntersectionObserver" in window)) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        animar(entrada.target);
        observador.unobserve(entrada.target);
      });
    }, { threshold: 0.5 });

    numeros.forEach(function (el) { observador.observe(el); });

    function animar(el) {
      var destino = parseFloat(el.getAttribute("data-numero"));
      if (isNaN(destino)) return;
      var sufixo = el.getAttribute("data-sufixo") || "";
      var duracao = 900;
      var inicio = null;
      function passo(t) {
        if (inicio === null) inicio = t;
        var p = Math.min((t - inicio) / duracao, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(destino * eased).toLocaleString("pt-BR") + sufixo;
        if (p < 1) requestAnimationFrame(passo);
      }
      requestAnimationFrame(passo);
    }
  }

  /**
   * Filtro de assistências técnicas por estado.
   * Progressive enhancement: sem JS, todas as assistências aparecem na página
   * e o formulário de filtro fica escondido (classe np-filtro[hidden]).
   */
  function initFiltroAssistencias() {
    var filtro = document.querySelector("[data-np-filtro-uf]");
    var lista = document.querySelector("[data-np-lista-assistencias]");
    if (!filtro || !lista) return;

    filtro.hidden = false;
    var itens = Array.prototype.slice.call(lista.querySelectorAll("[data-uf]"));
    var select = filtro.querySelector("select");
    var contagem = filtro.querySelector("[data-np-contagem]");
    var vazio = document.querySelector("[data-np-vazio]");
    var titulo = document.querySelector("[data-np-titulo-uf]");

    var NOMES = {
      BA: "Bahia", MS: "Mato Grosso do Sul", MG: "Minas Gerais", PR: "Paraná",
      PE: "Pernambuco", RJ: "Rio de Janeiro", RS: "Rio Grande do Sul",
      SC: "Santa Catarina", SP: "São Paulo"
    };

    function aplicar() {
      var uf = select.value;
      var visiveis = 0;
      itens.forEach(function (item) {
        var mostra = uf === "" || item.getAttribute("data-uf") === uf;
        item.hidden = !mostra;
        if (mostra) visiveis++;
      });
      if (contagem) {
        contagem.textContent = visiveis === 1
          ? "1 assistência encontrada"
          : visiveis + " assistências encontradas";
      }
      if (titulo) {
        titulo.textContent = uf === ""
          ? "Todas as assistências autorizadas"
          : "Assistências em " + (NOMES[uf] || uf);
      }
      if (vazio) vazio.hidden = visiveis !== 0;

      // guarda a escolha na URL, para o link poder ser compartilhado
      if (window.history && window.history.replaceState) {
        var url = new URL(window.location.href);
        if (uf) { url.searchParams.set("uf", uf); } else { url.searchParams.delete("uf"); }
        window.history.replaceState({}, "", url);
      }
    }

    // estado inicial vindo da URL (?uf=SP)
    var params = new URLSearchParams(window.location.search);
    var ufInicial = (params.get("uf") || "").toUpperCase();
    if (ufInicial && select.querySelector('option[value="' + ufInicial + '"]')) {
      select.value = ufInicial;
    }

    select.addEventListener("change", aplicar);
    aplicar();
  }

  /** Garante que o submenu de Produtos também abre via teclado (Tab), não só hover */
  function initSubmenuKeyboardAccess() {
    var items = document.querySelectorAll("[data-np-has-submenu]");
    items.forEach(function (item) {
      var link = item.querySelector(":scope > a");
      var submenu = item.querySelector(".np-nav__submenu");
      if (!link || !submenu) return;
      link.setAttribute("aria-haspopup", "true");
      link.setAttribute("aria-expanded", "false");
      item.addEventListener("focusin", function () {
        link.setAttribute("aria-expanded", "true");
      });
      item.addEventListener("focusout", function (e) {
        if (!item.contains(e.relatedTarget)) {
          link.setAttribute("aria-expanded", "false");
        }
      });
    });
  }
})();
