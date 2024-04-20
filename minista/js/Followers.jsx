
import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

export default function Followers({  }) {
    const { username } = useParams();

    const [logname, setLogname] = useState("");
    const [followers, setFollowers] = useState([]);

    const followersUrl = `/api/v1/users/${username}/followers/`

    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        // Call REST API to get the post's information
        fetch(followersUrl, { credentials: "same-origin" })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
                setLogname(data.logname);
                setFollowers(data.followers);
                console.log("called!")
                console.log(data)
            }
        })
        .catch((error) => {
            if(error.message == "NOT FOUND"){
                alert("Page not found");
                window.location.replace('/');
            }
            else{
                alert(error);
            }
        });

        return () => {
        // This is a cleanup function that runs whenever the Post component
        // unmounts or re-renders. If a Post is about to unmount or re-render, we
        // should avoid updating state.
        ignoreStaleRequest = true;
        };
    }, [followersUrl]);

    if (logname === "") {
        return <div>Loading~</div>;
    }



    const renderedFollowers = followers.map((follower) => (
        <div key={follower.username} className="user_header" style={{ marginBottom: '10px' }}>
            <Link to={`/users/${follower.username}`}>
                <img src={follower.user_img_url} alt={`Follower ${follower.username}`} className="user_img" />
            </Link>
            <div className="user_info">
                <Link to={`/users/${follower.username}`}>
                    <span className="user_id">{follower.username}</span>
                </Link>
                {logname !== follower.username && (
                    <div>
                        {follower.logname_follows_username ? (
                            <div>
                                <span className="user_stats">Status: following</span>
                                <button onClick={() => handleUnfollow(follower.username)}>unfollow</button>
                            </div>
                        ) : (
                            <div>
                                <span className="user_stats">Status: not following</span>
                                <button onClick={() => handleFollow(follower.username)}>follow</button>
                            </div>
                        )}
                    </div>
                )}
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
    
    const handleUnfollow = (followerUsername) => {
        const formData = new FormData();
        formData.append('operation', 'unfollow');
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
        .catch((error) => console.log('Unfollow error:', error));
    };
    
    return (
        <div>
            <div>
                <h2>Followers</h2>
            </div>
            
            <div>
                {renderedFollowers}
            </div>
        </div>
        
    );
}
