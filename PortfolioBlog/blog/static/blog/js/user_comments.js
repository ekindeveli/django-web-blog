// Remove duplicate titles and stack comments under one title for User Comments page
window.addEventListener("load", function(){

   var commentContainer = document.getElementsByClassName('comment-container');

   for(var i=0; i < commentContainer.length; i++){
       var article1 = commentContainer[i].getElementsByTagName('ARTICLE')[0];
       for(var t=i+1; t < commentContainer.length; t++){
           var article2 = commentContainer[t].getElementsByTagName('ARTICLE')[0];
           if (article1.innerHTML == article2.innerHTML) {
                var div1 = commentContainer[t].getElementsByClassName('comments')[0];
                commentContainer[i].getElementsByClassName('post-comments')[0].append(div1);
                commentContainer[t].remove();
                t -= 1
           }
       }
   }
});

