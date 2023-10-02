import * as ElementBuilder from "./util/element_builder.js"
import * as gql from "./util/gql.js"

const redirect = (page) => {
    let curr_url = window.location.href;
    let toks = curr_url.split('/');
    toks[toks.length - 1] = `${page}.html`;
    let new_url = toks.join("/");
    window.location.href = new_url;
}

var communities = []

const clear_inputs = () => {
    document.getElementById("join-community-name").value = "";
    document.getElementById("create-community-name").value = "";
    document.getElementById("create-community-description").value = "";
}

const logout = () => {
    localStorage.clear();
    redirect("landing");
}

const render = async () => {
    let uid = parseInt(localStorage.getItem("uid"));
    let user = await gql.get_user_with_rid(uid);

    document.getElementById("username-disp").innerHTML = user.username + " | ";
    console.log(user);

    for(let i = 0; i < user.communities.length; i++){
        let ok = false;
        for(let j = 0; j < user.communities[i].users.length; j++){
            if(user.communities[i].users[j].rid == uid){
                ok = true;
                break;
            }
        }
        if(!ok){
            continue;
        }
        communities.push({
            name: "TestCommunity",
            description: user.communities.description,
            member_cnt: user.communities[i].users.length,
            post_cnt: 0
        });
    }

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
                    <a class="discrete-a">
                        <div class="dialog-box">
                            <h3>${community.name}</h3>
                            <p>Members: ${community.member_cnt}</p>
                            <p>New posts: ${community.post_cnt}</p>
                        </div>
                    </a>
                </li>
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

    posts_content = `
        <h3>Your Posts:</h3>
        <t>No posts found</t>
    `

    document.getElementById("community-list").innerHTML = community_content;
    document.getElementById("post-list").innerHTML = posts_content;
}

const add_community = async () => {
    let community_name = document.getElementById("create-community-name").value;
    let community_desc = document.getElementById("create-community-description").value;

    let uid = parseInt(localStorage.getItem("uid"));
    await gql.create_community(community_desc, uid);

    clear_inputs();
    render();
}

const setup_event_handlers = () => {
    document.getElementById("create-community-btn").addEventListener("click", add_community);
    document.getElementById("logout-link").addEventListener("click", logout);
}

setup_event_handlers();
clear_inputs();
render();