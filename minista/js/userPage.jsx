
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function UserPage({  }) {
    const { username } = useParams();

    const [logname, setLogname] = useState("");
    const [full_name, setFull_name] = useState("");
    const [filename, setFilename] = useState("");
    const [logname_follows_username, setLogname_follows_username] = useState(false);
    const [following, setFollowing] = useState("");
    const [followers, setFollowers] = useState("");
    const [total_posts, setTotal_posts] = useState("");
    const [posts, setPosts] = useState([])

    const userUrl = `/api/v1/users/${username}/`

    const lognameIsUsername = logname==username;

    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;
        // Call REST API to get the post's information
        fetch(userUrl, { credentials: "same-origin" })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
            setLogname(data.logname);
            setFull_name(data.full_name);
            setFilename(data.filename)
            setLogname_follows_username(data.logname_follows_username);
            setFollowing(data.following);
            setFollowers(data.followers);
            setTotal_posts(data.total_posts);
            setPosts(data.posts);
            console.log(777)
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
    }, [userUrl]);

    if (full_name === "") {
        return <div>Loading~</div>;
    }


    const renderedPosts = posts.map((post) => (
        <div key={post.postid} className="user_posts">
            <img src={post.filename} style={{ width: '100%', height: '100%', objectFit: 'cover' }} alt={`Post ${post.postid}`} />
        </div>
    ));

    return (
        <div className="user_contents">
            <div className="user_header">
                <div>
                    <img src={filename} alt="user_image" className="user_img" />
                </div>

                <div className="user_info">
                    <div className="user_id">
                        <p style={{ marginRight: '40px' }}>{username}</p>
                        {lognameIsUsername ? (
                            <a href='/accounts/edit/'>edit profile</a>
                        ) : ( "" 
                        )}
                    </div>

                    <div className="user_stats">
                        <p style={{ marginRight: '30px' }}>Posts: {total_posts}</p>
                        <p style={{ marginRight: '30px' }}>followers: {followers}</p>
                        <p>following: {following}</p>
                    </div>
                    
                    <div className="full_name">
                        {full_name}
                    </div>
                </div>
            </div>

            {/* Posts */}
            <div className="user_posts_grid">
                {renderedPosts}
            </div>

        </div>
    );
}
