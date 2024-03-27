
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export default function Explore({  }) {

    const [logname, setLogname] = useState("");
    const [notFollowing, setNotFollowing] = useState([]);

    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        // Call REST API to get the post's information
        fetch(`/api/v1/explore/`, { credentials: "same-origin" })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
                setLogname(data.logname);
                setNotFollowing(data.not_following)
                
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

    if (logname === "") {
        return <div>Loading~</div>;
    }



    const renderPeople = notFollowing.map((user) => (
        <div key={user.username} className="user_header" style={{ marginBottom: '10px' }}>
            <Link to={`/users/${user.username}`}>
                <img src={user.user_img_url} alt={`new_user ${user.username}`} className="user_img" />
            </Link>
            <div className="user_info">
                <Link to={`/users/${user.username}`}>
                    <span className="user_id">{user.username}</span>
                </Link>

                <button onClick={() => handleFollow(user.username)} style={{marginTop: '30px', fontSize: '18px'}}>follow</button>

            </div>
            
        </div>
    ));

    const handleFollow = (followerUsername) => {
        const formData = new FormData();
        formData.append('operation', 'follow');
        formData.append('username', followerUsername);
    
        fetch('/api/v1/following/', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin',
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            window.location.reload();
        })
        .catch((error) => console.log('Follow error:', error));
    };
    
    return (
        <div>
            <div>
                <h2>Discover People</h2>
            </div>
            
            <div>
                {renderPeople}
            </div>
        </div>
        
    );
}
