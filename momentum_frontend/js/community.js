import * as ElementBuilder from "./util/element_builder.js"
import * as gql from "./util/gql.js"

const logout = () => {
    localStorage.clear();
    redirect("landing");
}

const render = async () => {
    let uid = parseInt(localStorage.getItem("uid"));
    let user = await gql.get_user_with_rid(uid);

    document.getElementById("username-disp").innerHTML = user.username + " | ";
    console.log(user);
}

const setup_event_handlers = () => {
    document.getElementById("logout-link").addEventListener("click", logout);
}

setup_event_handlers();
render();