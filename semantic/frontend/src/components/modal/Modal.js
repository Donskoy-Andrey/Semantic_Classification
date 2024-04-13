import React from 'react';
import ali_png from "../../img/ali.png"


function Modal({isOpen, onClose, onAccept}) {
    console.log(isOpen);
    if (!isOpen) return null;

    return (
        <div className="modal">
            <div className="modal__content">
                <h2> Примеры файлов</h2>
                <br></br>
                <button className="modal-close" onClick={onClose}>X</button>
                <div className="modal-buttons">
                    <div className="modal-buttons__row">
                        <div className="modal-buttons__col">
                            {/*<span className="modal-buttons__name">Пример 1</span>*/}
                            <p className="modal-buttons__specification">Спецификация: Банк</p>
                            <p className="modal-buttons__result">Результат: ок</p>
                        </div>
                        <button className="btn btn-primary modal-buttons__button" onClick={() => onAccept("first")}>
                            Отправить
                        </button>
                    </div>
                    <div className="modal-buttons__row">
                        <div className="modal-buttons__col">
                            {/*<span className="modal-buttons__name">Пример 2</span>*/}
                            <p className="modal-buttons__specification">Спецификация: Банк</p>
                            <p className="modal-buttons__result">Результат: ок</p>
                        </div>
                        <button className="btn btn-primary modal-buttons__button"
                                onClick={() => onAccept("second")}>
                            Отправить
                        </button>
                    </div>
                    {/*<div className="modal-buttons__row">*/}
                    {/*    <span className="modal-buttons__name">Пример 3</span>*/}
                    {/*    <button className="btn btn-primary modal-buttons__button" onClick={() => onAccept("third")}>Send*/}
                    {/*        Third*/}
                    {/*    </button>*/}
                    {/*</div>*/}

                </div>

            </div>
        </div>
    );
}

export default Modal;