import React from "react";
import { useAPI } from "../../context/APIContext";
import { useState, useEffect } from "react";

const EventsPage = () => {
    const { BASE_URL, apiMethods } = useAPI();

    const [data, setData] = useState(undefined);

    useEffect(() => {
        const fetch = async () => {
            const response = await apiMethods.get(BASE_URL + "/test");
            if (response.status >= 200 && response.status < 300) setData(response.data.detail);
            else {
                setData(response.data.detail);
                console.log(response);
            }
        }

        fetch();
    }, []);

    return (
        <div className="container d-flex justify-content-center align-items-center flex-column">
            {data}
        </div>
    );
}

export default EventsPage;