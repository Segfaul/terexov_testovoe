import React from 'react';
import CurrencyList from './currency/CurrencyList';
import { currency_api_url } from './config/client';

const Home: React.FC = () => {
  return (
    <div className='home'>
      <h1>Welcome to Currency API</h1>
      <p className='description'>
        This is a simple application to display currency data fetched from an API. Click{' '}
        <a href={currency_api_url + '/api/redoc'} target="_blank">
          here
        </a>{' '}
        to view the API.
      </p>
      <CurrencyList />
    </div>
  );
};

export default Home;
