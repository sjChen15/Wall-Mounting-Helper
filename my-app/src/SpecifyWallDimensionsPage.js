import React, { useState } from 'react';

function SpecifyWallDimensionsPage() {
  const [wallDimensions, setWallDimensions] = useState({ length: '', width: '' });

  const handleDimensionsChange = (event) => {
    const { name, value } = event.target;
    setWallDimensions((prevDimensions) => ({ ...prevDimensions, [name]: value }));
  };

  return (
    <div>
      <h1>Specify Wall Dimensions</h1>
      <input
        type="text"
        name="length"
        placeholder="Length"
        value={wallDimensions.length}
        onChange={handleDimensionsChange}
      />
      <input
        type="text"
        name="width"
        placeholder="Width"
        value={wallDimensions.width}
        onChange={handleDimensionsChange}
      />
    </div>
  );
}

export default SpecifyWallDimensionsPage;
