var SOFTY = SOFTY || {};

/**
 * Assigns CSRF token as required by the server
 *
 * @property SOFTY.csrf_token
 */
SOFTY.csrf_token = "{{ csrf_token }}";

/**
 * SOFTY.cart is used to hold all things related to cart.
 *
 * @class SOFTY.cart
 * @static
 */
SOFTY.cart = SOFTY.cart || {
    'add_url': '{% url "shop_cartitem_create" %}',
    'short_summary_url': '{% url "shop_cart_short_summary" %}',
    'link_element': $("a.cart_link")
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
    }

    $.ajax({
        type: 'POST',
        url: SOFTY.cart.add_url,
        data: query,
        async: false,
        success: function(data) {
            SOFTY.cart.display();
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
            SOFTY.cart.display_element.text(data);
        }
    });
};
