import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function CreatePage() {

    const [showPassword, setShowPassword] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();

        // Get form input values
        const username = event.target.elements.username.value;
        const password = event.target.elements.password.value;
        const email = event.target.elements.email.value;
        const file = event.target.elements.file.value;

        // Check username length
        if (username.length < 6 ) {
            alert("Username must be at least 6 characters long");
            event.target.elements.username.value = '';
            return;
        }

        // Check email format
        if (!isEmailValid(email)) {
            alert("Invalid email format");
            event.target.elements.email.value = '';
            return;
        }

        // Check username length and password complexity
        if (!isPasswordValid(password)) {
            alert("password must contain at least 8 characters including numbers, alphabets, and special characters. No space!!!");
            event.target.elements.password.value = '';
            return;
        }

        // When the user does not give pic
        if(!file){
            const formData = new FormData(event.target);
            fetch(`/api/v1/accounts/generatePic/`,{
                method: "POST",
                credentials: "same-origin",
                body: formData,
            })
            .then((response) =>{
                if (!response.ok) throw Error(response.statusText);
                window.location.replace('/');
            })
            .catch((error) => {
                if(error.message == "CONFLICT"){
                    alert("existing username");
                    // reset the username inside of inputs in form
                    event.target.elements.username.value = '';
                }
                else{
                    console.error(error);
                }
            });
        }

        // When the user gives pic
        else{
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
                    window.location.replace('/');
                })
                .catch((error) => {
                    if(error.message == "CONFLICT"){
                        alert("existing username");
                        // reset the username inside of inputs in form
                        event.target.elements.username.value = '';
                    }
                    else{
                        console.error(error);
                    }
                });
            }
        
    };

    const isEmailValid = (email) => {
        // Regular expression for validating email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    // Function to check password complexity
    const isPasswordValid = (password) => {
        const passwordRegex = /^(?=.*\d)(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9])\S{8,}$/;
        return passwordRegex.test(password);
    };

    return (
        <div className="password_change">
            
            <form onSubmit={handleSubmit} method="post" encType="multipart/form-data">
                <div className="create_container">
                    <p className="custom-p">Photo</p>
                    <input className="custom-p" type="file" name="file"  />
                </div>
                
                <div className='passwords_container'>
                    <p className="custom-p">Name</p>
                    <input className="password_input" type="text" name="fullname" placeholder="Full Name" maxLength="20" required />
                    <p className="custom-p">Username</p>
                    <input className="password_input" type="text" name="username" placeholder="Username" maxLength="15" required />
                    <p className="custom-p">Email</p>
                    <input className="password_input" type="text" name="email" placeholder="Email" maxLength="30" required />
                    <p className="custom-p">Password</p>
                    <input 
                        className="password_input" 
                        type={showPassword ? "text" : "password"}
                        name="password" 
                        placeholder="Password" 
                        maxLength="20"
                        required />
                    <div>
                        <label htmlFor="showPassword" className="password_input" >
                            <input
                                style={{margin: 10}}
                                type="checkbox"
                                id="showPassword"
                                checked={showPassword}
                                onChange={() => setShowPassword(!showPassword)}
                            />
                            Show Password
                        </label>
                    </div>
                    <input className="custom-p" type="submit" name="signup" value="Sign Up" />
                    <input type="hidden" name="operation" value="create" />
                </div>
                
            </form>
            <p className="custom-p">Already have an account? <a href="/accounts/login/">Login</a></p>
        </div>
    );
}
