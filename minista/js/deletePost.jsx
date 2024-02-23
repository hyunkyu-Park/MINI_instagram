import React from "react";
import PropTypes from "prop-types";

export default function DeletePost({postUrl}) {
    const deletePost = () => {
        fetch(postUrl, {
        method: "DELETE",
        credentials: "same-origin",
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            console.log(333)
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
};
