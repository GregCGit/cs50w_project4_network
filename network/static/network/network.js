document.addEventListener('DOMContentLoaded', function() {
    if (is_authenticated == 'True') {
        if (filter == 'all') {
            document.querySelector('#new_post').addEventListener('click', new_post);
        }

        if (filter != 'all' && flw != 1 && filter != cur_user_id) {
            document.querySelector('#change_follow').addEventListener('click', change_follow);
        }
    }
});


function change_follow() {
    fetch('/change_follow', {
        method: 'POST',
        credentials: 'same-origin',
        body: JSON.stringify({
            cur_user_id: cur_user_id,
            req_user_id: filter
        })
    })
    location.reload()
}

function change_like(post_id) {
    console.log("Inside JS chng_like", cur_user_id, "AND", post_id);
    fetch('/change_like', {
        method: 'POST',
        credentials: 'same-origin',
        body: JSON.stringify({
            cur_user_id: cur_user_id,
            post_id: post_id
        })
    });
    // Update the button state and count

    if (document.querySelector('#clb' + post_id).value == "Like") {
       document.querySelector('#clb' + post_id).value = 'Unlike';
       document.querySelector('#lkc' + post_id).innerHTML++;
    }
    else {
        document.querySelector('#clb' + post_id).value = 'Like';
        document.querySelector('#lkc' + post_id).innerHTML--;
    }
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
        //show_posts('all');
    });

}

function edit_post(post_id) {
    console.log("Made it inside of edit post JSS", post_id);
    let epost = document.querySelector('#entry' + post_id);
    let original_post = epost.innerHTML;

    // Change the text to textarea
    let new_post = document.createElement('div');
    let new_form = document.createElement('form');
    let new_text_area = document.createElement('textarea');
    new_text_area.classList.add('form-control');
    new_text_area.id = 'epta' + post_id;
    new_text_area.innerHTML = original_post;
    new_form.appendChild(new_text_area)
    new_post.appendChild(new_form);
    epost.innerHTML = new_post.innerHTML;

    // Change edit to save
    let epb = document.querySelector('#epb' + post_id);
    epb.className = 'btn btn-primary';
    epb.setAttribute('onclick',"javascript:save_edited_post('" + post_id + "')");
    epb.value = 'Save';

}

function save_edited_post(post_id) {
    console.log("Made it inside of save edited post JSS", post_id);
    let updated_entry = document.querySelector('#epta' + post_id).value
    console.log('UP', updated_entry)

    fetch('/update_post', {
        method: 'POST',
        credentials: 'same-origin',
        body: JSON.stringify({
            id: post_id,
            entry: updated_entry
        })
    })

    // Change text are back to text using updated_entry
    document.querySelector('#entry' + post_id).innerHTML = updated_entry;

    // Change edit to save
    let epb = document.querySelector('#epb' + post_id);
    epb.className = 'btn btn-outline-primary';
    epb.setAttribute('onclick',"javascript:edit_post('" + post_id + "')");
    epb.value = 'Edit';
}