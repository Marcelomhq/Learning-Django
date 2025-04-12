function funcaoMenu() {
    var i = document.getElementById("navMenu");

    if(i.className === "nav-menu") {
        i.className += " responsive";
    } else {
        i.className = "nav-menu";
    }
   }


   var a = document.getElementById("loginBtn");
   var b = document.getElementById("registerBtn");
   var x = document.getElementById("login");
   var y = document.getElementById("register");

   function login() {
   var loginForm = document.getElementById("login");
   var registerForm = document.getElementById("register");
   var rememberForm = document.getElementById("remember");

   loginForm.style.left = "4px";
   registerForm.style.left = "-510px";
   rememberForm.style.left = "-510px";

   loginForm.style.opacity = "1";
   registerForm.style.opacity = "0";
   rememberForm.style.opacity = "0";
}

function register() {
   var loginForm = document.getElementById("login");
   var registerForm = document.getElementById("register");
   var rememberForm = document.getElementById("remember");

   loginForm.style.left = "-510px";
   registerForm.style.left = "4px";
   rememberForm.style.left = "-510px";

   loginForm.style.opacity = "0";
   registerForm.style.opacity = "1";
   rememberForm.style.opacity = "0";
}

window.onload = function () {
   const params = new URLSearchParams(window.location.search);
   const form = params.get("form");

   const loginForm = document.getElementById("login");
   const registerForm = document.getElementById("register");
  
   loginForm.style.transition = "none";
   registerForm.style.transition = "none";
   

   if (form === "register") {
       loginForm.style.left = "-510px";
       loginForm.style.opacity = "0";

       registerForm.style.left = "4px";
       registerForm.style.opacity = "1";
   } else if (form === "remember") {
       loginForm.style.left = "-510px";
       loginForm.style.opacity = "0";

   }

};