from web_messaging.extensions import twilio_client, currency_converter

def get_twilio_credits():
    """ Get Twilio balance amount """ 
    try: 
        balance_data = twilio_client.api.v2010.balance.fetch()
        balance = float(balance_data.balance)
        currency = balance_data.currency
        return balance, currency  
    except Exception:
        return "Error 505"

def inject_credit():
    """ Inject Twilio balance on a template layer """ 
    credits_response = get_twilio_credits()
    if type(credits_response) is str:
        return dict(credit=credits_response)
    (credit, currency) = credits_response
    if currency != "EUR":
        credit = currency_converter.convert(credit, currency, 'EUR')
    return dict(credit=(round(credit,2)))

