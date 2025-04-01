from django.shortcuts import render
from django.template.defaulttags import register

# Filter personalizado para acceder a diccionarios usando variables
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
    import requests
    import json
    
    # Añadir manejo de errores para las peticiones API
    try:
        price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD,EUR", timeout=10)
        price = json.loads(price_request.content)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        # Si hay un error, mostrar datos vacíos
        price = {"DISPLAY": {}, "RAW": {}}
    
    try:
        api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=ES", timeout=10)
        api = json.loads(api_request.content)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        # Si hay un error, mostrar datos vacíos
        api = {"Data": []}
    
    context = {
        'api': api, 
        'price': price,
        'page_title': 'Inicio - Criptcha Noticias',
    }
    return render(request, 'home.html', context)


def prices(request):
    if request.method == 'POST':
        import requests
        import json
        
        # Obtener el símbolo y validarlo
        quote = request.POST.get('quote', '').strip().upper()
        
        if not quote:
            notfound = "Por favor, introduce el símbolo de una criptomoneda"
            return render(request, 'prices.html', {'notfound': notfound, 'page_title': 'Explorar precios - Criptcha'})
        
        try:
            crypto_request = requests.get(f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={quote}&tsyms=USD", timeout=10)
            crypto = json.loads(crypto_request.content)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            # Si hay un error en la petición
            crypto = {"Response": "Error", "Message": "Ocurrió un error al conectar con la API"}
        
        context = {
            'quote': quote, 
            'crypto': crypto,
            'page_title': f'{quote} - Criptcha Noticias',
        }
        return render(request, 'prices.html', context)

    else:
        notfound = "Ingresa el símbolo de la criptomoneda que deseas explorar"
        return render(request, 'prices.html', {'notfound': notfound, 'page_title': 'Explorar precios - Criptcha'})
def home(request):
    import requests
    import json

    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD,EUR")
    price = json.loads(price_request.content)


    api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=ES")
    api = json.loads(api_request.content)
    return render(request, 'home.html', {'api': api, 'price': price })


def prices(request):
    if request.method == 'POST':
        import requests
        import json              
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote +"&tsyms=USD")
        crypto = json.loads(crypto_request.content)
        return render(request, 'prices.html', {'quote': quote, 'crypto': crypto})

    else:
        notfound = "Ingresa el símbolo de la Cripto Moneda que deseas explorar en Buscar una cripto"
        return render(request, 'prices.html', {'notfound': notfound})
