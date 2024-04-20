
import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

export default function Following({  }) {
    const { username } = useParams();

    const [logname, setLogname] = useState("");
    const [following, setFollowing] = useState([]);

    const followingUrl = `/api/v1/users/${username}/following/`

    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        // Call REST API to get the post's information
        fetch(followingUrl, { credentials: "same-origin" })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
                setLogname(data.logname);
                setFollowing(data.following);
                // console.log("called!")
                // console.log(data)
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
    }, [followingUrl]);

    if (logname === "") {
        return <div>Loading~</div>;
    }



    const renderFollowing = following.map((f) => (
        <div key={f.username} className="user_header" style={{ marginBottom: '10px' }}>
            <Link to={`/users/${f.username}`}>
                <img src={f.user_img_url} alt={`Following ${f.username}`} className="user_img" />
            </Link>
            <div className="user_info">
                <Link to={`/users/${f.username}`}>
                    <span className="user_id">{f.username}</span>
                </Link>
                {logname !== f.username && (
                    <div>
                        {f.logname_follows_username ? (
                            <div>
                                <span className="user_stats">Status: following</span>
                                <button onClick={() => handleUnfollow(f.username)}>unfollow</button>
                            </div>
                        ) : (
                            <div>
                                <span className="user_stats">Status: not following</span>
                                <button onClick={() => handleFollow(f.username)}>follow</button>
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
                <h2>Following</h2>
            </div>
            
            <div>
                {renderFollowing}
            </div>
        </div>
        
    );
}
