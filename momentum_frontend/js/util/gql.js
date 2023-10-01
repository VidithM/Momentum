const ARIADNE_PORT = 8020;
const ARIADNE_URL = `http://localhost:${ARIADNE_PORT}`;

export const login_user = async (username, password) => {

}

export const get_user_with_rid = async (rid) => {
    let query_body = `
        query ($rids: [Int!]) {
            search_users(
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
                }
            }
        }
    `
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // update this to have usernames
        body: JSON.stringify({"query": query_body, "variables": {"rids": [rid]}}),
    };

    let res = await fetch(ARIADNE_URL, requestOptions);
    let json = await res.json();
    console.log(json);
}

export const create_user = (user_data) => {

}