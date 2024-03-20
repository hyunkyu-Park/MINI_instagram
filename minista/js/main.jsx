import React from "react";
import { createRoot } from "react-dom/client";
import Post from "./post";
import '../static/css/style.css'; 
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PostDetail from "./post_detail";
import UserPage from "./userPage";
import UserEditPage from "./userEditPage"
import ChangePassword from "./changePasswordPage"
import DeleteAccount from "./deleteAccount"
import Followers from "./Followers"
import Following from "./Following"
import Explore from "./Explore";
import LoginPage from "./Login"
import CreatePage from "./Create";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));


root.render(
  <BrowserRouter>
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
          path="/accounts/edit/"
          element={<UserEditPage/>}
        />

        <Route
          path="/accounts/password/"
          element={<ChangePassword/>}
        />

        <Route
          path="/accounts/delete/"
          element={<DeleteAccount/>}
        />

        <Route 
          path="/users/:username/followers" 
          element={<Followers />}
        />

        <Route 
          path="/users/:username/following" 
          element={<Following />}
        />

        <Route
          path="/explore/"
          element={<Explore/>}
        />

        <Route
          path="/accounts/login/"
          element={<LoginPage/>}
        />

        <Route
          path="/accounts/create/"
          element={<CreatePage/>}
        />

      </Routes>
    </div>
  </BrowserRouter>
);
