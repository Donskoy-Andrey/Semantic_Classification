export const TypesDropdown = (props) => {

    const onChange = props.onChange;
    const currentDocType = props.currentDocType;
    const documentTypes = props.documentTypes;
    return (
        <div className="btn-group">
            <button type="button" className="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                {documentTypes[currentDocType]}
            </button>
            <ul className="dropdown-menu">
                {Object.keys(documentTypes).map(key => (
                    <li key={key}><p className="dropdown-item" onClick={() => onChange(key)}>{documentTypes[key]}</p></li>
                ))}
            </ul>
        </div>
    )
}