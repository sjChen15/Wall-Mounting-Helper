import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UploadPhotosPage from "./UploadPhotosPage";
import SpecifyWallDimensionsPage from "./SpecifyWallDimensionsPage";
import DragOrganizeDecorationsPage from "./DragOrganizeDecorationsPage";

const App = () => {
  return (
    <Router>
      <nav>
        <ul>
          <li>
            <Link to="/">UploadPhotosPage</Link>
          </li>
          <li>
            <Link to="/specify-wall-dimensions">SpecifyWallDimensionsPage</Link>
          </li>
          <li>
            <Link to="/drag-organize-decorations">
              DragOrganizeDecorationsPage
            </Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<UploadPhotosPage />} />
        <Route
          path="/specify-wall-dimensions"
          element={<SpecifyWallDimensionsPage />}
        />
        <Route
          path="/drag-organize-decorations"
          element={<DragOrganizeDecorationsPage />}
        />
      </Routes>
    </Router>
  );
};

export default App;
