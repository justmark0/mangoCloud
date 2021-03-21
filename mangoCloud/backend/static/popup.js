var LOGIN_OPERATION = false;
var ADD_ACCESS = false;
var FILE_ID_OPERATION = '';
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
function show_access_pop_up(file_id){
    ADD_ACCESS = true;
    FILE_ID_OPERATION = file_id;
    $(".login_button").text("Add");
    $("#filter").click(()=>close_pop_up_access());
    $(".login_title").text("Add Access");
    $(".filter").css('display','block');
    $(".popup_ac").css('display','block');
    $(".login_input#username_ac").val("");
    $(".filter").click(()=>close_pop_up_access());
}
function close_pop_up_access(){
    print('lol')
    ADD_ACCESS = false;
    FILE_ID_OPERATION = '';
    $(".popup_ac").css('display','none');
    $(".access_link").css('display','none');
    $(".filter").css('display','none');

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
        Activate($('.nav_button#Main'));
    }
}


$(".login_button").click(function() {
    var login = $(".login_input#username").val();
    var password = $(".login_input#password").val();
    if(LOGIN_OPERATION){
        authorization(login,password);
    }else{
        give_accsess(FILE_ID_OPERATION,$(".login_input#username_ac").val())
        // close_pop_up_access();
    }
});

function save_cookie(){
    document.cookie = 'token=' +encodeURIComponent(USER_TOKEN)+";";
    document.cookie =  'login=' + encodeURIComponent(USER_LOGIN)+";";
    document.cookie =  'password=' + encodeURIComponent(USER_PASSWORD)+";";
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
    USER_TOKEN = getCookie('token');
    USER_LOGIN = getCookie('login');
    USER_PASSWORD = getCookie('password');
    if(USER_TOKEN != ''){
        authorization(USER_LOGIN, USER_PASSWORD);
    }else{
        show_login_pop_up();
    }
}