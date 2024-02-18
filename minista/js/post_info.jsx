import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import Button from "./Button";
import Comment from "./CommentCreate";
import CommentDelete from "./deleteComment";
import Double from "./doubleClick";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function PostInfo({ resultUrl }) {
  const [comments, setComments] = useState([]);
  const [created, setCreated] = useState("");
  const [imgUrl, setImgUrl] = useState("");
  const [likes, setLikes] = useState([]);
  const [owner, setOwner] = useState("");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [postId, setPostId] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    // Call REST API to get the post's information
    fetch(resultUrl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setComments(data.comments);
          setCreated(dayjs(data.created).fromNow());
          setImgUrl(data.imgUrl);
          setLikes(data.likes);
          setOwner(data.owner);
          setOwnerImgUrl(data.ownerImgUrl);
          setPostId(data.postid.toString());
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [resultUrl]);

  if (postId === "") {
    return <div>Loading~</div>;
  }

  const renderedComments = comments.map((comment) => (
    <div key={comment.commentid}>
      <b>
        {" "}
        <a href={`/users/${comment.owner}/`}>{comment.owner}</a>{" "}
      </b>
      <span data-testid="comment-text"> {comment.text} </span>
      {comment.lognameOwnsThis ? (
        <CommentDelete
          commentUrl={comment.url ? comment.url : ""}
          comments={comments}
          commentid={comment.commentid}
          setComments={setComments}
        />
      ) : (
        ""
      )}
    </div>
  ));

  return (
    <div className="post">
      <div className="above">
        <a href={`/users/${owner}/`}>
          {" "}
          <img src={ownerImgUrl} alt="owner_image" />
          <p>{owner}</p>
        </a>
        <p>
          <a href={`/posts/${postId}/`}>{created}</a>
        </p>
      </div>

      <div className="post_img">
        <Double
          imgUrl={imgUrl}
          postid={postId}
          setLikes={setLikes}
          lognameLikesThis={likes.lognameLikesThis}
          numLikes={likes.numLikes}
        />
        <Button
          likesUrl={likes.url ? likes.url : ""}
          postid={postId}
          lognameLikesThis={likes.lognameLikesThis}
          numLikes={likes.numLikes}
          setLikes={setLikes}
        />
      </div>

      <div className="below">
        <p>
          {likes.numLikes} {likes.numLikes === 1 ? "like" : "likes"}
        </p>
        {renderedComments}
        <Comment
          postid={postId}
          setComments={setComments}
          commentsList={comments}
        />
      </div>
    </div>
  );
}

PostInfo.propTypes = {
  resultUrl: PropTypes.string.isRequired,
};
