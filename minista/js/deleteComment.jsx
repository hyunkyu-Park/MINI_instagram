import React from "react";
import PropTypes from "prop-types";

export default function DeleteComment({
  commentUrl,
  setComments,
  commentid,
  comments,
}) {
  const deleteComment = () => {
    fetch(commentUrl, {
      method: "DELETE",
      credentials: "same-origin",
    })
      .then(() => {
        const newList = comments.filter(
          (comment) => comment.commentid !== commentid,
        );
        setComments(newList);
      })
      .catch((error) => console.log(error));
  };
  return (
    <div>
      <button
        type="button"
        onClick={deleteComment}
      >
        Delete comment
      </button>
    </div>
  );
}

DeleteComment.propTypes = {
  commentUrl: PropTypes.string.isRequired,
  setComments: PropTypes.func.isRequired,
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      commentid: PropTypes.number.isRequired,
      lognameOwnsThis: PropTypes.bool.isRequired,
      owner: PropTypes.string.isRequired,
      ownerShowUrl: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    })
  ).isRequired,
  commentid: PropTypes.number.isRequired,
};
