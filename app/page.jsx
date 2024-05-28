"use client";

import React, { useState } from 'react';
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';

export default function Home() {
  const [imageFile, setImageFile] = useState(null);
  const [croppedImage, setCroppedImage] = useState(null);
  const [cropper, setCropper] = useState(null);

  const [src, setSrc] = useState(''); // initial src will be empty


  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setImageFile(file);
  };

  const handleCropImage = () => {
    if (cropper) {
      const croppedImageData = cropper.getCroppedCanvas().toDataURL();
      setCroppedImage(croppedImageData);
    }
  };

  const handleUpload = async () => {
    if (croppedImage) {
      const formData = new FormData();
      formData.append('image', croppedImage);

      const response = await fetch('./api/process_image', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {

        
        const processedImage = await response.blob();

        console.log(response)
        console.log(processedImage)
        const imageUrl = URL.createObjectURL(processedImage);
        setSrc(imageUrl);
      } else {
        console.error('Error processing the image');
      }
    }
  };

  const dataURItoBlob = (dataURI) => {
    const splitDataURI = dataURI.split(',');
    const byteString =
      splitDataURI[0].indexOf('base64') >= 0
        ? atob(splitDataURI[1])
        : decodeURI(splitDataURI[1]);
    const mimeString = splitDataURI[0].split(':')[1].split(';')[0];
    const ia = new Uint8Array(byteString.length);
    for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i);
    return new Blob([ia], { type: mimeString });
  };

  return (
    <div>
      <h1>Watermelon PFP Generator</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {imageFile && (
        <Cropper
          src={URL.createObjectURL(imageFile)}
          style={{ maxWidth: '500px', maxHeight: '500px' }}
          viewMode={2}
          guides={true}
          autoCropArea={0.8}
          autoCropAreaOrder={[0.5, 0.2, 0.3, 0.8]}
          aspectRatio={1}
          onInitialized={(instance) => setCropper(instance)}
        />
      )}
      <button onClick={handleCropImage}>Crop Image</button>
      {croppedImage && (
        <>
          <img src={croppedImage} alt="Cropped" />
          <button onClick={handleUpload}>Upload</button>
        </>
      )}
      {src && (
      <img src={src} alt="Processed" />
    )}
    </div>
  );
}