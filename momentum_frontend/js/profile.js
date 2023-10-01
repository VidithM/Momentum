import * as ElementBuilder from "./util/element_builder.js"


var communities = []

const clear_inputs = () => {
    
}

const render = () => {
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
                            <p>Members: 1</p>
                            <p>New posts: 0</p>
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

const add_community = () => {
    let community_name = document.getElementById("create-community-name").value;
    let community_desc = document.getElementById("create-community-description").value;

    communities.push({
        name: community_name,
        description: community_desc
    });

    render();
}

const setup_event_handlers = () => {
    document.getElementById("create-community-btn").addEventListener("click", add_community);
}

setup_event_handlers();
render();