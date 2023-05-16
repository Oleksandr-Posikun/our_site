console.log(window.location);

const
    HOST = window.location.origin;
    IMG_URL = HOST + '/media';
    URL = 'http://127.0.0.1:8000/ajax',
    URL_MINICART = 'http://127.0.0.1:8000/cart/mini_cart',
    URL_ADDCART = 'http://127.0.0.1:8000/cart/add_cart',
    URL_DELCART = 'http://127.0.0.1:8000/cart/del_cart',
    URL_SORT = 'http://127.0.0.1:8000/shop/sort';

// URL_MINICART = 'http://127.0.0.1:8000/shop/cart',


function createAjaxParams(body) {
    return {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-Request-With": "XMLHttpRequest",
            'X-CSRFToken': getCookie('csrftoken'),
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

function whileInnerHtml(variable, innerText){
    for (let i = 0; i < variable.length; i++) {
				variable[i].innerHTML = innerText;
			}
}

function updateText(classname, text) {
        const getElement = document.getElementsByClassName(classname);
            for (let i = 0; i < getElement.length; i++) {
              getElement[i].innerText = text;
            }
        }

function updateCart(response, sums) {
		const TbodyCartProduct = document.getElementsByClassName('tbody-cart-product');
		const totalSums = document.getElementsByClassName('caption-total-price');
		let htmlInnerCartProduct = '';
		let htmlInnerCartSums = `<ul>
											<li>Subtotal <span>$ ${sums}</span></li>
											<li>Total <span>$ ${sums}</span></li>
							
										</ul>`

		for (let i = 0; i < TbodyCartProduct.length; i++) {
				for (let k = 0; k < response.length; k++) {
					htmlInnerCartProduct +=
						`<tr id="parent" class="row-0">
							<td class="row-close close-1" data-title="product-remove"><a href="#"><i class="ion-close-circled"></i></a></td>
							<td class="row-img"><img src="${IMG_URL}/${response[k]['image']}" alt="cart-img"></td>
							<td class="product-name" data-title="Product"><a href="#">${response[k]['name']}</a></td>
							<td class="product-price" data-title="Price"><p>$ ${response[k]['price']}</p></td>
							<td class="product-quantity" data-title="Quantity">
								<div class="quantity_filter">
									<input type="button" value="-" class="minus">
									<input class="quantity-number qty" type="text" value="${response[k]['count']}" min="1" max="10">
									<input type="button" value="+" class="plus">
								</div>
							</td>
							<td class="product-total" data-title="Subprice"><p>$ ${response[k]['sums_product']}</p></td>
							<td class="item-cart row-close close-2" data-id= "${response[k]['id']}"><button class="close-icon align-items-center btn-del-product"><i class="ion-close btn-del-product"></i></button></td>
						</tr>`;
				}
				TbodyCartProduct[i].innerHTML = htmlInnerCartProduct;
			}

			whileInnerHtml(totalSums, htmlInnerCartSums)
	}


function updateMiniCart(response, sums, count_product) {
    const cartMiniLogo = document.getElementsByClassName('cart-mini-box-logo');
    let htmlInnerCartLogoSums = `
            <div class="cart-icon">
                <img src="/static/image/cart-icon.png" alt="cart-icon">
                <span>${count_product}</span>
            </div>
            $ ${sums}<i class="fa fa-angle-down"></i>
            `

    const PriceProdect = document.getElementsByClassName('price-prodect d-flex align-items-center justify-content-between');
    let htmlInnerCartTotal = `<p class="total">total</p>
                             <p class="total-price">$ ${sums}</p>;
                            `

    const cartInfo = document.getElementsByClassName('cart-info');
    let htmlInnerCartProduct = '';

    whileInnerHtml(cartMiniLogo, htmlInnerCartLogoSums)

    for (let i = 0; i < cartInfo.length; i++) {
        for (let k = 0; k < response.length; k++) {
            htmlInnerCartProduct +=
                `<div class="cart-prodect d-flex item-cart" data-id="${response[k]['id']}">
                    <div class="cart-img">
                        <img src="${IMG_URL}/${response[k]['image']}" alt="cart-img">
                    </div>
                    <div class="cart-product">
                        <a href="#"> ${response[k]['name']}</a>
                        <p>$ ${response[k]['price']}</p>
                        <p>Count x ${response[k]['count']}</p>
                    </div>
                    <button class="close-icon d-flex align-items-center btn-del-product"><i class="ion-close btn-del-product"></i></button>
                </div>`;
        }
        cartInfo[i].innerHTML = htmlInnerCartProduct;
    }

    whileInnerHtml(PriceProdect, htmlInnerCartTotal)
}