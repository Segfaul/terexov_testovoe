import React, { useEffect, useState } from 'react';
import { client_currency } from '../config/client';
import { Currency } from '../config/types';

const CurrencyList: React.FC = () => {
  const [currencies, setCurrencies] = useState<Currency[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await client_currency.get('/api/v1/currency/?include_currency_rates=1');
        setCurrencies(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="currency-list">
      <h2>Currency List</h2>
      {currencies.map(currency => (
        <div key={currency.id} className="currency-item">
          <h3>{currency.name}</h3>
          <p>Character Code: {currency.char_code}</p>
          <p>Created At: {String(new Date(currency.created_at).toLocaleString())}</p>
          <div className="currency-rates">
            <h4>Currency Rates:</h4>
            {currency.currency_rates?.map(rate => (
              <div key={rate.id} className="rate-item">
                <p>Nominal: {rate.nominal}</p>
                <p>Value: {rate.value}</p>
                <p>VUnit Rate: {rate.vunit_rate}</p>
                <p>Modified At: {String(new Date(rate.modified_at).toLocaleString())}</p>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default CurrencyList;
