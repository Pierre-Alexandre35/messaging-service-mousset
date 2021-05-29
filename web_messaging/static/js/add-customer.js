console.log('adding customer')

const form = document.querySelector('.customer-form');
var phoneInput = document.querySelector('#phone-input')
var firstNameInput = document.querySelector('#first-name-input')
var LastNameInput = document.querySelector('#last-name-input')


const debounce = (fn, delay = 500) => {
    let timeoutId;
    return (...args) => {
        // cancel the previous timer
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        // setup a new timer
        timeoutId = setTimeout(() => {
            fn.apply(null, args)
        }, delay);
    };
};

form.addEventListener('input', debounce(function (e) {
    switch (e.target.id) {
        case 'phone-input':
            isPhoneValid(phoneInput.value);
            break;
        case 'first-name-input':
            break;
        case 'last-name-input':
            break;
    }
}));


const isNameValid = () => {

}

const isPhoneValid = (phone) => {
    var isValid = /^([0-9]{10})$/.test(phone);
    var startsWithValidFrenchNumber = phone.startsWith("06") || phone.startsWith("07");
    console.log(isValid && startsWithValidFrenchNumber)
};
