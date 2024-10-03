/*top-panel.js*/
window.onscroll = function() {
   var currentScrollPos = window.pageYOffset;
   if (currentScrollPos > 100) {
     document.querySelector(".top-panel").style.top = "-60px";
     document.querySelector(".logo").style.top = "-100px";
   } else {
     document.querySelector(".top-panel").style.top = "120px";
     document.querySelector(".logo").style.top = "20px"; 
   }
};
