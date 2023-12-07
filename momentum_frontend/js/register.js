import * as gql from "./util/gql.js"

const redirect = (page) => {
    let curr_url = window.location.href;
    let toks = curr_url.split('/');
    toks[toks.length - 1] = `${page}.html`;
    let new_url = toks.join("/");
    window.location.href = new_url;
}

const register = async () => {
    let email = document.getElementById("email-input").value;
    let username = document.getElementById("username-input").value;
    let name = document.getElementById("name-input").value;
    let password = document.getElementById("password-input").value;
    let confirm_password = document.getElementById("password-confirm-input").value;
    if(password !== confirm_password){
        alert('Confirmation password does not match!');
        return;
    }
    let rid = Date.now() % 1e9;
    console.log(rid);
    let res = await gql.register_user(rid, email, username, name, password);
    if(res == null){
        alert('Email is already in use!');
        return;
    }
    localStorage.setItem("uid", res.rid);
    redirect("profile");
}

const clear_inputs = () => {
    document.getElementById("email-input").value = "";
    document.getElementById("username-input").value = "";
    document.getElementById("name-input").value = "";
    document.getElementById("password-input").value = "";
    document.getElementById("password-confirm-input").value = "";
}

const setup_event_handlers = () => {
    document.getElementById("register-btn").addEventListener("click", register);
}

clear_inputs();
setup_event_handlers();