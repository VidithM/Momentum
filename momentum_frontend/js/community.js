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
    <div id="comments-section-${post.rid}" class="comments-section">
        <div class="comment">
            <span><strong>Jane Smith</strong></span>
            <span> | @janesmith</span>
            <p>This is a great post!</p>
        </div>

        <div class="comment">
            <span><strong>Bob Johnson</strong></span>
            <span> | @bobjohnson</span>
            <p>Awesome content!</p>
        </div>
    </div>
</div>
*/

const redirect = (page, args = "", get_link = false) => {
    let curr_url = window.location.href;
    let toks = curr_url.split('/');
    toks[toks.length - 1] = `${page}.html`;
    let new_url = toks.join("/");
    if(args.length > 0){
        new_url = `${new_url}/${args}`;
    }
    if(get_link){
        return new_url;
    }
    window.location.href = new_url;
}

const logout = () => {
    localStorage.clear();
    redirect("landing");
}

const clear_inputs = () => {
    document.getElementById("post-content").value = "";
}

const render = async () => {
    let uid = parseInt(localStorage.getItem("uid"));
    let comm_id = localStorage.getItem("community");

    if((uid == null || comm_id == null) || isNaN(uid)){
        logout();
    }

    let user = await gql.get_user_with_rid(uid);
    console.log(comm_id);
    let comm = await gql.get_community_with_rid(comm_id);
    console.log(comm);
    let raw_desc = comm.description.split("%");
    let name = raw_desc[0];
    let desc = raw_desc[1];
    let num_posts = (comm.posts == null ? 0 : comm.posts.length);
    document.getElementById("username-disp").innerHTML = user.username + " | ";
    document.getElementById("comm-status").innerHTML = `${comm.users.length} member(s) | ${num_posts} posts | Community Code: ${comm.rid}`;
    document.getElementById("community-title").innerHTML = `Momentum | ${name}`;
    document.getElementById("comm-title").innerHTML = `${name}`;
    document.getElementById("comm-desc").innerHTML = `${desc}`;

    let postContent = "";
    for(let i = 0; i < num_posts; i++){
        let post = comm.posts[i];
        let date = post.timestamp.substring(0, post.timestamp.indexOf("T"));
        postContent += `
            <div class="post-container">
                <div>
                    <span><strong>${post.user.name}</strong></span>
                    <span> | @${post.user.username} | Posted on: ${date}</span>
                </div>
                <div class="post-content">
                    <p>${post.content}</p>
                </div>
                <div class="post-buttons">
                    <input id="comment-content-${post.rid}" type="text" class="search-input" placeholder="Enter comment">
                    <button id="comment-submit-${post.rid}" class="btn btn-secondary">Comment</button>
                </div>
                <br>
                <div id="comments-section-${post.rid}" class="comments-section">
                </div>
            </div>
        `
    }
    document.getElementById("all-posts").innerHTML = postContent;
    for(let i = 0; i < num_posts; i++){
        let post = comm.posts[i];
        render_post_comments(post);
        document.getElementById(`comment-submit-${post.rid}`).addEventListener("click", () => submitComment(post));
    }
}

const render_post_comments = async (post) => {
    let commentsContent = "";
    let rids = [];
    if(post.comments != null){
        for(let i = 0; i < post.comments.length; i++){
            rids.push(post.comments[i].rid);
        }
        let comments = await gql.get_comment_with_rid(rids);
        for(let i = 0; i < comments.length; i++){
            let comment = comments[i];
            console.log(comments[i]);
            commentsContent += `
                <div class="comment">
                    <span><strong>${comment.user.name}</strong></span>
                    <span> | @${comment.user.username}</span>
                    <p>${comment.content}</p>
                </div>
            `
        }
    }
    document.getElementById(`comments-section-${post.rid}`).innerHTML = commentsContent;
}

const getISODateString = (d) => {
    function pad(n){
        return n < 10 ? '0' + n : n
    }
    return d.getUTCFullYear()+'-'
            + pad(d.getUTCMonth()+1)+'-'
            + pad(d.getUTCDate());
}

const submitComment = async (post) => {
    let post_rid = post.rid;
    console.log(`submitted on ${post_rid}`);
    let text_content = document.getElementById(`comment-content-${post_rid}`).value;
    if(text_content.length == 0){
        alert("Please enter a valid comment!");
        return;
    }
    let uid = parseInt(localStorage.getItem("uid"));
    let timestamp = getISODateString(new Date());

    await gql.add_comment_to_post(uid, text_content, timestamp, post_rid);
    let new_post = await gql.get_post_with_rid(post_rid);
    post.comments = new_post.comments;

    document.getElementById(`comment-content-${post_rid}`).value = "";
    await render_post_comments(post);
}

const submitPost = async () => {
    /*
    Source: https://stackoverflow.com/questions/7244246/generate-an-rfc-3339-timestamp-similar-to-google-tasks-api
    */
    let text_content = document.getElementById("post-content").value;
    let uid = parseInt(localStorage.getItem("uid"));
    let comm_id = localStorage.getItem("community");
    let timestamp = getISODateString(new Date());

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