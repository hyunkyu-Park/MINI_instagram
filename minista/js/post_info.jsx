
import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import Button from "./Button";
import Comment from "./CommentCreate";
import CommentDelete from "./deleteComment";
import Double from "./doubleClick";
import PostDetail from "./post_detail";

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
          setCreated(dayjs.utc(data.created).local().fromNow());
          setImgUrl(data.imgUrl);
          setLikes(data.likes);
          setOwner(data.owner);
          setOwnerImgUrl(data.ownerImgUrl);
          setPostId(data.postid.toString());
          console.log(222)
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
  }, [resultUrl]);

  if (postId === "") {
    return (
      <div className="contents">
        <div className="posts">
            <div className="post_header" style={{ backgroundColor: 'white', width: 'auto', height: '20px' }}>
              <div className="post_profile" style={{ backgroundColor: 'rgb(240, 240, 240)', width: '180px', height: '25px' }}></div>
              <div style={{ backgroundColor: 'rgb(240, 240, 240)', width: '50px', height: '25px' }}></div>
            </div>
  
            <div style={{ backgroundColor: 'rgb(240, 240, 240)', width: 'auto', height: '600px'}}>
            </div>
  
            <div className="post_footer">
              <div className="post_likes" style={{ backgroundColor: 'rgb(240, 240, 240)', width: '60px', height: '20px' }}></div>
              
              <div className="comments">
                <div style={{ backgroundColor: 'rgb(240, 240, 240)', width: '180px', height: '20px' }}></div>
                <div style={{ backgroundColor: 'rgb(240, 240, 240)', width: '180px', height: '20px', marginTop: "3px"}}></div>
                <div style={{ backgroundColor: 'rgb(240, 240, 240)', width: '180px', height: '20px', marginTop: "3px" }}></div>
              </div>
            </div>
        </div>
      </div>
    )
  }

  const renderedComments = comments.map((comment) => (
    <div key={comment.commentid} className="comment">
      <div className="comment-content">
        <b>
          {" "}
          <a href={`/users/${comment.owner}/`}>{comment.owner}</a>{" "}
        </b>
        <span> {comment.text} </span>
      </div>
      <div className="comment-actions">
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
    </div>
  ));


  
  return (
    <div className="contents">
      <div className="posts">
        <article className="post">
          <div className="post_header">
            <div className="post_profile">
              <a href={`/users/${owner}/`}>
                <img src={ownerImgUrl} alt="owner_image" className="post_user_profile" loading="lazy"/>
                <p className="post_user_name">{owner}</p>
              </a>
            </div>
            <div>
              <a href={`/posts/${postId}/`}>
                {created}
              </a>
            </div>
          </div>

          <div>
            <Double
              imgUrl={imgUrl}
              postid={postId}
              setLikes={setLikes}
              lognameLikesThis={likes.lognameLikesThis}
              numLikes={likes.numLikes}
            />
          </div>

          <div className="post_footer">
            <div className="post_likes">
              <p>
                {likes.numLikes} {likes.numLikes === 1 ? "like" : "likes"}
              </p>
              <Button
                likesUrl={likes.url ? likes.url : ""}
                postid={postId}
                lognameLikesThis={likes.lognameLikesThis}
                numLikes={likes.numLikes}
                setLikes={setLikes}
              />
            </div>
            
            <div className="comments">
              {renderedComments}
              <Comment
                postid={postId}
                setComments={setComments}
                commentsList={comments}
              />
            </div>
          </div>
        </article>
      </div>
    </div>
  );
}

PostInfo.propTypes = {
  resultUrl: PropTypes.string.isRequired,
};
