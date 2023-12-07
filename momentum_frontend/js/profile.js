import * as ElementBuilder from "./util/element_builder.js"
import * as gql from "./util/gql.js"

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

var communities = [];
var posts = [];
var setup = false;

const clear_inputs = () => {
    communities = [];
    posts = [];
    document.getElementById("join-community-name").value = "";
    document.getElementById("create-community-name").value = "";
    document.getElementById("create-community-description").value = "";
}

const logout = () => {
    localStorage.clear();
    redirect("landing");
}

const render = async () => {
    setup = false;
    let uid = parseInt(localStorage.getItem("uid"));
    if(uid == null || isNaN(uid)){
        logout();
    }

    let user = await gql.get_user_with_rid(uid);

    document.getElementById("username-disp").innerHTML = user.username + " | ";
    console.log(user);
    if(user.communities != null){
        for(let i = 0; i < user.communities.length; i++){
            let raw_desc = user.communities[i].description.split("%");
            let name = raw_desc[0];
            let desc = raw_desc[1];
            communities.push({
                rid: user.communities[i].rid,
                name: name,
                description: desc,
                member_cnt: user.communities[i].users.length,
                post_cnt: (user.communities[i].posts == null ? 0 : user.communities[i].posts.length)
            });
        }
    }
    if(user.posts != null){
        for(let i = 0; i < user.posts.length; i++){
            if(user.posts[i].community == null){
                continue;
            }
            let num_comments = 0;
            if(user.posts[i].comments != null){
                num_comments = user.posts[i].comments.length;
            }
            posts.push({
                content: user.posts[i].content,
                timestamp: user.posts[i].timestamp.substring(0, user.posts[i].timestamp.indexOf("T")),
                comm_name: user.posts[i].community.description.split("%")[0],
                comm_rid: user.posts[i].community.rid,
                num_comments: num_comments
            });
        }
    }
    console.log(communities);

    let community_content = "";
    let posts_content = "";
    
    if(communities.length > 0){
        community_content = `
            <h3>Your Communities:</h3>
            <ul style="list-style: none;">
        `
        for(let i = 0; i < communities.length; i++){
            let community = communities[i];
            community_content += `
                <li>
                    <a id="comm-link-${community.rid}" class="discrete-a">
                        <div class="dialog-box">
                            <h3>${community.name}</h3>
                            <p>Members: ${community.member_cnt}</p>
                            <p>New posts: ${community.post_cnt}</p>
                        </div>
                    </a>
                </li>
                <br>
            `
        }
        community_content += `
            </ul>
        `
    } else {
        community_content = `
            <h3>Your Communities:</h3>
            <t>No communities found</t>
        `
    }
    if(posts.length > 0){
        posts_content = `
            <h3>Your Posts:</h3>
            <ul style="list-style: none;">
        `
        for(let i = 0; i < posts.length; i++){
            let post = posts[i];
            posts_content += `
                <li>
                    <a id="comm-link-post-${post.comm_rid}" class="discrete-a">
                        <div class="dialog-box">
                            <t><strong>Posted on:</strong> ${post.timestamp} | <strong>Posted in:</strong> ${post.comm_name}<t>
                            <hr>
                            <p>
                                ${post.content}
                            </p>
                            <hr>
                            <t>Number of comments: ${post.num_comments}
                        </div>
                    </a>
                </li>
                <br>
            `
        }
        posts_content += `
            </ul>
        `
    } else {
        posts_content = `
            <h3>Your Posts:</h3>
            <t>No posts found</t>
        `
    }

    document.getElementById("community-list").innerHTML = community_content;
    document.getElementById("post-list").innerHTML = posts_content;

    for(let i = 0; i < communities.length; i++){
        let community = communities[i];
        document.getElementById(`comm-link-${community.rid}`).addEventListener("click", () => {
            localStorage.setItem("community", community.rid);
            redirect("community", "", false);
        });
        document.getElementById(`comm-link-post-${community.rid}`).addEventListener("click", () => {
            localStorage.setItem("community", community.rid);
            redirect("community", "", false);
        });
    }
    setup = true;
}

const join_community = async () => {
    if(!setup){
        return;
    }
    let community_rid = document.getElementById("join-community-name").value;
    if(community_rid.length == 0){
        alert("Please enter a valid community ID");
        return;
    }
    let comm = await gql.get_community_with_rid(community_rid);
    if(comm == null){
        alert("That community does not exist!");
        return;
    }
    for(let i = 0; i < communities.length; i++){
        if(communities[i].rid == community_rid){
            alert("You are already in that community!");
            return;
        }
    }
    let uid = parseInt(localStorage.getItem("uid"));
    await gql.add_user_to_community(uid, communities, community_rid);

    clear_inputs();
    render();
}

const add_community = async () => {
    if(!setup){
        return;
    }
    let community_name = document.getElementById("create-community-name").value;
    let community_desc = document.getElementById("create-community-description").value;

    if(community_name.length == 0 || community_desc.length == 0){
        alert("Please enter a name and description");
        return;
    }
    if(community_name.includes("%") || community_desc.includes("%")){
        alert("Please use a name and description with characters [A-Z][a-z]");
        return;
    }

    let uid = parseInt(localStorage.getItem("uid"));
    await gql.create_community(community_name, community_desc, uid, communities);

    clear_inputs();
    render();
}

const setup_event_handlers = () => {
    document.getElementById("create-community-btn").addEventListener("click", add_community);
    document.getElementById("join-community-btn").addEventListener("click", join_community);
    document.getElementById("logout-link").addEventListener("click", logout);
}

setup_event_handlers();
clear_inputs();
render();