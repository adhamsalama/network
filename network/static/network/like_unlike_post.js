document.addEventListener("DOMContentLoaded", () => {
    let buttons = document.querySelectorAll(".like_unlike_button");
    for(let i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function() {
            let post_div = buttons[i].parentElement;
            let post_id = post_div.id.slice(5);
            console.log(buttons[i].innerHTML);
            //return false;
            const request = new Request("/like_unlike", {headers: {'X-CSRFToken': getCookie("csrftoken")}})
            fetch(request, {
                method: 'POST',
                body: JSON.stringify({
                    post_id: post_id,
                    action: buttons[i].innerHTML.toLowerCase(),            
                })
              })
              .then(response => response.json())
              .then(result => {
                    // Print result
                    console.log(result);
                    let likes_count = document.querySelector(`#post-${post_id}-likes`);
                    if (buttons[i].innerHTML == "Like"){
                      buttons[i].innerHTML = "Unlike";
                      likes_count.innerHTML = parseInt(likes_count.innerHTML) + 1;
                    }
                    else {
                        buttons[i].innerHTML = "Like";
                        likes_count.innerHTML = parseInt(likes_count.innerHTML) - 1;
                    }
                  
              });
        }
    }

})