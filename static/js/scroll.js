$(window).on('load',function(){
    $('.category-tab').on('click', function() {
        setTimeout(function() {
 
        window.scrollBy({ top: 1, left: 0, behavior: 'smooth' });
           
          },200);
          setTimeout(function() {
     
            window.scrollBy({ top: -1, left: 0, behavior: 'smooth' });
           
          },400);
    });
});
