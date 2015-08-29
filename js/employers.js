/* Wait until the DOM loads by wrapping our code in a callback to $. */
$(function() {
  $('.job-sublist a').click(function(event) {
    event.preventDefault();

    var $job = $(this);
    var $description = $job.parents('.job-sublist').find('.job_description-sublist');

    /* If the category list is shown, hide it. */
     if($description.is(':visible')) {
      $description.slideUp();
      return;
    }
   
    /* Fade out all other category lists. */
    $('.job_description-sublist').not($jobs).slideUp();

    $.ajax({
      type: 'GET',
      url: $job.attr('href'),
      dataType: 'json'
    }).done(function(data) {

      /* This gets called if the Ajax call is successful. */

      /* We expect the JSON data to be in this form:
       *   [
       *     {
       *       "href": <url-of-category>,
       *       "name": <name-of-category>
       *     },
       *     ...
       *   ]
       */

      /* Empty out existing contents in the category list. */
      $description.empty();

      /* Add a list item/link for each category received. */
      var description = data;
      for(var i = 0, n = description.length; i < n; ++i) {
        var job = description[i];
        $description.append(
          $('<a>')
            .addClass('list-group-item no-gutter')
            .attr('href', job.href)
            .append(
              $('<div>')
                .text(job.name)
                .addClass('list-group-item-heading no-gutter')
              )
        );
      }
      /* Slide the newly populated category list into view. */
      $jobs.slideDown();
    }).fail(function() {

      /* This gets called if the Ajax call fails. */

      $jobs.empty().slideUp();

      /* Create an alert box. */
      var $alert = (
        $('<div>')
          .text('Whoops! Something went wrong.')
          .addClass('alert')
          .addClass('alert-danger')
          .addClass('alert-dismissible')
          .attr('role', 'alert')
          .prepend(
            $('<button>')
              .attr('type', 'button')
              .addClass('close')
              .attr('data-dismiss', 'alert')
              .html('&times;')
          )
          .hide()
      );
      /* Add the alert to the alert container. */
      $('#alerts').append($alert);
      /* Slide the alert into view with an animation. */
      $alert.slideDown();
    });
  });
});


$(function() {

  /* Add click event listeners to the restaurant list items. This adds a
   * handler for each element matching the CSS selector
   * .restaurant-list-item. */
  $('.employer-list-item a').click(function(event) {

    /* Prevent the default link navigation behavior. */
    event.preventDefault();

    var $employer = $(this);
    var $jobs = $employer.parents('.employer-list-item').find('.job-sublist');

    /* If the category list is shown, hide it. */
    if($jobs.is(':visible')) {
      $jobs.slideUp();
      return;
    }

    /* Fade out all other category lists. */
    $('.job-sublist').not($jobs).slideUp();

    /* Get the category JSON data via Ajax. */
    $.ajax({
      type: 'GET',
      url: $employer.attr('href'),
      dataType: 'json'
    }).done(function(data) {

      /* This gets called if the Ajax call is successful. */

      /* We expect the JSON data to be in this form:
       *   [
       *     {
       *       "href": <url-of-category>,
       *       "name": <name-of-category>
       *     },
       *     ...
       *   ]
       */

      /* Empty out existing contents in the category list. */
      $jobs.empty();

      /* Add a list item/link for each category received. */
      var jobs = data;
      for(var i = 0, n = jobs.length; i < n; ++i) {
        var job = jobs[i];
        $jobs.append(
          $('<a>')
            .addClass('list-group-item no-gutter')
            .attr('href', job.href)
            .append(
              $('<div>')
                .text(job.name)
                .addClass('list-group-item-heading no-gutter')
            )
        );
      }
      /* Slide the newly populated category list into view. */
      $jobs.slideDown();
    }).fail(function() {

      /* This gets called if the Ajax call fails. */

      $jobs.empty().slideUp();

      /* Create an alert box. */
      var $alert = (
        $('<div>')
          .text('Whoops! Something went wrong.')
          .addClass('alert')
          .addClass('alert-danger')
          .addClass('alert-dismissible')
          .attr('role', 'alert')
          .prepend(
            $('<button>')
              .attr('type', 'button')
              .addClass('close')
              .attr('data-dismiss', 'alert')
              .html('&times;')
          )
          .hide()
      );
      /* Add the alert to the alert container. */
      $('#alerts').append($alert);
      /* Slide the alert into view with an animation. */
      $alert.slideDown();
    });
  });
});
