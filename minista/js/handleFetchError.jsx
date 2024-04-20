const handleFetchError = (error) => {
    if (error.message == "BAD REQUEST") {
        alert("Bad Request");
    } else if (error.status === 400) {
        alert("Bad Request");
    } else {
        console.error(error);
    }
    if(error.message == "CONFLICT"){
        alert("existing username");
        // reset the username inside of inputs in form
        event.target.elements.username.value = '';
    }
    else{
        console.error(error);
    }
};
