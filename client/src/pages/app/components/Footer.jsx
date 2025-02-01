import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-dark text-white text-center py-3">
            <div className="container">
                <p className="mb-0">&copy; {new Date().getFullYear()} <a href='https://github.com/AFND-Industries' target='_blank' style={{textDecoration: "none", color: "#9ad8fa"}}>AFND Industries</a> :)</p>
            </div>
        </footer>
    );
};

export default Footer;