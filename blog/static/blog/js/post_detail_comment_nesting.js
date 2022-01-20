window.addEventListener("load", function(){

   var commentList = document.getElementsByClassName('comments');

   for(var i=0; i < commentList.length; i++){
       var comment = commentList[i].getAttribute('class');
       var sonOf = comment.slice(-1); // check if this comment has a father comment
       // if the last char of the class name of the comment are int numbers (son of someone)
       if(!isNaN(parseInt(sonOf))) {
         var parentQuery1 = 'comment-' + sonOf;
         var parentQuery2 = 'comment-' + sonOf + '-alt';
         parentOptionOne = document.getElementById(parentQuery1)
         if (parentOptionOne == null) {
            var nodes = document.querySelectorAll('#' + parentQuery2 + ' div.comment-descendants > div.collapse > div.card > div.comments-children');
            nodes[0].innerHTML += commentList[i].outerHTML;
            commentList[i+1].remove();

         } else {
            var nodes = document.querySelectorAll('#' + parentQuery1 + ' div.comment-descendants > div.collapse > div.card > div.comments-children');
            nodes[0].innerHTML += commentList[i].outerHTML;
            commentList[i+1].remove();
         };
       };
     };
});

window.addEventListener("load", function(){
    commentsList = document.getElementsByClassName("comments");
    for (let i = 0; i < commentsList.length; i++) {
        var nodes = document.querySelectorAll('#' + commentsList[i].id + ' div.comment-descendants > div.collapse.show > div.card > div.comments-children');
        if (nodes[0].innerHTML.length < 2) {
           var emptyDescendants = document.querySelectorAll('#' + commentsList[i].id + ' div.comment-descendants')[0];
           emptyDescendants.style.display = "block";
           emptyDescendants.style.display = "none";
        }
    }

});

window.addEventListener("load", function(){
    var commentCollapseButtons = document.querySelectorAll('.comment-collapse-btn')
    for (let i = 0; i < commentCollapseButtons.length; i++) {
        commentCollapseButtons[i].addEventListener("click", function(){

            if (commentCollapseButtons[i].textContent.includes("+")) {
                commentCollapseButtons[i].textContent = commentCollapseButtons[i].textContent.replace("+", "-");
            } else if (commentCollapseButtons[i].textContent.includes("-")) {
                  commentCollapseButtons[i].textContent = commentCollapseButtons[i].textContent.replace("-", "+");
            };
      })
    };
});