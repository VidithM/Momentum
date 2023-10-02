const ARIADNE_PORT = 8020;
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

export const register_user = async (email, username, name, password) => {
    let user_raw = await get_user_with_email(email);
    let user = user_raw.data.search_users.users;

    if(user != null){
        // user with this email already exists
        return null;
    }
    let query_body = `
        mutation ($name: String!, $username: String!, $password: String!, $email: EmailAddress!) {
            create_user (
                input : {
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
    let res = await run_gql(query_body, {"name" : name, "username": username, "password": password, "email": email});
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
                    communities {
                        rid
                        description
                        users {
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

export const create_community = async (description, owner_rid) => {
    let query_body = `
        mutation ($description: String!, $owner_rid: [Int!]!) {
            create_community (
                input: {
                    description: $description,
                    users: $owner_rid
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
    let res = await run_gql(query_body, {"description" : description, "owner_rid" : [owner_rid]});
    console.log(res);
}