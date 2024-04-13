export const Categories = (props) => {
    const responseData = props.responseData['files'];
    const status = props.responseData['status'];
    const docType = responseData.docType;

    return (
        <div>
            {
                status === 'ok'? <div className="status ok">ok</div> :
                    <div className="status bad">not ok</div>
            }
            {Object.keys(responseData).map(key => (
                <div className="response-file__container" key={key}>
                    <span className="response-file__key">
                        <code>{key}</code>
                    </span>
                    <span className="response-file__category">
                        {responseData[key].category}
                    </span>
                </div>
            ))}
        </div>
    )
}