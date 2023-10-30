import * as ElementBuilder from "./util/element_builder.js"
import * as gql from "./util/gql.js"

/*
<div class="post-container">
    <div>
        <span><strong>John Doe</strong></span>
        <span> | @johndoe</span>
    </div>
    <div class="post-content">
        <p>This is a sample social media post. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
    </div>
    <div class="post-buttons">
        <button class="btn btn-secondary">Comment</button>
    </div>
</div>
*/

const logout = () => {
    localStorage.clear();
    redirect("landing");
}

const clear_inputs = () => {
    document.getElementById("post-submit").value = "";
}

const render = async () => {
    let uid = parseInt(localStorage.getItem("uid"));
    let comm_id = parseInt(localStorage.getItem("community"));

    if(uid == null || comm_id == null){
        logout();
    }

    let user = await gql.get_user_with_rid(uid);
    let comm = await gql.get_community_with_rid(comm_id);
    console.log(comm);
    let raw_desc = comm.description.split("%");
    let name = raw_desc[0];
    let desc = raw_desc[1];
    let num_posts = (comm.posts == null ? 0 : comm.posts.length);
    document.getElementById("username-disp").innerHTML = "Settings (NO-OP) | " + user.username + " | ";
    document.getElementById("comm-status").innerHTML = `${comm.users.length} member(s) | ${num_posts} posts | Community Code: ${comm.rid}`;
    document.getElementById("community-title").innerHTML = `Momentum | ${name}`;
    document.getElementById("comm-title").innerHTML = `${name}`;
    document.getElementById("comm-desc").innerHTML = `${desc}`;

    let postContent = "";
    for(let i = 0; i < num_posts; i++){
        let post = comm.posts[i];
        postContent += `
            <div class="post-container">
                <div>
                    <span><strong>${post.user.name}</strong></span>
                    <span> | @${post.user.username}</span>
                </div>
                <div class="post-content">
                    <p>${post.content}</p>
                </div>
                <div class="post-buttons">
                    <button class="btn btn-secondary">Comment (NO-OP)</button>
                </div>
            </div>
        `
    }
    document.getElementById("all-posts").innerHTML = postContent;
}

const submitPost = async () => {
    /*
    Source: https://stackoverflow.com/questions/7244246/generate-an-rfc-3339-timestamp-similar-to-google-tasks-api
    */
    function ISODateString(d){
        function pad(n){return n<10 ? '0'+n : n}
        return d.getUTCFullYear()+'-'
             + pad(d.getUTCMonth()+1)+'-'
             + pad(d.getUTCDate());
    }
    let text_content = document.getElementById("post-content").value;
    let uid = parseInt(localStorage.getItem("uid"));
    let comm_id = parseInt(localStorage.getItem("community"));
    let timestamp = ISODateString(new Date());

    await gql.create_post(uid, text_content, timestamp, comm_id);
    
    clear_inputs();
    render();
}

const setup_event_handlers = () => {
    document.getElementById("logout-link").addEventListener("click", logout);
    document.getElementById("post-submit").addEventListener("click", submitPost);
}

setup_event_handlers();
clear_inputs();
render();