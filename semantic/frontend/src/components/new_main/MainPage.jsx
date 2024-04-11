import React from 'react';
import "./style.css";
import Modal from "../modal/Modal";

class MainPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            file: null,
            imageURL: null,
            loading: false,
            image: false,
            isModalOpen: false,
            visited: false
        };
    }

    // componentDidMount() {
    //     const mysiteVisited = localStorage.getItem('mysite_visited');
    //     console.log('mysiteVisited', mysiteVisited);
    //     // If mysite_visited doesn't exist or is null, set it to true in local storage
    //     if (!mysiteVisited) {
    //         localStorage.setItem('mysite_visited', 'true');
    //         this.setState({ visited: false });
    //     }
    // }

    // componentDidUpdate() {
    //     const visited = localStorage.getItem("timer");
    //     console.log('componentDidMount', visited)
    //     if (!this.state.visited) {
    //         this.setState({ visited: true });
    //     }
    // }


    openModal = () => {
        console.log("Modal open");
        this.setState({ isModalOpen: true });
    }

    closeModal = () => {
        console.log("Modal closed");
        this.setState({ isModalOpen: false });
    }

    handleFileChange = (event) => {
        this.setState({ file: event.target.files[0] });
    };

    handleDrop = (event) => {
        console.log(event);
        event.preventDefault();
        const droppedFile = event.dataTransfer.files[0];
        this.setState({ file: droppedFile });
    };

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

    handleSubmit = async (event) => {
        event.preventDefault();
        this.setState({ image: false });

        // Check if a file is selected
        if (!this.state.file) {
            console.error('No file selected');
            return;
        }

        // Check file type
        if (this.state.file.type !== 'image/png') {
            console.error('File is not a PNG');
            alert("Please choose a valid png type");
            return;
        }

        // Check file size
        if (this.state.file.size > 20 * 1024 * 1024) { // 20MB in bytes
            alert('File size exceeds 20MB');
            return;
        }

        const formData = new FormData();
        formData.append('file', this.state.file);
        console.log(formData);

        this.setState({ loading: true });

        try {
            const response = await fetch('http://localhost:8000/handle_image', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.blob();
                const url = URL.createObjectURL(data);
                this.setState({ imageURL: url, image: true });
                console.log(url);

            } else {
                console.error('Error uploading file');
            }
        } catch (error) {
            console.error('Error:', error);
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
                    <h1>Главная страница</h1>
                    {/*{!this.state.visited && <h3>hello</h3>}*/}
                    <div
                        className="drag-drop-field"
                        onDrop={this.handleDrop}
                        onDragOver={this.handleDragOver}
                    >
                        <p>{file === null ? `Перетащите файл сюда` : file.name}</p>
                    </div>
                    <div>
                        <div className="mb-3">
                            <label htmlFor="fileInput" className="form-label">Или выберите вручную</label>
                            <input type="file" className="form-control" id="fileInput" onChange={this.handleFileChange} />
                        </div>
                        <div className="input-control__buttons">
                            <button type="submit" className="btn btn-primary" onClick={this.handleSubmit}>Отправить</button>
                            <button className="btn btn-success modal-button" onClick={this.openModal}>Примеры</button>
                        </div>
                    </div>
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
