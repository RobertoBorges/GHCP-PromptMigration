define(['moment', 'spinjs'], function (moment, spinner) {
    var formatDate = function (date) {  
        var result = moment(date);
        return result;
    };
    
    //Add spinner configuration
    var opts = {
        lines: 11, // The number of lines to draw
        length: 0, // The length of each line
        width: 20, // The line thickness
        radius: 20, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        rotate: 0, // The rotation offset
        color: '#000', // #rgb or #rrggbb
        speed: 2, // Rounds per second
        trail: 40, // Afterglow percentage
        shadow: false, // Whether to render a shadow
        hwaccel: false, // Whether to use hardware acceleration
        className: 'spinner', // The CSS class to assign to the spinner
        zIndex: 2e9, // The z-index (defaults to 2000000000)
        top: 25, // Top position relative to parent in px
        left: 25 // Left position relative to parent in px
    };
    var target = document.getElementById('spinjs');
    var spinjs = new spinner(opts);

    function showSpinner() {
        spinjs.spin(target);
    }

    function stopSpinner() {
        spinjs.stop();
    }

    var utils = {        
      formatDate: formatDate,
      makeAjaxCall: function (url, data) {
            return $.ajax({
                url: url,
                type: 'POST',
                dataType: 'json',
                data: data
            });
      },
      spinner: {
          show: showSpinner,
          hide: stopSpinner
      }
    };

    return utils;
});