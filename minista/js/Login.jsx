import React from 'react';
import { Link } from "react-router-dom";

export default function LoginPage() {

    const handleSubmit = (event) => {
        event.preventDefault();
        
        // Create FormData object using Form data
        const formData = new FormData(event.target);
        
        // Sending data to server
        fetch(`/api/v1/accounts/login/`, {
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
                alert("Wrong id or password")

                // reset the values inside of inputs in form
                event.target.reset();
            });
    };

    return (
        <>
            <a href="/accounts/login/" className="custom-p">Login</a>
            <form onSubmit={handleSubmit} method="post" encType="multipart/form-data">
                <input className="custom-p" type="text" name="username" placeholder="Username" maxlength="20" required />
                <input className="custom-p" type="password" name="password" placeholder="Password" maxlength="20" required />
                <input className="custom-p" type="submit" value="Login" />
                <input type="hidden" name="operation" value="login" />
            </form>
            <p className="custom-p">Don't have an account??</p>
            <Link className="custom-p" to={`/accounts/create/`}>Sign up</Link>
        </>
    );
}