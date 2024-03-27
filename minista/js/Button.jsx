import React from "react";
import PropTypes from "prop-types";

export default function Button({
  likesUrl,
  postid,
  lognameLikesThis,
  numLikes,
  setLikes,
}) {
  const url = "/api/v1/likes/";

  const unlike = () => {
    fetch(likesUrl, {
      method: "DELETE",
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        console.log("likesUrl")
        console.log(likesUrl)
        const tempLikes = {
          lognameLikesThis: false,
          numLikes: numLikes - 1,
          url: null,
        };
        setLikes(tempLikes);
      })
      .catch((error) => console.log(error));
  };

  const like = () => {
    let check = `${url}?postid=${postid}`
    console.log("check")
    console.log(check)
    fetch(`${url}?postid=${postid}`, {
      method: "POST",
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        console.log("likesUrl")
        console.log(likesUrl)
        return response.json();
      })
      .then((data) => {
        const tempLikes = {
          lognameLikesThis: true,
          numLikes: numLikes + 1,
          url: data.url,
        };
        setLikes(tempLikes);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div>
      <button 
        type="button"
        onClick={lognameLikesThis === true ? unlike : like}
      >
        {lognameLikesThis === true ? "unlike" : "like"}
      </button>
    </div>
  );
}

Button.propTypes = {
  likesUrl: PropTypes.string.isRequired,
  postid: PropTypes.string.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
  numLikes: PropTypes.number.isRequired,
  setLikes: PropTypes.func.isRequired,
};
