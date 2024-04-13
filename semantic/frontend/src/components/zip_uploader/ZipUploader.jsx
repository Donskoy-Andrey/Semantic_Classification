import React, { useRef, useState } from 'react';

const ZipUploadComponent = ({ docsNumber, openModal }) => {
    const fileInputRef = useRef(null);
    const [uploadedFile, setUploadedFile] = useState(null);
    const [outputFile, setOutputFile] = useState(null);

    const handleClick = () => {
        fileInputRef.current.click();
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const files = event.dataTransfer.files;
        handleFileChange(files);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    const handleFileChange = (files) => {
        setUploadedFile(files[0]);
    }

    const handleUpload = async (files) => {
        const formData = new FormData();
        formData.append('file', files[0]); // Assuming only one file is selected

        try {
            console.log("response")
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/upload`, {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                throw new Error('Failed to upload file');
            }
            const data = await response.json(); // Assuming the server returns JSON data
            setOutputFile(data); // Assuming response.data contains the uploaded file information
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const handleDownload = () => {
        // Implement download logic here
    };

    // const handleUpload = () => {
    //     // Implement upload logic here
    // };

    return (
        <div className="main-page">
            <div className="container mt-4 main-bg">
                <div
                    onClick={handleClick}
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    className="drag-drop-field"
                >
                    <i className="fa-regular fa-file-lines fa-big"></i>
                    <h3>
                        Перетащите zip файл сюда <br />
                        или <div className="text-warning">выберите его вручную</div>
                    </h3>
                    <div className="drag-drop-field__extensions">zip</div>
                    <input
                        type="file"
                        accept=".zip"
                        onChange={(e) => handleFileChange(e.target.files)}
                        ref={fileInputRef}
                        style={{ display: 'none' }}
                    />
                </div>

                <div className="input-control__buttons">
                    <button className="btn btn-primary" onClick={handleUpload}>
                        Отправить
                    </button>
                    {outputFile && (
                        <div>
                            <button className="btn btn-primary" onClick={handleDownload}>
                                Скачать
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ZipUploadComponent;
