import React from 'react';
import "./style.css";
import Modal from "../modal/Modal";
import FileUploader from "../file_uploader/FileUploader";
import {TypesDropdown} from "../types_dropdown/TypesDropdown";


class MainPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            files: [],
            currentDocType: "bank",
            documentTypes: {
                "bank": "банк",
                "test": "тест"
            },
            imageURL: null,
            loading: false,
            image: false,
            isModalOpen: false,
            visited: false
        };
    }

    setFiles = (files) => {
        this.setState({ files: files });
    }

    onDocumentTypeChange = (key) => {
        this.setState({ currentDocType: key });
        console.log("choose: ", key);
    }


    openModal = () => {
        console.log("Modal open");
        this.setState({ isModalOpen: true });
    }

    closeModal = () => {
        console.log("Modal closed");
        this.setState({ isModalOpen: false });
    }

    sendExample = async (event, name) => {
        console.log("Sending example");
        this.setState({ isModalOpen: false });
        console.log('name=', name);

        const requestData = { name: "first" };
        this.setState({ loading: true });
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
            this.setState({ imageURL: url, image: true });
            console.log('Image URL:', url);
        } catch (error) {
            console.error('Error:', error.message);
        } finally {
            this.setState({ loading: false });
        }
    };


    handleDragOver = (event) => {
        event.preventDefault();
    };

    render() {
        const { file, loading, image, imageURL, isModalOpen, visited } = this.state;
        console.log('visited',visited);

        return (
            <div className="main-page">
                <div className="container mt-4 main-bg">
                    <TypesDropdown onChange={this.onDocumentTypeChange} currentDocType={this.state.currentDocType} documentTypes={this.state.documentTypes}/>
                    <FileUploader openModal={this.openModal} setFiles={this.setFiles} currentDocType={this.state.currentDocType}/>

                    {loading && (
                        <div className="big-center loader"></div>
                    )}
                    {image && <div className="card mt-4">
                        {imageURL && <img src={imageURL} className="card-img-top" alt="Uploaded" />}
                    </div>}
                    <div>
                        <Modal isOpen={isModalOpen} onClose={this.closeModal} onAccept={this.sendExample}>
                            <h2>Modal Content</h2>
                            <p>This is the content of the modal.</p>
                        </Modal>
                    </div>
                </div>
            </div>
        );
    }
}

export default MainPage;
