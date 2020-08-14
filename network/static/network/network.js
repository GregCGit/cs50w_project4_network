document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM handler");
    document.querySelector('#new_post').addEventListener('click', new_post);

    // By default, load the all posts
    show_posts('all');

});

function show_posts(post_filter) {
    // As we add views, add functionality here to hide / block
    // Get the list of posts
    console.log("Filter", post_filter)
    fetch('/get_posts/' + post_filter)
    .then(response => response.json())
    .then(posts => {
        // Print posts
        console.log(posts);
    });
}

function new_post() {
    console.log("Made it inside of new post JSS");

    fetch('/new_post', {
        method: 'POST',
        credentials: 'same-origin',
        body: JSON.stringify({
            entry: document.querySelector('#new_entry').value
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        if (result.error) {
          alert(result.error)
        }
    });
    
  }