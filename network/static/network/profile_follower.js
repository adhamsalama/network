document.addEventListener("DOMContentLoaded", () => {
        
    let form = document.querySelector("#follow_form");
    if (form) {
    let action = document.querySelector("#follow_action");
    let followed_user_id = document.querySelector("#followed_user_id").value;
    form.onsubmit = function() {
            console.log(action.value);
            const request = new Request("/follow_unfollow",
            
            {headers: {'X-CSRFToken': getCookie("csrftoken")}}
            );
            fetch(request, {
                method: 'POST',
                body: JSON.stringify({
                    followed_user_id: followed_user_id,
                    action: action.value,            
                })
              })
              .then(response => response.json())
              .then(result => {
                  // Print result
                  console.log(result);
                  let button = document.querySelector("#follow_unfollow_button");
                  let count = document.querySelector("#followers_count");
                  if (action.value == "follow") {
                        action.value="unfollow";
                        button.innerHTML = "Unfollow";
                        count.innerHTML = parseInt(count.innerHTML) + 1;
                  }
                  else {
                        action.value="follow";
                        button.innerHTML = "Follow";
                        count.innerHTML = parseInt(count.innerHTML) - 1;
                    }                 
              });
        
        return false;
    }
}
})
