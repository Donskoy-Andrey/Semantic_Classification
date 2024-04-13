import React, { useState, useEffect } from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';

export const Categories = (props) => {
    const [screenWidth, setScreenWidth] = useState(window.innerWidth);

    useEffect(() => {
        const handleResize = () => {
            setScreenWidth(window.innerWidth);
        };
        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    const responseData = props.responseData['files'];
    const status = props.responseData['status'];

    const getDisplayKey = (key) => {
        if (screenWidth < 480 && key.length > 15) {
            const shortKey = `${key.substring(0, 5)}...${key.substring(key.length - 10)}`;
            return (
                <OverlayTrigger
                    placement="top"
                    overlay={<Tooltip id={`tooltip-${key}`}>{key}</Tooltip>}
                >
                    <span className="response-file__key">
                        <code>{shortKey}</code>
                    </span>
                </OverlayTrigger>
            );
        }
        return (
            <span className="response-file__key">
                <code>{key}</code>
            </span>
        );
    };

    return (
        <div>
            {
                status === 'ok' ?
                    <div className="status ok">ok</div> :
                    <div className="status bad">not ok</div>
            }
            {Object.keys(responseData).map(key => (
                <div className="response-file__container" key={key}>
                    {getDisplayKey(key)}
                    <span className="response-file__category">
                        {responseData[key].category}
                    </span>
                </div>
            ))}
        </div>
    );
};
