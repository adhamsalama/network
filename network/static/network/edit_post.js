document.addEventListener("DOMContentLoaded", () => {
    let buttons = document.querySelectorAll(".edit-post-button");
    //console.log(forms.parentElement);
    for (let i = 0; i < buttons.length; i++) {
            let edit_post = buttons[i].parentElement;
            let post_div = buttons[i].parentElement.parentElement;
            //console.log(forms[i].parentElement.childNodes);
            buttons[i].onclick = function() {
            console.log(post_div);
            let post_id = post_div.id.slice(5);
            //console.log(post_div);
            let text_div = post_div.childNodes[13];
            console.log(text_div.innerText);
            let textarea = document.createElement("textarea");
            textarea.name = "new_text";
            textarea.className = "form-control";
            textarea.id = `post-${post_id}-text`
            textarea.innerHTML =  text_div.innerHTML.trim();
            textarea.value =  text_div.innerHTML.trim()
            post_div.replaceChild(textarea, text_div);
            let save_button = document.createElement("button");
            save_button.className = "btn btn-primary save-post";
            //save_button.name = "save-but";
            save_button.innerHTML = "Save";
            edit_post.append(save_button);
            buttons[i].style.display = "none";
            save_button.onclick = function() {
            const request = new Request("/edit_post",
                {headers: {'X-CSRFToken': getCookie("csrftoken")}}
            );
            fetch(request, {
                method: 'POST',
                body: JSON.stringify({
                    post_id: post_id,
                    new_text: textarea.value,            
                })
              })
              .then(response => response.json())
              .then(result => {
                  // Print result
                  console.log(result);
                  save_button.remove();
                  buttons[i].style.display = "inline";
                  text_div.innerHTML = textarea.value;
                  post_div.replaceChild(text_div, textarea);
                 
              });
                }
            
        }
    }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}