var SOFTY = SOFTY || {};

/**
 * Assigns CSRF token as required by the server
 *
 * @property SOFTY.csrf_token
 */
SOFTY.csrf_token = "";

/**
 * SOFTY.cart is used to hold all things related to cart.
 *
 * @class SOFTY.cart
 * @static
 */
SOFTY.cart = SOFTY.cart || {
    'add_url': "",
    'short_summary_url': "",
    'cart_summary_element': $(".cart_sidebar"),
    'cart_items_count': $(".cart_items_count")
};

/**
 * Method to add items to the cart using ajax.
 *
 * @method add
 * @static
 *
 * @param content_type_id
 * @param object_id
 * @param quantity
 */
SOFTY.cart.Add = function(ctid, oid, qty) {
    query = {
        content_type_id: ctid,
        object_id: oid,
        quantity: qty,
        csrfmiddlewaretoken: SOFTY.csrf_token
    };

    $.ajax({
        type: 'POST',
        url: SOFTY.cart.add_url,
        data: query,
        async: false,
        success: function(data) {
            SOFTY.cart.display();
            SOFTY.cart.alert('Item added to the cart.');
        }
    });
};

/**
 * Fetch cart information and display in display_element
 *
 * @method display
 */
SOFTY.cart.display = function() {
    $.ajax({
        type: 'GET',
        url: SOFTY.cart.short_summary_url,
        async: false,
        success: function(data) {
            SOFTY.cart.cart_summary_element.html(data);
        }
    });

    $.getJSON(SOFTY.cart.short_summary_url+"?json", {}, function(data) {
        SOFTY.cart.cart_items_count.text(data.items);
    });
};

/**
 * Display alert message
 *
 * @method alert
 */
SOFTY.cart.alert = function(msg) {
    var msg_div = $("<div></div>").css({
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'padding': '2px',
        'width': '100%',
        'font-weight': 'bold',
        'text-align': 'center',
        'background-color': '#fcb905'
    });

    msg_div.text(msg).fadeIn(300);
    $("body").prepend(msg_div);
    msg_div.delay(1000).fadeOut(200);
};
