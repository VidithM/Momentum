import * as gql from "./util/gql.js"

const redirect = (page) => {
    let curr_url = window.location.href;
    let toks = curr_url.split('/');
    toks[toks.length - 1] = `${page}.html`;
    let new_url = toks.join("/");
    window.location.href = new_url;
}

const login = async () => {
    let email = document.getElementById("email-input").value;
    let password = document.getElementById("password-input").value;

    let rid = await gql.login_user(email, password);
    if(rid == null){
        alert("User does not exist or incorrect password!");
        return;
    }
    localStorage.setItem("uid", rid);
    redirect("profile");
}

const clear_inputs = () => {
    document.getElementById("email-input").value = "";
    document.getElementById("password-input").value = "";
}

const setup_event_handlers = () => {
    document.getElementById("login-btn").addEventListener("click", login);
}

clear_inputs();
setup_event_handlers();