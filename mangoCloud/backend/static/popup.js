var LOGIN_OPERATION = false;
var USER_LOGIN = 'StiveMan1';
var USER_PASSWORD = 'StiveMan1';
var USER_TOKEN = '0b7e165d46a07d22ac08b8154519ca3c5c85900870ece28b5dd1b9ad8ce375f5';

function show_login_pop_up(){
    LOGIN_OPERATION = true;
    $(".login_button").text("Login");
    $(".login_title").text("Login");
    $(".filter").css('display','block');
    $(".popup").css('display','block');
}
function close_pop_up(){
    LOGIN_OPERATION = false;
    $(".filter").css('display','none');
    $(".popup").css('display','none');
    
    print(USER_TOKEN);
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
// show_login_pop_up();

$(".login_button").click(function() {
    var login = $(".login_input#username").val();
    var password = $(".login_input#password").val();
    if(LOGIN_OPERATION){
        authorization(login,password);
    }
});
