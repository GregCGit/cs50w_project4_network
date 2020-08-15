document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new_post').addEventListener('click', new_post);
    //document.querySelector('#display-user').addEventListener('click', function() {
    //    show_posts(document.querySelector('#display-user-id').innerText)
    //});

    // By default, load the all posts
    relative_path = relative_path.slice(0,-1)
    console.log("R path", relative_path);
    console.log("auth", is_authenticated)
    show_posts(req_user_id);
    if (follow_needed) {
        show_follow(req_user_id)
    }

});

function show_posts(post_filter) {
    // As we add views, add functionality here to hide / block
    console.log("Made it to show_posts ", post_filter)
    if (post_filter == 'all' && is_authenticated == "True" ) {
        document.querySelector('#post-view').style.display = 'block';
        document.querySelector('#new_entry').value = '';
    }
    else {
        document.querySelector('#post-view').style.display = 'none';
    }

    // Get the list of posts
    console.log("Filter", post_filter)
    
    fetch('/get_posts/' + post_filter)
    .then(response => response.json())
    .then(posts => {
        // Print posts
        console.log(posts);
        if (posts.error) {
            alert(posts.error)
        }
        else {
            if (post_filter == "all") {
                list_h3 = "All"
            }
            else {
                list_h3 = "";
            }
            document.querySelector('#list-view').innerHTML = `<h3>${list_h3}</h3>`;
            let postlist = document.querySelector('#list-view');
            posts.forEach(build_list);

            function build_list(post) {
                //console.log("Build List", post);
                // Build each row - post
                let display_posts = document.createElement('div');
                display_posts.classList.add("posting");
          
                // Next build the elements
                let post_owner = document.createElement('a');
                post_owner.appendChild(document.createTextNode(post.user));
                post_owner.classList.add('owner');
                //post_owner.href = "profile/" + post.user_id
                post_owner.href = relative_path + post.user_id
                
          
                let post_entry = document.createElement('div');
                post_entry.appendChild(document.createTextNode(post.entry));
                post_entry.classList.add('entry');
          
                let post_like = document.createElement('div');
                post_like.appendChild(document.createTextNode("Likes " + post.like));
                post_like.classList.add('like');

                let post_ulike = document.createElement('div');
                // TBD the like / unlike button should go here
                if (post.user_like) {
                    post_ulike.appendChild(document.createTextNode("I like "));
                    post_ulike.classList.add('ulike');
                }

                let post_timestamp = document.createElement('div');
                post_timestamp.appendChild(document.createTextNode(post.timestamp));
                post_timestamp.classList.add('timestamp');
                    
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

function show_follow(req_user_id) {
    console.log("Calling show_follow", req_user_id)
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