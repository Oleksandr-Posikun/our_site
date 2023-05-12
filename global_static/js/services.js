const
    URL = 'http://127.0.0.1:8000/ajax',
    URL_MINICART = 'http://127.0.0.1:8000/cart/',
    URL_SORT = 'http://127.0.0.1:8000/shop/sort',
    URL_ADDCART = 'http://127.0.0.1:8000/cart/add_cart',
    URL_DELCART = 'http://127.0.0.1:8000/cart/del_cart';

// URL_MINICART = 'http://127.0.0.1:8000/shop/cart',


function createAjaxParams(body) {
    return {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-Request-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie('csrftoken'),
        },
        body: JSON.stringify(body)
	};
}

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}