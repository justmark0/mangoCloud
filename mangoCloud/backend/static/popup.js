var LOGIN_OPERATION = false;
var USER_LOGIN = 'StiveMan1';
var USER_PASSWORD = 'StiveMan1';
var USER_TOKEN = 'a433f9ca09e0e913dca2d68b5043b324a3caf229afd969c41829f8407d61f894';

function show_login_pop_up(){
    LOGIN_OPERATION = true;
    $(".login_button").text("Login");
    $(".login_title").text("Login");
    $(".filter").css('display','block');
    $(".popup").css('display','block');
    $(".login_input#username").val("");
    $(".login_input#password").val("");
}
function close_pop_up(){
    LOGIN_OPERATION = false;
    $(".filter").css('display','none');
    $(".popup").css('display','none');
}

async function authorization(login, password){
    var error = false;
    var data = await $.ajax({

        type : "POST",
        mode    : "no-cors",
        url    : "/api/get_token",
        dataType: "json",
        headers : {"Access-Control-Allow-Origin" : "*"},
        contentType: "application/json; charset=utf-8",
        data   : JSON.stringify({"username":login,"password":password}),
        success: function(data){
            return data;
        },

        error: function(error_data){
            $(".login_errors").text("Error with connection");
            error = true;
        }
    });
    if('Error' in data){
        $(".login_errors").text('This user already exist');
        error = true;
    }
    USER_TOKEN = data['token'];
    USER_LOGIN = login;
    USER_PASSWORD = password;
    save_cookie();
    if(!error){
        $(".Login_name").text(USER_LOGIN);
        close_pop_up();
    }
}


$(".login_button").click(function() {
    var login = $(".login_input#username").val();
    var password = $(".login_input#password").val();
    if(LOGIN_OPERATION){
        authorization(login,password);
    }
});

function save_cookie(){
    document.cookie = 'user=' +encodeURIComponent(USER_TOKEN)+";";
    document.cookie =  'login=' + encodeURIComponent(USER_LOGIN)+";";
    // print(USER_LOGIN)
    // print(document.cookie)
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function get_cookie(){
    USER_TOKEN = getCookie('user');
    USER_LOGIN = getCookie('login');
    if(USER_TOKEN != ''){
        $(".Login_name").text(USER_LOGIN);
        close_pop_up();
    }else{
        show_login_pop_up();
    }
}