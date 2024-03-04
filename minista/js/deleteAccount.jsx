import React, { useState, useEffect } from "react";

export default function DeleteAccount({ }) {
    const [logname, setLogname] = useState("");

    const apiUrl = `/api/v1/accounts/delete/`;

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
                }
            })
            .catch((error) => console.log(error));
    
        return () => {
            ignoreStaleRequest = true;
        };
    }, []);

    const handleDelete = async () => {
        try {
            const response = await fetch("/api/v1/accounts/delete/", {
                method: "DELETE",
                credentials: "same-origin",
            });

            if (!response.ok) {
                throw Error(response.statusText);
            }
            window.location.replace('/');
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h1>{logname}</h1>
            <button onClick={handleDelete}>confirm delete account</button>
        </div>
    );
}
