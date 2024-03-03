import React, { useState, useEffect } from "react";

export default function ChangePassword({ }) {
    const [logname, setLogname] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword1, setNewPassword1] = useState("");
    const [newPassword2, setNewPassword2] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [okMessage, setOkMessage] = useState("");

    const apiUrl = `/api/v1/accounts/password/`;

    useEffect(() => {
        let ignoreStaleRequest = false;
    
        fetch(apiUrl, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                if (!ignoreStaleRequest) {
                    setLogname(data.logname);
                    console.log(222)
                }
            })
            .catch((error) => console.log(error));
    
        return () => {
            ignoreStaleRequest = true;
        };
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            // Perform password change logic here
            // You can use the state variables oldPassword, newPassword1, and newPassword2

            // Example: Fetch request to change the password
            const response = await fetch(apiUrl, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    password: oldPassword,
                    new_password1: newPassword1,
                    new_password2: newPassword2,
                    operation: "update_password",
                }).toString(),
            });

            if (!response.ok) {
                throw Error(response.statusText);
            }

            setErrorMessage("")
            setOkMessage("Successfully changed!")

            // Password changed successfully, handle the response as needed
        } catch (error) {
            console.error(error);
            setErrorMessage(error.message);
            setOkMessage("")
        }
    };

    return (
        <div>
            <h2>Change Password</h2>
            {errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
            <form onSubmit={handleSubmit}>
                <label htmlFor="oldPassword">Old Password:</label>
                <input
                    type="password"
                    id="oldPassword"
                    name="oldPassword"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                />
                <label htmlFor="newPassword1">New Password:</label>
                <input
                    type="password"
                    id="newPassword1"
                    name="newPassword1"
                    value={newPassword1}
                    onChange={(e) => setNewPassword1(e.target.value)}
                    required
                />
                <label htmlFor="newPassword2">Confirm New Password:</label>
                <input
                    type="password"
                    id="newPassword2"
                    name="newPassword2"
                    value={newPassword2}
                    onChange={(e) => setNewPassword2(e.target.value)}
                    required
                />
                <input type="submit" name="update_password" value="Submit" />
                <input type="hidden" name="operation" value="update_password" />
            </form>
            {okMessage && <div style={{ color: "blue" }}>{okMessage}</div>}
            <p>
                <a href="/accounts/edit/">Back to Account Edit</a>
            </p>
        </div>
    );
}
