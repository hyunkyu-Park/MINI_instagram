import React, {useState} from 'react';

export default function CreatePage() {

    const handleSubmit = (event) => {
        event.preventDefault();
        
        // Create FormData object using Form data
        const formData = new FormData(event.target);
        
        // Sending data to server
        fetch(`/api/v1/accounts/create/`, {
            method: "POST",
            credentials: "same-origin",
            body: formData,
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            // Reload/Refrash the page when it is updated
            console.log("success!")
            window.location.replace('/');
        })
        .catch((error) => {
            console.log(error);
            alert("existing username")

            // reset the username inside of inputs in form
            event.target.elements.username.value = '';
        });
    };

    return (
        <>
            <form onSubmit={handleSubmit} method="post" encType="multipart/form-data">
                <p>Photo</p>
                <input type="file" name="file" required />
                <p>Name</p>
                <input type="text" name="fullname" placeholder="Full Name" required />
                <p>Username</p>
                <input type="text" name="username" placeholder="Username" required />
                <p>Email</p>
                <input type="text" name="email" placeholder="Email" required />
                <p>Password</p>
                <input type="password" name="password" placeholder="Password" required />
                <input type="submit" name="signup" value="Sign Up" />
                <input type="hidden" name="operation" value="create" />
            </form>

            <p>Already have an account? <a href="/accounts/login/">Login</a></p>
        </>
    );
}