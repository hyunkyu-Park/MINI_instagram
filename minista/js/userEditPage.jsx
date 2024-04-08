import React, { useState, useEffect } from "react";

export default function UserEditPage({ }) {
    const [logname, setLogname] = useState("");
    const [email, setEmail] = useState("");
    const [fullName, setFullName] = useState("");
    const [userPhotoUrl, setUserPhotoUrl] = useState("");
    const [username, setUsername] = useState("");

    const apiUrl = `/api/v1/accounts/edit/`;

    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        // Call REST API to get the post's information
        fetch(apiUrl, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                // If ignoreStaleRequest was set to true, we want to ignore the results of the
                // the request. Otherwise, update the state to trigger a new render.
                if (!ignoreStaleRequest) {
                    setLogname(data.logname);
                    setEmail(data.email);
                    setFullName(data.full_name);
                    setUserPhotoUrl(data.user_photo_url);
                    setUsername(data.username);
                    console.log(111)
                    console.log(data)
                }
            })
            .catch((error) => console.log(error));

        return () => {
            // This is a cleanup function that runs whenever the Post component
            // unmounts or re-renders. If a Post is about to unmount or re-render, we
            // should avoid updating state.
            ignoreStaleRequest = true;
        };
    }, []);

    const handleFullNameChange = (event) => {
        setFullName(event.target.value);
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const isEmailValid = (email) => {
        // Regular expression for validating email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        // Get form input values
        const email = event.target.elements.email.value;

        // Check email format
        if (!isEmailValid(email)) {
            alert("Invalid email format");
            event.target.elements.email.value = '';
            return;
        }

        
        // Create FormData object using Form data
        const formData = new FormData(event.target);
        
        // Sending data to server
        fetch("/api/v1/accounts/edit_account", {
            method: "POST",
            credentials: "same-origin",
            body: formData,
        })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                // Reload/Refrash the page when it is updated
                window.location.reload();
            })
            .catch((error) => console.log(error));
    };


    if (username === "") {
        return <div>Loading~</div>;
    }

    return (
        <div>
            <style>
                {`
                    .custom-p {
                        font-size: 24px;
                    }
                `}
            </style>
            <h1>Edit account</h1>

            <div>
                <img src={userPhotoUrl} alt="owner_image" className="user_img_for_edit_profile" />
            </div>

            <div>
                <p className="custom-p">{username}</p>
            </div>

            <form onSubmit={handleSubmit} encType="multipart/form-data">
                <label htmlFor="file" className="custom-p">Photo:</label>
                <input type="file" name="file" id="file" accept="image/*" className="custom-p" />
                <label htmlFor="fullname" className="custom-p">Name:</label>
                <input
                    type="text"
                    name="fullname"
                    id="fullname"
                    value={fullName}
                    onChange={handleFullNameChange}
                    maxLength="20"
                    className="custom-p"
                    required
                />
                <label htmlFor="email" className="custom-p">Email:</label>
                <input
                    type="text"
                    name="email"
                    id="email"
                    value={email}
                    onChange={handleEmailChange}
                    maxLength="30"
                    className="custom-p"
                    required
                />
                <input type="submit" name="update" value="Submit" className="custom-p" />
                <input type="hidden" name="operation" value="edit_account" />
            </form>

            <p><a href="/accounts/password/" className="custom-p">Change Password</a></p>
            <p><a href="/accounts/delete/" className="custom-p">Delete Account</a></p>
        </div>
    );
}
