import React from "react";
import { useAPI } from "../../context/APIContext";
import { useState, useEffect } from "react";

const EventsPage = () => {
    const { BASE_URL, drinks } = useAPI();

    const [data, setData] = useState(undefined);

    useEffect(() => {
        const fetch = async () => {
            const response = await drinks.getAll("/?limit=1");
            if (response.status >= 200 && response.status < 300) setData(response.data);
            else {
                setData(response.data.detail);
                console.log(response);
            }            
        }

        fetch();
    }, []);

    return (
        <div className="container d-flex justify-content-center align-items-center flex-column">
            {
                !data ? <span className="spinner-border text-primary mt-4"></span> : 
                data instanceof Array ? data.map((drink, index) => (
                    <div key={index} className="card m-2" style={{ width: "18rem" }}>
                        <div className="card-body">
                            <h5 className="card-title">{drink.name}</h5>
                            <p className="card-text">{drink.capacity} ml</p>
                        </div>
                    </div>
                )) : {data}
            }
        </div>
    );
}

export default EventsPage;