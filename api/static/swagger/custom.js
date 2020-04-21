

function auth() {
    var token = document.getElementsByClassName('auth-container')[0].getElementsByTagName('input')[0].value
    localStorage.setItem('token', token)
}


function auth_modal() {
    setTimeout(function() {
        document.querySelector('.auth.button').onclick = auth
    }, 500)
}


function init() {
    if (localStorage.getItem('token'))
        ui.preauthorizeApiKey('apiKey', localStorage.getItem('token'))
    document.querySelector('.authorize.btn').onclick = auth_modal
}


setTimeout(init, 1000)
