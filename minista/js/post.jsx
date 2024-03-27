import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import PostInfo from "./post_info";

export default function Post({ url }) {
  const [results, setResults] = useState([]);
  const [next, setNext] = useState("");

  useEffect(() => {
    let ignoreStaleRequest = false;

    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setResults(data.results);
          setNext(data.next);
          console.log(111)
          console.log(data)
          if (data.results.length === 0) {
            window.location.href = "/explore/"; // 클라이언트 측에서 리디렉션 처리
          }
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  // Load more posts when the user scrolls to the bottom
  const fetchMoreData = () => {
    // Fetch the next page of posts using the 'next' URL
    fetch(next, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // Update the results and next URL
        setResults((prevResults) => [...prevResults, ...data.results]);
        setNext(data.next);
      })
      .catch((error) => console.log(error));
  };

  const renderedPosts = results.map((result) => (
    <PostInfo key={result.postid} resultUrl={result.url} />
  ));

  return (
    <>
      <div className="post">
        <InfiniteScroll
          dataLength={results.length}
          next={fetchMoreData}
          hasMore={next !== ""}
          loader={<h4>Loading...</h4>}
        >
          {renderedPosts}
        </InfiniteScroll>
      </div>
    </>
    
  );
}


Post.propTypes = {
  url: PropTypes.string.isRequired,
};