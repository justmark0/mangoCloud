var LOGIN_OPERATION = false;
var REGISTR_OPERATION = false;
var USER_LOGIN = 'StiveMan1';
var USER_PASSWORD = 'StiveMan1';
var USER_TOKEN = '96b011a7a4fe24b67bbd4d258ce028d08f5b6ea4903fe7127bcf8e38f1699857';

function show_login_pop_up(){
    LOGIN_OPERATION = true;
    REGISTR_OPERATION = false;
    $(".login_button").text("Login");
    $(".login_title").text("Login");
    $(".change_sing_up_in").text("Register new account");
    $(".filter").css('display','block');
    $(".popup").css('display','block');
}
function show_register_pop_up(){
    LOGIN_OPERATION = false;
    REGISTR_OPERATION = true;
    $(".login_button").text("Register");
    $(".login_title").text("Register");
    $(".change_sing_up_in").text("You all ready have account");
    $(".filter").css('display','block');
    $(".popup").css('display','block');
}
function close_pop_up(){
    LOGIN_OPERATION = false;
    REGISTR_OPERATION = false;
    $(".filter").css('display','none');
    $(".popup").css('display','none');
    
    print(USER_TOKEN);
}

async function registertion(login, password){
    var error = false;
    var data = await $.ajax({

        type : "POST",
        mode    : "no-cors",
        url    : "/api/reg",
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
    if(!error){
        close_pop_up();
    }
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
    if(!error){
        close_pop_up();
    }
}
// registertion('sdijsoijd','sdhisjhdihsi');
// show_register_pop_up();

$(".login_button").click(function() {
    var login = $(".login_input#username").val();
    var password = $(".login_input#password").val();
    if(REGISTR_OPERATION){
        if(login != null && password != null && login.length > 8 && password.length > 8){
            registertion(login,password);
        }else{
            $(".login_errors").text('Your username and password are not secure enough');
            $(".login_input#username").text('');
            $(".login_input#password").text('');
        }
    }
    if(LOGIN_OPERATION){
        authorization(login,password);
    }
});
$(".change_sing_up_in").click(function(){
    if(LOGIN_OPERATION){
        show_register_pop_up();
    }else{
        show_login_pop_up();
    }
})
