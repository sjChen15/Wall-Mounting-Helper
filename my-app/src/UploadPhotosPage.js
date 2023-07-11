import React, { useState } from 'react';

function UploadPhotosPage() {
  const [images, setImages] = useState([]);
  const [dimensions, setDimensions] = useState({ length: '', width: '' });

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setImages((prevImages) => [...prevImages, reader.result]);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleDimensionsChange = (event) => {
    const { name, value } = event.target;
    setDimensions((prevDimensions) => ({ ...prevDimensions, [name]: value }));
  };

  return (
    <div>
      <h1>Upload Photos</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      {images.map((image, index) => (
        <div key={index}>
          <img src={image} alt={`Decoration ${index}`} />
          <input
            type="text"
            name="length"
            placeholder="Length"
            value={dimensions.length}
            onChange={handleDimensionsChange}
          />
          <input
            type="text"
            name="width"
            placeholder="Width"
            value={dimensions.width}
            onChange={handleDimensionsChange}
          />
        </div>
      ))}
    </div>
  );
}

export default UploadPhotosPage;
