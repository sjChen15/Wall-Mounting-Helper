import React, { useState } from "react";

function UploadPhotosPage() {
  const [photo, setPhoto] = useState(null);
  const [length, setLength] = useState("");
  const [width, setWidth] = useState("");
  const [downloadCount, setDownloadCount] = useState(0);

  const handlePhotoChange = (e) => {
    const selectedPhoto = e.target.files[0];
    setPhoto(selectedPhoto);
  };

  const handleLengthChange = (e) => {
    setLength(e.target.value);
  };

  const handleWidthChange = (e) => {
    setWidth(e.target.value);
  };

  const formatDownloadCount = (count) => {
    return count.toString().padStart(3, "0");
  };

  const handleDownload = () => {
    if (!photo || !length || !width) {
      alert("Please upload a photo and enter length and width values.");
      return;
    }

    const blob = new Blob([photo], { type: photo.type });
    const url = URL.createObjectURL(blob);

    const fileName = `${formatDownloadCount(
      downloadCount
    )}-L${length}-W${width}.${photo.type.split("/")[1]}`;
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    a.click();

    URL.revokeObjectURL(url);

    // Update the download count
    setDownloadCount((prevCount) => prevCount + 1);

    // Clear the UI fields after download
    setPhoto(null);
    setLength("");
    setWidth("");
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handlePhotoChange} />
      <br />
      <label>
        Length:
        <input type="number" value={length} onChange={handleLengthChange} />
      </label>
      <br />
      <label>
        Width:
        <input type="number" value={width} onChange={handleWidthChange} />
      </label>
      <br />
      <button onClick={handleDownload}>Submit</button>
    </div>
  );
}

export default UploadPhotosPage;
