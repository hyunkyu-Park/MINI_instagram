import React, { useState, useEffect } from "react";

export default function ChangePassword({ }) {
    const [logname, setLogname] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword1, setNewPassword1] = useState("");
    const [newPassword2, setNewPassword2] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [okMessage, setOkMessage] = useState("");
    const [showPassword, setShowPassword] = useState(false);

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

    const handleSubmit = (event) => {
        event.preventDefault();

        if (!isPasswordValid(newPassword1)) {
            alert("password must contain at least 8 characters including numbers, alphabets, and special characters.");
            event.target.elements.newPassword1.value = '';
            return;
        }
    
        if (!isPasswordValid(newPassword2)) {
            alert("password must contain at least 8 characters including numbers, alphabets, and special characters.");
            event.target.elements.newPassword2.value = '';
            return;
        }

        fetch(apiUrl, {
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
        })
        .then((response) => {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            setErrorMessage("")
            setOkMessage("Successfully changed!")
        })
        .catch((error) => {
            if(error.message == "UNAUTHORIZED"){
                setErrorMessage("New password 1 and New password 2 are different");
                setOkMessage("")
            }
            else if(error.message == "FORBIDDEN"){
                setErrorMessage("Wrong Current Password");
                setOkMessage("")
            }
            else{
                console.error(error);
            }
        });
    };


    const isPasswordValid = (password) => {
        const passwordRegex = /^(?=.*\d)(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,}$/;
        return passwordRegex.test(password);
    };

    return (
        <div className="password_change">
            <h2>Change Password</h2>
            {errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
            <div className="passwords_container">
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="oldPassword" className="custom-p">Current Password:</label>
                        <input
                            className="password_input"
                            type={showPassword ? "text" : "password"}
                            id="oldPassword"
                            name="oldPassword"
                            value={oldPassword}
                            onChange={(e) => setOldPassword(e.target.value)}
                            required
                        />
                    </div>
                    
                    <div>
                        <label htmlFor="newPassword1" className="custom-p">New Password:</label>
                        <input
                            className="password_input"
                            type={showPassword ? "text" : "password"}
                            id="newPassword1"
                            name="newPassword1"
                            value={newPassword1}
                            onChange={(e) => setNewPassword1(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="newPassword2" className="custom-p">Confirm New Password:</label>
                        <input
                            className="password_input"
                            type={showPassword ? "text" : "password"}
                            id="newPassword2"
                            name="newPassword2"
                            value={newPassword2}
                            onChange={(e) => setNewPassword2(e.target.value)}
                            required
                        />
                    </div>
                    
                    <div>
                        <label htmlFor="showPassword" className="password_input" >
                            <input
                                type="checkbox"
                                id="showPassword"
                                checked={showPassword}
                                onChange={() => setShowPassword(!showPassword)}
                            />
                            Show Password
                        </label>
                    </div>
                    
                    <input type="submit" name="update_password" value="Submit" className="custom-p" style={{maxWidth: 200, float: "right"}} />
                    <input type="hidden" name="operation" value="update_password" />
                </form>
            </div>
            
            {okMessage && <div style={{ color: "blue" }}>{okMessage}</div>}
            <p>
                Password must contain at least 8 characters including numbers, alphabets, and special characters
            </p>
            <h4>
                <a href="/accounts/edit/">Back to Account Edit</a>
            </h4>
        </div>
    );
}
