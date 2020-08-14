document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM handler");
    document.querySelector('#new_post').addEventListener('click', new_post);

    // By default, load the all posts
    show_posts('all');

});

function show_posts(post_filter) {
    // As we add views, add functionality here to hide / block
    document.querySelector('#new_entry').value = '';
    // Get the list of posts
    console.log("Filter", post_filter)
    document.querySelector('#list-view').innerHTML = `<h3>${post_filter.charAt(0).toUpperCase() + post_filter.slice(1)}</h3>`;
    fetch('/get_posts/' + post_filter)
    .then(response => response.json())
    .then(posts => {
        // Print posts
        console.log(posts);
        if (posts.error) {
            alert(posts.error)
        }
        else {
            let postlist = document.querySelector('#list-view');
            posts.forEach(build_list);

            function build_list(post) {
                console.log("Build List", post);
                // Build each row - most properties are set at the end
                let display_posts = document.createElement('div');
                display_posts.classList.add("posting");
          
                // Next build the three elements
                let post_owner = document.createElement('div');
                post_owner.appendChild(document.createTextNode(post.user));
                post_owner.classList.add('owner');
          
                let post_entry = document.createElement('div');
                post_entry.appendChild(document.createTextNode(post.entry));
                post_entry.classList.add('entry');
          
                let post_like = document.createElement('div');
                post_like.appendChild(document.createTextNode("Likes " + post.like));
                post_like.classList.add('like');

                let post_ulike = document.createElement('div');
                if (post.user_like) {
                    post_ulike.appendChild(document.createTextNode("I like "));
                    post_ulike.classList.add('ulike');
                }
                let post_timestamp = document.createElement('div');
                post_timestamp.appendChild(document.createTextNode(post.timestamp));
                post_timestamp.classList.add('timestamp');
          
                // TBD Need to handle likes
          
                display_posts.appendChild(post_owner);
                display_posts.appendChild(post_entry);
                display_posts.appendChild(post_like);
                display_posts.appendChild(post_ulike);
                display_posts.appendChild(post_timestamp);
                postlist.appendChild(display_posts);
              }
        }
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
    .then(results => {
        // Print result
        console.log(results);
        if (results.error) {
          alert(results.error)
        }
        show_posts('all');
    });
    
  }