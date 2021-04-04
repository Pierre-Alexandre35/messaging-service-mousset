function updateCost(input_length, selected_list) {
  $.ajax({
    url : "/get_cost_estimation",
    type : "POST",
    data : JSON.stringify({
              input_length: input_length,
              selected_list: selected_list
            }),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
})
.done(function(data){
    document.getElementById("total-cost-value").innerHTML = data;
});
}

function myFunction(body, max_caracters) {
  var message = body.value;
  var message_length = message.length;
  selected_list = document.querySelector('input[name="list"]:checked').innerHTML;


  if (message_length > max_caracters) {
    document.getElementById("message-cost-alert").style.display = "block";
    updateCost(message_length, selected_list);
  } else {
    document.getElementById("message-cost-alert").style.display = "none";
  }
}
