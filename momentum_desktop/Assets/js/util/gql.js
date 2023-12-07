const ARIADNE_PORT = 8010;
const ARIADNE_URL = `http://localhost:${ARIADNE_PORT}`;

const run_gql = async (query_body, variables) => {
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"query": query_body, "variables": variables}),
    };

    let res = await fetch(ARIADNE_URL, requestOptions);
    let json = await res.json();
    console.log(json);
    return json;
}

const get_user_with_email = async (email) => {
    let query_body = `
        query ($emails: [EmailAddress!]) {
            search_users (
                terms: {
                    emails: $emails
                }
            )
            {
                error {
                    description
                }
                users {
                    rid
                    password
                }
            }
        }
    `
    let res = await run_gql(query_body, {"emails" : [email]});
    return res;
}

export const login_user = async (email, password) => {
    let user_raw = await get_user_with_email(email);
    let user = user_raw.data.search_users.users;
    if(user == null){
        return null;
    }
    user = user[0];
    if(user.password === password){
        return user.rid;
    }
    return null;
}

export const register_user = async (rid, email, username, name, password) => {
    let user_raw = await get_user_with_email(email);
    let user = user_raw.data.search_users.users;

    if(user != null){
        // user with this email already exists
        return null;
    }
    let query_body = `
        mutation ($rid: Int!, $name: String!, $username: String!, $password: String!, $email: EmailAddress!) {
            create_user (
                input : {
                    rid: $rid,
                    name: $name,
                    username: $username,
                    password: $password,
                    email: $email
                }
            )
            {
                error {
                    description
                }
                user {
                    rid
                }
            }
        }
    `
    let res = await run_gql(query_body, {"rid": rid, "name": name, "username": username, "password": password, "email": email});
    return res.data.create_user.user;
}

export const get_user_with_rid = async (rid) => {
    let query_body = `
        query ($rids: [Int!]) {
            search_users (
                terms: {
                    rids: $rids
                }
            )
            {
                error {
                    description
                }
                users {
                    rid
                    username
                    name
                    posts {
                        rid
                        content
                        timestamp
                        community {
                            rid
                            description
                        }
                        comments {
                            rid
                        }
                    }
                    communities {
                        rid
                        description
                        users {
                            rid
                        }
                        posts {
                            rid
                        }
                    }
                }
            }
        }
    `
    let res = await run_gql(query_body, {"rids" : [rid]});
    let user = res.data.search_users.users;
    if(user == null){
        return null;
    }
    return user[0];
}

export const add_user_to_community = async (user_rid, existing, community_rid) => {
    let query_body = `
        mutation ($user_rid: Int!, $new_communities: [String!]) {
            update_user (
                input: {
                    rid: $user_rid,
                    communities: $new_communities
                }
            )
            {
                error {
                    description
                }
                user {
                    rid
                    username
                    communities {
                        rid
                    }
                }
            }
        }
    `
    let existing_rids = []
    for(let i = 0; i < existing.length; i++){
        existing_rids.push(existing[i].rid);
    }
    existing_rids.push(community_rid);
    await run_gql(query_body, {"user_rid" : user_rid, "new_communities" : existing_rids});
}

export const get_community_with_rid = async (rid) => {
    let query_body = `
        query ($rids: [String!]) {
            search_communities (
                terms: {
                    rids: $rids
                }
            )
            {
                error {
                    description
                }
                communities {
                    rid
                    description
                    posts {
                        rid
                        user {
                            rid
                            username
                            name
                        }
                        content
                        timestamp
                        comments {
                            rid
                        }
                    }
                    users {
                        rid
                    }
                }
            }
        }
    `
    let res = await run_gql(query_body, {"rids" : [rid.toString()]});
    let communities = res.data.search_communities.communities;
    if(communities == null){
        return null;
    }
    return communities[0];
}

export const create_community = async (name, description, owner_rid, owner_existing_communities) => {
    let query_body = `
        mutation ($description: String!) {
            create_community (
                input: {
                    description: $description
                }
            )
            {
                error {
                    description
                }
                community {
                    rid
                }
            }
        }
    `
    let res = await run_gql(query_body, {"description" : name.concat("%").concat(description)});
    await add_user_to_community(owner_rid, owner_existing_communities, res.data.create_community.community.rid);
    console.log(res);
}

export const create_post = async (user_rid, content, timestamp, community) => {
    let query_body = `
        mutation ($user: Int!, $content: String!, $timestamp: Datetime!, $community: String!) {
            create_post (
                input: {
                    user: $user,
                    content: $content,
                    timestamp: $timestamp,
                    community: $community
                }
            )
            {
                error {
                    description
                }
            }
        }
    `
    await run_gql(query_body, {"user": user_rid, "content": content, "timestamp": timestamp, "community": community.toString()});
}

export const get_post_with_rid = async (post_rid) => {
    let query_body = `
        query ($rid: [Int!]) {
            search_posts (
                terms: {
                    rids: $rid,
                }
            )
            {
                posts {
                    rid
                    comments {
                        rid
                    }
                }
                error {
                    description
                }
            }
        }
    `
    let res = await run_gql(query_body, {"rid": [post_rid]});
    if(res.data.search_posts.posts == null){
        return null;
    }
    return res.data.search_posts.posts[0];
}

export const get_comment_with_rid = async (comment_rid) => {
    let query_body = `
        query ($rids: [Int!]) {
            search_comments (
                terms: {
                    rids: $rids
                }
            )
            {
                comments {
                    rid
                    content
                    user {
                        rid
                        username
                        name
                    }
                    timestamp
                }
                error {
                    description
                }
            }
        }
    `
    let res = await run_gql(query_body, {"rids": comment_rid});
    console.log(res);
    return res.data.search_comments.comments;
}

export const add_comment_to_post = async (user_rid, content, timestamp, post_rid) => {
    let query_body = `
        mutation ($user: Int!, $content: String!, $timestamp: Datetime!, $post: Int!) {
            create_comment (
                input: {
                    user: $user,
                    content: $content,
                    timestamp: $timestamp,
                    post: $post
                }
            )
            {
                error {
                    description
                }
            }
        }
    `
    await run_gql(query_body, {"user": user_rid, "content": content, "timestamp": timestamp, "post": post_rid});
}