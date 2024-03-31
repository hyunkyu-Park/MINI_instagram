
import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

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

    const logout = () => {
        fetch(`/api/v1/accounts/logout/`, {
            method: "POST",
            credentials: "same-origin",
        })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                window.location.replace(`/accounts/login/`);
            })
            .catch((error) => console.log(error));
    };

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


    const renderedPosts = posts.map((post) => (
        <div key={post.postid} className="user_posts">
            <Link to={`/posts/${post.postid}`}>
                <img src={post.filename} style={{ width: '100%', height: '100%', objectFit: 'cover' }} alt={`Post ${post.postid}`} />
            </Link>
        </div>
    ));

    if (full_name === "") {
        return <div>Loading~</div>;
    }

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
                            <>
                                <Link to={`/accounts/edit/`}>edit profile</Link>
                                <input type="submit" value="logout" onClick={logout} style={{ marginLeft: '30px',fontSize: '18px' }} />
                            </>
                        ) : (
                            <div>
                                <input
                                    type="submit"
                                    value={logname_follows_username ? "unfollow" : "follow"}
                                    onClick={() => (logname_follows_username ? handleUnfollow(username) : handleFollow(username))}
                                    style={{fontSize: '18px' }}
                                />
                            </div>
                            
                        )}
                    </div>

                    <div className="user_stats">
                        <p style={{ marginRight: '30px' }}>{total_posts === 1 ? "Post: " : "Posts: "} {total_posts}</p>
                        <Link to={`/users/${username}/followers/`} style={{ marginRight: '30px' }}>
                            {followers === 1 ? "Follower: " : "Followers: "} {followers}
                        </Link>
                        <Link to={`/users/${username}/following/`} style={{ marginRight: '30px' }}>
                            <p>Following: {following}</p>
                        </Link>
                        
                    </div>
                    
                    <div className="full_name">
                        {full_name}
                    </div>
                </div>
            </div>
            
            <div>
                {logname === username && (
                    <form className="new_post_container" action="/api/v1/posts/" method="POST" encType="multipart/form-data">
                        <input style={{fontSize:18}} type="file" name="file" accept="image/*" required />
                        <input style={{fontSize:18}} type="submit" name="create_post" value="upload new post" />
                        <input type="hidden" name="operation" value="create" />
                    </form>
                )}
            </div>

            {/* Posts */}
            <div className="user_posts_grid">
                {renderedPosts}
            </div>

        </div>
    );
}
