import React from 'react';
import ali_png from "../../img/ali.png"


function Modal({isOpen, onClose, onAccept}) {
    console.log(isOpen);
    if (!isOpen) return null;

    return (
        <div className="modal">
            <div className="modal__content">
                <h2> Примеры файлов</h2>
                <button className="modal-close" onClick={onClose}>X</button>
                <img src={ali_png} alt="ali" className="img__ali"/>
                <div className="modal-buttons">
                    <div className="modal-buttons__row">
                        <span className="modal-buttons__name">Пример 1</span>
                        <button className="btn btn-primary modal-buttons__button" onClick={() => onAccept("first")}>Send
                            First
                        </button>
                    </div>
                    <div className="modal-buttons__row">
                        <span className="modal-buttons__name">Пример 2</span>
                        <button className="btn btn-primary modal-buttons__button" onClick={() => onAccept("second")}>Send
                            Second
                        </button>
                    </div>
                    <div className="modal-buttons__row">
                        <span className="modal-buttons__name">Пример 3</span>
                        <button className="btn btn-primary modal-buttons__button" onClick={() => onAccept("third")}>Send
                            Third
                        </button>
                    </div>

                </div>

            </div>
        </div>
    );
}

export default Modal;