import React from "react";
import PropTypes from "prop-types";

function Double({ imgUrl, postid, setLikes, lognameLikesThis, numLikes }) {
  const url = "/api/v1/likes/";
  // Function to handle double click event
  const handleDoubleClick = () => {
    if (!lognameLikesThis)
      fetch(`${url}?postid=${postid}`, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
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
    <div style={{width: "100%", height:"600px"}}>
      <img src={imgUrl} alt="image_url" onDoubleClick={handleDoubleClick} loading="lazy" style={{ width: '100%', height: '100%', objectFit: 'cover' }}/>
    </div>
  );
}

Double.propTypes = {
  imgUrl: PropTypes.string.isRequired,
  setLikes: PropTypes.func.isRequired,
  postid: PropTypes.string.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
  numLikes: PropTypes.number.isRequired,
};

export default Double;
