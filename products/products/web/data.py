from datetime import datetime

ingredients = [
    { 
        'id': '602f2ab3-97bd-468e-a88b-bb9e00531fd0',
        'name': 'Milk',
        'stock': {
            'quantity': 100.00,
            'unit': 'LITERS',
        }, 
        'supplier': '92f2daa3-a4f8-4aae-8d74-5ldd74e5de6d',
        'products': [],
        'lastUpdate': datetime.now(),
    }, 
]

products = [
    {
        'id': '6961ca64-78f3-41d4-bc3b-a63550754bd8',
        'name': 'Walnut Bomb',
        'price': 37.00,
        'size': 'MEDIUM',
        'available': False,
        'ingredients': [
            {
                'ingredient': '602f2ab3-97bd-468e-a88b-bb9e00531fd0',
                'quantity': 100.00,
                'unit': 'LITERS',
            }
        ],
        'hasFilling': False,
        'hasNutsToppingOption': True,
        'lastUpdated': datetime.now(),
    },
    {
        'id': 'e4e33d0b-1355-4735-9505-749e3fdf8a16',
        'name': 'Cappuccino Star',
        'price': 12.50,
        'size': 'SMALL',
        'available': True,
        'ingredients': [
            {
                'ingredient': '602f2ab3-97bd-468e-a88b-bb9e00531fd0',
                'quantity': 100.00,
                'unit': 'LITERS',
            }
        ],
        'hasCreamOnTopOption': True,
        'hasServeOnIceOption': True,
        'lastUpdated': datetime.now(),
    },
]

suppliers = [
    {
        'id': '92f2daa3-a4f8-4aae-8d74-5ldd74e5de6d',
        'name': 'supplier1',
        "address": "Moscow 1",
        "contactNumber": "+46456756743424",
        "email": "company1@mail.com",
    }
]