import React, { useEffect, useState } from 'react';
import { useAPI } from '../../context/APIContext';

const UserPage = () => {

    const [user, setUser] = useState(undefined);
    const { users } = useAPI();


    useEffect(() => {
        const f = async () => {
            const response = await users.getAll();
            if (response.status >= 200 && response.status < 300) {
            const randomUser = response.data[Math.floor(Math.random() * response.data.length)];
            setUser(randomUser);
            }
            else console.log(response);
        }
        f()
    }, []);

    return (
        !user ? <div className='container text-center'><span className="spinner-border text-warning mt-4"></span></div> :
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <img src={user.profile_picture} alt={`${user.name} profile picture`} style={{ borderRadius: '50%', width: '150px', height: '150px' }} />
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    );
};

export default UserPage;