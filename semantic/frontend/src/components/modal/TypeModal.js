import React from 'react';

const typeMapping = {
    "proxy": "Доверенность",
    "contract": "Договор",
    "act": "Акт",
    "application": "Заявление",
    "order": "Приказ",
    "invoice": "Счет",
    "bill": "Приложение",
    "arrangement": "Соглашение",
    "contract offer": "Договор оферты",
    "statute": "Устав",
    "determination": "Решение",
};

function TypeModal({isOpen, onClose, onAccept}) {
    const [typeName, setTypeName] = React.useState('');
    const [types, setTypes] = React.useState({});
    if (!isOpen) return null;


    const handleCheckboxChange = (type) => {
        setTypes(prevTypes => ({
            ...prevTypes,
            [type]: !prevTypes[type]
        }));
    };

    return (
        <div className="modal">
            <div className="modal__content">
                <h2>Добавление нового типа</h2>
                <br></br>
                <button className="modal-close" onClick={onClose}>x</button>
                <div className="modal-form">
                    <input
                        type="text"
                        placeholder="Введите название типа"
                        value={typeName}
                        onChange={(e) => setTypeName(e.target.value)}
                    />
                    {Object.entries(typeMapping).map(([type, label]) => (
                        <div key={type}>
                            <input
                                type="checkbox"
                                id={type}
                                checked={types[type] || false}
                                onChange={() => handleCheckboxChange(type)}
                            />
                            <label htmlFor={type}>{label}</label>
                        </div>
                    ))}
                    <button onClick={() => onAccept(typeName, Object.keys(types).filter(key => types[key]))}>
                        Принять
                    </button>
                </div>
            </div>
        </div>
    );
}

export default TypeModal;
