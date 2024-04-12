import React, {useState, useRef} from 'react';

const FileUploader = (props) => {
    const allowedFormats = ['pdf', 'doc', 'docx', 'xlsx', 'txt', 'rtf'];
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        setSelectedFiles([...selectedFiles, ...e.target.files]);
        console.log('selected files: ', e.target.files[0]);
    };

    const checkFiles = (files) => {
        for (let i = 0; i < files.length; i++) {
            const extension = files[i].name.split('.').pop().toLowerCase();
            if (!allowedFormats.includes(extension)){
                setFormValid(false);
                return false;
            }
        }
        setFormValid(true);
        return true;
    }

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const files = [...e.dataTransfer.files];
        setSelectedFiles([...selectedFiles, ...files]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        if (selectedFiles.length === 0) {
            alert('Выберите файлы');
            return;
        }
        if (!checkFiles(selectedFiles)){
            alert('Удалите невалидные файлы');
            return;
        }
        for (let i = 0; i < selectedFiles.length; i++) {
            formData.append('files', selectedFiles[i]);
        }

        const config = {
            method: 'POST',
            body: formData,
        };

        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/upload', config);
            if (response.ok) {
                console.log('Files uploaded successfully');
            } else {
                console.error('Error uploading files:', response.statusText);
            }
        } catch (error) {
            console.error('Error uploading files:', error);
        } finally {
          setLoading(false);
        }
    };

    const checkFileFormat = (file) => {
        const extension = file.name.split('.').pop().toLowerCase();
        return allowedFormats.includes(extension);
    }

    const handleClick = () => {
        fileInputRef.current.click();
    };

    const deleteFile = (index) => {
        const updatedFiles = [...selectedFiles];
        updatedFiles.splice(index, 1);
        setSelectedFiles(updatedFiles);
    };

    return (
        <div>
            <div
                onClick={handleClick}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                className="drag-drop-field"
            >
                {/*<i className="fa-regular fa-file fa-big"></i>*/}
                {/*<i className="fa-solid fa-file-export fa-big"></i>*/}
                <i className="fa-solid fa-file-arrow-down fa-big"></i>
                <h3>Перетащите файл сюда <br/>или <div className="text-warning">выберите вручную</div></h3>
                <div className="drag-drop-field__extensions">pdf, doc, docx, xlsx, txt, rtf</div>
                <input
                    type="file"
                    multiple
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    style={{display: 'none'}}
                />
            </div>

            <div className="input-control__buttons">
                <button className="btn btn-primary" onClick={handleUpload}>Отправить</button>
                <button className="btn btn-success modal-button" onClick={props.openModal}>Примеры</button>
            </div>
            <div className="uploaded-file__container">
            {selectedFiles.length > 0 && (
                selectedFiles.map((file, i) => (
                    <div className={`uploaded-file__item ${checkFileFormat(file)? "": "wrong"}`} key={i}>
                        <span>{file.name}</span>
                        <button className="btn uploaded-file__button" onClick={() =>deleteFile(i)}>X</button>
                    </div>
                ))
            )}
            </div>
            {loading && (
                <div className="big-center loader"></div>
            )}
        </div>
    );
};

export default FileUploader;
