(function(){
  function norm(s){return (s||'').trim().toLowerCase().replace(/^@/,'');}
  var cat = '';
  function apply(inp){
    var q = norm(inp ? inp.value : '');
    var items = document.querySelectorAll(inp ? inp.dataset.target : 'li.pc'), shown = 0;
    items.forEach(function(el){
      var ok = (!q || el.dataset.name.indexOf(q) !== -1) && (!cat || (' '+(el.dataset.cats||'')+' ').indexOf(' '+cat+' ') !== -1);
      el.hidden = !ok; if (ok) shown++;
    });
    if (inp && inp.dataset.toc) document.querySelectorAll(inp.dataset.toc).forEach(function(li){ li.hidden = q && li.dataset.name.indexOf(q) === -1; });
    var c = document.querySelector('.count b'); if (c) c.textContent = shown;
    var em = document.querySelector('.empty'); if (em) em.hidden = shown !== 0;
  }
  var inputs = document.querySelectorAll('.filter input');
  inputs.forEach(function(inp){
    inp.addEventListener('input', function(){
      inputs.forEach(function(o){ if (o !== inp) o.value = inp.value; });
      apply(inp);
    });
  });
  document.querySelectorAll('.seg').forEach(function(b){
    b.addEventListener('click', function(){
      document.querySelectorAll('.seg').forEach(function(x){ x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); });
      cat = b.dataset.cat; apply(inputs[0]);
    });
  });
  // close mobile toc after jump
  document.querySelectorAll('.mtoc a').forEach(function(a){ a.addEventListener('click', function(){ a.closest('details').open = false; }); });
  // scrollspy
  var links = document.querySelectorAll('.side .toc a');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {}; links.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function(es){
      es.forEach(function(en){
        if (en.isIntersecting) { links.forEach(function(a){ a.classList.remove('act'); }); var a = map[en.target.id]; if (a) a.classList.add('act'); }
      });
    }, {rootMargin: '-90px 0px -65% 0px'});
    Object.keys(map).forEach(function(id){ var el = document.getElementById(id); if (el) io.observe(el); });
  }
})();
