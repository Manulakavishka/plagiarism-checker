import React, { useState } from 'react';

const App = () => {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('http://127.0.0.1:5001/upload', {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log(data); // Display response in console (for now)
        
        // Assuming the response contains 'extracted_text'
        setExtractedText(data.extracted_text);  // Store extracted text in React state
      } else {
        console.error('Failed to upload file:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  return (
    <div>
      <h1>Plagiarism Checker</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Check Plagiarism</button>
      </form>

      {/* Display extracted text */}
    {extractedText && (
      <div>
        <h3>Extracted Text</h3>
        <pre>{extractedText}</pre>
      </div>
    )}
    </div>
  );
};

export default App;
