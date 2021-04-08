var inputMessageLength = 0;
var currentSegment = 1;
var SelectedCustomerList;

// on load of the page 
$(document).ready(function () {
  updateList(getSelectedCustomersList());
  updateCost();
});

// call the get_cost_estimation to update the price 
function updateCost() {
  $.ajax({
    url: "/get_cost_estimation",
    type: "POST",
    data: JSON.stringify({
      input_length: inputMessageLength,
      selected_list: SelectedCustomerList,
    }),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
  }).done(function (data) {
    var newCost = data['estimated_cost'] + ' ' + data['currency'];
    document.getElementById("total-cost-value").innerHTML = newCost
  });
}

function updateList(NewSelectedCustomerList) {
  SelectedCustomerList = NewSelectedCustomerList;
  updateCost();
}

function getSelectedCustomersList() {
  return $("input[name=list]:checked").val();
}

function updateSegmentNumber(newSegmentNumber){
  currentSegment = newSegmentNumber;
}

// caled everytime the user make a change in the message input area 
function updateMessage(body, SegmentCharactersLimit) {
  var messageContent = body.value;
  inputMessageLength = messageContent.length;
  updateSegmentMessage(inputMessageLength, SegmentCharactersLimit);
  
  var newSegment = Math.ceil(inputMessageLength / SegmentCharactersLimit)
  if(newSegment != currentSegment){
    updateSegmentNumber(newSegment);
    updateCost();
  }
}

// alert message displayed to tell the client that he already reached the limit of segment 1
function updateSegmentMessage(inputMessageLength, SegmentCharactersLimit) {
  if (inputMessageLength > SegmentCharactersLimit) {
    document.getElementById("message-cost-alert").style.display = "block";
  } else {
    document.getElementById("message-cost-alert").style.display = "none";
  }
}
