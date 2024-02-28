import React from "react";
import { createRoot } from "react-dom/client";
import Post from "./post";
import '../static/css/style.css'; 
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PostDetail from "./post_detail";
import UserPage from "./userPage";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));


root.render(
  <Router>
    <div>
      <Routes>
        <Route 
          path="/"
          element={<Post url="/api/v1/posts/"/>}
        />

        <Route
          path="/posts/:id/"
          element={<PostDetail />}
        />

        <Route 
          path="/users/:username/" 
          element={<UserPage />}
        />

        <Route
          path="/api/v1/accounts/edit/"
          element={</>}
        />

      </Routes>
    </div>
  </Router>
);
