export interface Currency {
    id: number;
    num_code: number;
    char_code: string;
    name: string;
    created_at: string;
    currency_rates: CurrencyRate[] | null;
}
  
export interface CurrencyRate {
    id: number;
    currency_id: number;
    nominal: number;
    value: number;
    vunit_rate: number;
    modified_at: Date;
}