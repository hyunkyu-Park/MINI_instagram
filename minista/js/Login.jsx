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
                if(error.message == "FORBIDDEN"){
                    alert("Please check ID or Password");
                }
                else{
                    alert(error);
                }
            });
    };

    return (
        <>
            <a href="/accounts/login/" className="custom-p">Login</a>
            <form onSubmit={handleSubmit} method="post" encType="multipart/form-data">
                <input className="custom-p" type="text" name="username" placeholder="Username" maxLength="20" required />
                <input className="custom-p" type="password" name="password" placeholder="Password" maxLength="20" required />
                <input className="custom-p" type="submit" value="Login" />
                <input type="hidden" name="operation" value="login" />
            </form>
            <p className="custom-p">Don't have an account??</p>
            <Link to={`/accounts/create/`} style={{ fontWeight: "bold", fontSize: "32px" }}>Sign up</Link>
        </>
    );
}