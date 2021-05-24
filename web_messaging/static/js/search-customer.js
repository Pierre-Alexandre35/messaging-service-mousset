
// Call the find_customers_records in the mongodb
function retrieveUserRecords(selectedList, selectedField, inputValue) {
    $.ajax({
      url: "/search",
      type: "POST",
      data: JSON.stringify({
        selected_customer_list: selectedList,
        field: selectedField,
        input_text: inputValue
      }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
    }).done(function (data) {
      console.log(123456)
    });
  }

function searchUser(inputText, selectedCustomerList) {
    var selectedField = document.getElementById("user-search-field").value;
    inputValue = inputText.value
    retrieveUserRecords(selectedCustomerList, selectedField, inputValue)
}





