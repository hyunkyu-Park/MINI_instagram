import React, { useState } from "react";
import PropTypes from "prop-types";

export default function Comment({ postid, setComments }) {
  const url = `/api/v1/comments/?postid=${postid}`;

  const [text, setText] = useState("");

  const addComment = () => {
    fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json", // Specify JSON content type
      },
      body: JSON.stringify({ text }), // Convert text to JSON and send in the body
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // Update comments state with the newly added comment
        setComments((commentsList) => [...commentsList, data]);
        // Clear the text input
        setText("");
      })
      .catch((error) => console.error(error));
  };
  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (text.trim() !== "") {
      // Call the addComment function to submit the comment
      addComment();
    }
  };

  return (
    <div>
      <form data-testid="comment-form" onSubmit={handleSubmit}>
        Comment:
        <input
          className="ui input"
          type="text"
          value={text}
          onChange={handleChange}
        />
      </form>
    </div>
  );
}

Comment.propTypes = {
  postid: PropTypes.string.isRequired,
  setComments: PropTypes.func.isRequired,
};
