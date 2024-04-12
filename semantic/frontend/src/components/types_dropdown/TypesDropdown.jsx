export const TypesDropdown = (props) => {

    const onChange = props.onChange;
    const currentDocType = props.currentDocType;
    const documentTypes = props.documentTypes;

    const handleChange = (event) => {
        onChange(event.target.value);
    }

    return (
        <div className="">
            <h3>Выберите тип документа:</h3>
            <select
                className="form-select form-select-lg mb-3"
                name={"select"}
                value={currentDocType}
                onChange={handleChange}
            >
                {Object.keys(documentTypes).map(key => (
                    <option key={key} value={key}>{documentTypes[key]}</option>
                ))}
            </select>
        </div>
    )
}