import React, {useState} from 'react';
import "./style.css";
import Modal from "../modal/Modal";

const MainPage = () => {

    const [file, setFile] = useState(null);
    const [imageURL, setImageURL] = useState(null);
    const [loading, setLoading] = useState(false);
    const [image, setImage] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);


    const openModal = () => {
        console.log("Modal open");
        setIsModalOpen(true);
    }
    const closeModal = () => {
        console.log("Modal closed");
        setIsModalOpen(false);
    }

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleDrop = (event) => {
        console.log(event);
        event.preventDefault();
        const droppedFile = event.dataTransfer.files[0];
        setFile(droppedFile);
    };

    const sendExample = async (event, name) => {
        console.log("Sending example");
        setIsModalOpen(false);
        console.log('name=', name);


        const requestData = {name: "first"};
        setLoading(true);
        console.log(requestData);
        try {
            const response = await fetch('http://localhost:8000/handle_example', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' // Specify content type as JSON
                },
                body: JSON.stringify(requestData) // Convert JSON object to string
            });

            if (!response.ok) {
                throw new Error('Failed to upload file');
            }

            const data = await response.blob();
            const url = URL.createObjectURL(data);
            setImageURL(url);
            console.log('Image URL:', url);
            setImage(true);
        } catch (error) {
            console.error('Error:', error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setImage(false);

        // Check if a file is selected
        if (!file) {
            console.error('No file selected');
            return;
        }

        // Check file type
        if (file.type !== 'image/png') {
            console.error('File is not a PNG');
            alert("Please choose a valid png type");
            return;
        }

        // Check file size
        if (file.size > 20 * 1024 * 1024) { // 20MB in bytes
            alert('File size exceeds 20MB');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        console.log(formData);

        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/handle_image', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.blob();
                const url = URL.createObjectURL(data);
                setImageURL(url);
                console.log(url);
                setImage(true);

            } else {
                console.error('Error uploading file');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };


    const handleDragOver = (event) => {
        event.preventDefault();
    };

    return (
        <div className="main-page">
            <div className="container mt-4 main-bg">
                <h1>Main Page</h1>
                <div
                    className="drag-drop-field"
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                >
                    <p>{file === null ? `Drag and drop your files here` : file.name}</p>
                </div>
                <div>
                    <div className="mb-3">
                        <label htmlFor="fileInput" className="form-label">Or choose file</label>
                        <input type="file" className="form-control" id="fileInput" onChange={handleFileChange}/>
                    </div>
                    <div className="input-control__buttons">
                        <button type="submit" className="btn btn-primary" onClick={handleSubmit}>Send</button>
                        <button className="btn btn-success modal-button" onClick={openModal}>Examples</button>
                    </div>
                </div>
                {loading && (
                    <div className="big-center loader"></div>
                )}
                {image && <div className="card mt-4">
                    {imageURL && <img src={imageURL} className="card-img-top" alt="Uploaded"/>}
                </div>}
                <div>
                    <Modal isOpen={isModalOpen} onClose={closeModal} onAccept={sendExample}>
                        <h2>Modal Content</h2>
                        <p>This is the content of the modal.</p>
                    </Modal>
                </div>
            </div>

        </div>
    );
};

export default MainPage;
