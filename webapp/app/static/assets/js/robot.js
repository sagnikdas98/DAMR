$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-robot-move .modal-content").html("");
          $("#modal-robot-move").modal("show");
        },
        success: function (data) {
          $("#modal-robot-move .modal-content").html(data.popup);
          }
      });
    };
    
    /* Binding */
    
    $(".js-robot-move").click(loadForm);
});
