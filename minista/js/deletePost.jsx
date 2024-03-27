import React from "react";
import PropTypes from "prop-types";

export default function DeletePost({ postUrl, ownerShowUrl }) {
    const deletePost = () => {
        fetch(postUrl, {
            method: "DELETE",
            credentials: "same-origin",
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            // Reload/Refrash the page when it is updated
            window.location.replace(ownerShowUrl);
        })
        .catch((error) => console.log(error));
    };

    return (
        <div>
            <button
                type="button"
                onClick={deletePost}
            >
                Delete post
            </button>
        </div>
    );
}

DeletePost.propTypes = {
    postUrl: PropTypes.string.isRequired,
    ownerShowUrl: PropTypes.string.isRequired,
};
