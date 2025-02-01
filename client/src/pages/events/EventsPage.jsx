import React from "react";
import { useAPI } from "../../context/APIContext";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const EventsPage = () => {
    const { BASE_URL, events } = useAPI();

    const [data, setData] = useState(undefined);

    useEffect(() => {
        const fetch = async () => {
            const response = await events.getAll("?limit=1");
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
                !data ? <div className="text-center"><span className="spinner-border text-warning mt-4"></span></div> : 
                data instanceof Array ? data.map((drink, index) => (
                    <div key={index} className="card m-2" style={{ width: "18rem" }}>
                        <div className="card-body">
                            <h5 className="card-title">{drink.name}</h5>
                            <p className="card-text">{drink.description}</p>
                        </div>
                    </div>
                )) : {data}
            }

            <p>Evento random para comprobar que el backend funciona :)</p>

            <div className="container text-center">
                <h2>Más páginas chulas</h2>
                <div className="row g-3">
                    <div className="col-12">
                    <Link to="/drinks" className="btn btn-secondary p-3">Ver bebidas</Link> 
                    </div>
                    <div className="col-12">
                    <Link to="/profile" className="btn btn-secondary p-3">Ver perfil</Link>
                    </div>
                </div>
            </div>

        
        </div>
    );
}

export default EventsPage;