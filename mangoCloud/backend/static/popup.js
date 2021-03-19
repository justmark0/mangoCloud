var string_login = '';
var string_registr = '';
var login = false;
var registr = false;

function show_Login_pop_up(){
    login = true;
    $(".login_button").text("Login");
    $(".login_title").text("Login");
    $(".filter").css('display','block');
    $(".popup").css('display','block');
}
function show_register_pop_up(){
    login = true;
    registr = true;
    $(".login_title").text("Register");
    $(".login_button").text("Register");
    $(".filter").css('display','block');
    $(".popup").css('display','block');
}
// print( JSON.stringify({"username":"makr7","password":"1234"}))
data = {"token": "fcf0646ddf586305e28651799a5b3d15becee3ef73e478812fe8ea6f447c52c8", "file_id": "72c76d1721fedd3bfc26b2ce3bf28be26c5dc6585a9919d2f1ae04fbd4170fb6"};
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Referrer-Policy", "same-origin");
// $.ajax({
//     type: "POST",
//     url: "http://58bd2bb77759.ngrok.io/api/reg",
//     headers: myHeaders,
//     data: JSON.stringify(data),
//     processData: false,
//     dataType: "json",
//     success: function (msg) {
//         print(msg);
//     },
// });
$.ajax({

    type : "POST",
    mode    : "no-cors",
    url    : "http://127.0.0.1:8000/api/reg",
    dataType: "json",
    headers : {"Access-Control-Allow-Origin" : "*"},
    contentType: "application/json; charset=utf-8",
    data   : JSON.stringify({"username":"makr100skdjksdnk000","password":"1234"}),
    success: function(data){
        print(data);
    },

    error: function(error_data){
        console.log("error")
        console.log(error_data);
    }
});
// show_Login_pop_up();
// show_Login_pop_up();
// $('.login_button').click(function() {
//     if(active != null){
//     }
//     Activate(this);
// })
