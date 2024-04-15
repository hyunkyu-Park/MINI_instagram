const handleFetchError = (error) => {
    if (error.status === 404) {
        alert("Page Not Found");
    } else if (error.status === 400) {
        alert("Bad Request");
    } else {
        console.error(error);
    }
};