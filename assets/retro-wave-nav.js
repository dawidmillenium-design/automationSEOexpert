(function(){
  var tb=document.getElementById('rwTop');
  if(!tb)return;
  function onScroll(){tb.classList.toggle('rw-small',window.scrollY>40);}
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();
})();
