# Banglalion WiMAX API

This (dump) API allows you to fetch account data (credit, internet balance etc) from your Banglalion account.

## Requirment

* BeautifulSoup
* libxml

## How to Run

```bash
python3 banglalionwimaxapi.py
usage: banglalionwimaxapi.py -u USER -p PSWD
banglalionwimaxapi.py: error: the following arguments are required: -u, -p

# wrong username and password
python3 banglalionwimaxapi.py -u raj.mhs -p 123
Invalid Username or Password. Check and retry.

# correct username and password
python3 banglalionwimaxapi -u raj.minhaz -p 12345678
{
  "databank": "Unlimited",
  "walletbank_till": "2018-12-31 00:00:00",
  "user_name": "MD. MINHAZUL HAQUE",
  "expiration_date": "Promotional 20Mbps",
  "account_status": "Active",
  "walletbank": "Tk 1000",
  "user_id": "raj.minhaz",
  "databank_till": "2018-12-31 00:00:00",
  "total_balance": "Tk 5000.00"
}
```

## TODO

- [ ] Add HTTPS support
- [ ] Bugs?
