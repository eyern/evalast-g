const searchButton = document.getElementById('search-button'),
      searchClose = document.getElementById('search-close'),
      searchContent = document.getElementById('search-content');

if(searchButton){
    searchButton.addEventListener('click', () => {
        searchContent.classList.add('show-search'); // ဒီနေရာမှာ classList လို့ ပြင်ပါ
    })
}

if(searchClose){
    searchClose.addEventListener('click', () => {
        searchContent.classList.remove('show-search'); // ဒီနေရာမှာလည်း classList လို့ ပြင်ပါ
    })
}


const loginButton = document.getElementById('login-button'),
      loginClose = document.getElementById('login-close'),
      loginContent = document.getElementById('login-content');

if(loginButton){
    loginButton.addEventListener('click', () => {
        loginContent.classList.add('show-login'); // ဒီနေရာမှာ classList လို့ ပြင်ပါ
    })
}

if(loginClose){
    loginClose.addEventListener('click', () => {
        loginContent.classList.remove('show-login'); // ဒီနေရာမှာလည်း classList လို့ ပြင်ပါ
    })
}



