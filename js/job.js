$(function() {

  /* We're going to use these elements a lot, so let's save references to them
   * here. All of these elements are already created by the HTML code produced
   * by the items page. */
  var $orderPanel = $('#order-panel');
  var $orderPanelCloseButton = $('#order-panel-close-button');
  var $itemName = $('#item-name');
  var $itemDescription = $('#item-description');
  var $itemQuantity = $('#item-quantity-input');
  var $itemId = $('#item-id-input');

  /* A function to show an alert box at the top of the page. */
  var showAlert = function(message, type) {

    /* This stuctured mess of code creates a Bootstrap-style alert box.
     * Note the use of chainable jQuery methods. */
    var $alert = (
      $('<div>')                // create a <div> element
        .text(message)          // set its text
        .addClass('alert')      // add some CSS classes and attributes
        .addClass('alert-' + type)
        .addClass('alert-dismissible')
        .attr('role', 'alert')
        .prepend(               // prepend a close button to the inner HTML
          $('<button>')         // create a <button> element
            .attr('type', 'button') // and so on...
            .addClass('close')
            .attr('data-dismiss', 'alert')
            .html('&times;')    // &times; is code for the x-symbol
        )
        .hide()  // initially hide the alert so it will slide into view
    );

    /* Add the alert to the alert container. */
    $('#alerts').append($alert);

    /* Slide the alert into view with an animation. */
    $alert.slideDown();
  };

  /* Whenever an element with class `item-link` is clicked, copy over the item
   * information to the side panel, then show the side panel. */
  $('.item-link').click(function(event) {
    // Prevent default link navigation
    event.preventDefault();

    /* No input validation... yet. */

    /* Send the data to `PUT /orders/:orderid/items/:itemid`. */
    $.ajax({
      /* The HTTP method. */
      type: 'POST',
      /* The URL. Use a dummy order ID for now. */
      url: "http://tedcogan.com/employers/3/jobs/6",
      /* The `Content-Type` header. This tells the server what format the body
       * of our request is in. This sets the header as
       * `Content-Type: application/json`. */
      contentType: 'application/json',
      /* The request body. `JSON.stringify` formats it as JSON. */
      /* The `Accept` header. This tells the server that we want to receive
       * JSON. This sets the header as something like
       * `Accept: application/json`. */
      dataType: 'json'
    }).done(function() {

      /* This is called if and when the server responds with a 2XX (success)
       * status code. */

      /* Show a success message. */
      showAlert('Posted the order!', 'success');

      /* Close the side panel while we're at it. */
      togglePanel(false);
    }).fail(function() {
      showAlert('Something went wrong.', 'danger');
    });
  });
});
