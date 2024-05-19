import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Post from "./post";
import PostDetail from "./post_detail";
import UserPage from "./userPage";
import UserEditPage from "./userEditPage";
import ChangePassword from "./changePasswordPage";
import DeleteAccount from "./deleteAccount";
import Followers from "./Followers";
import Following from "./Following";
import Explore from "./Explore";
import LoginPage from "./Login";
import CreatePage from "./Create";
import '../static/css/style.css'; 

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

function App() {
  const [darkMode, setDarkMode] = useState(false);

  // check if the user previously selected dark mode
  useEffect(() => {
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'enabled') {
      setDarkMode(true);
      document.body.classList.add('dark-mode');
    }
  }, []);

  const toggleDarkMode = () => {
    if (darkMode) {
      setDarkMode(false);
      document.body.classList.remove('dark-mode');
      localStorage.removeItem('darkMode');
    } else {
      setDarkMode(true);
      document.body.classList.add('dark-mode');
      localStorage.setItem('darkMode', 'enabled');
    }
  };

  return (
    <div style={{ display: "flex" }}>
      <div style={{ marginRight: 10 }}>
        <button onClick={toggleDarkMode} style={{ marginTop: 10 }}>
          {darkMode ? 'Light Mode' : 'Dark Mode'}
        </button>
      </div>

      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Post url="/api/v1/posts/" />} />
          <Route path="/posts/:id/" element={<PostDetail />} />
          <Route path="/users/:username/" element={<UserPage />} />
          <Route path="/accounts/edit/" element={<UserEditPage />} />
          <Route path="/accounts/password/" element={<ChangePassword />} />
          <Route path="/accounts/delete/" element={<DeleteAccount />} />
          <Route path="/users/:username/followers" element={<Followers />} />
          <Route path="/users/:username/following" element={<Following />} />
          <Route path="/explore/" element={<Explore />} />
          <Route path="/accounts/login/" element={<LoginPage />} />
          <Route path="/accounts/create/" element={<CreatePage />} />
        </Routes>
      </div>
    </div>
  );
}

root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
