import React, { useEffect, useState } from 'react';
import { useAPI } from '../../context/APIContext';

const DrinksPage = () => {

    const [drinkList, setDrinkList] = useState([]);

    const categories = {
        "Cerveza": "🍺",
        "Vino": "🍷",
        "Cocktail": "🍸",
        "Copa sola": "🥃",
        "Copa": "🍹",
        "Refresco": "🥤",
    }

    const { drinks } = useAPI();

    useEffect(() => {
        const fetch = async () => {
            const response = await drinks.getAll("?limit=0");
            if (response.status >= 200 && response.status < 300) setDrinkList(response.data);
            else console.log(response);
        }

        fetch();
    }, []);

    return (
        <div className="container mt-4">
            <h1>Drinks List</h1>
            <div className="row g-3 mb-2">
                {drinkList.length === 0 ? <div className='col-12 text-center'><span className='spinner-border text-warning'></span></div> : drinkList.map((drink, index) => (
                    <div key={index} className="col-lg-3 col-md-4 col-sm-6 col-12">
                        <div className='card'>
                        <div className="card-body">
                            <h5 className="card-title">{drink.name} {categories[drink.category]}</h5>
                            <p className="card-text">
                                <strong>Category:</strong> {drink.category}
                            </p>
                            <p className="card-text">
                                <strong>Capacity:</strong> {drink.capacity}
                            </p>
                            <p className="card-text">
                                <strong>Score:</strong> {drink.score}
                            </p>
                        </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DrinksPage;