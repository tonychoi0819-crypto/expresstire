from django.core.management.base import BaseCommand
from tires.models import Brand, Tyre, TyreVariant, Promotion
from orders.models import Coupon
from bookings.models import ShopLocation
import random


class Command(BaseCommand):
    help = "Seed ExpressTire with real HK tyre catalogue data"

    def handle(self, *args, **options):
        self.stdout.write('[ExpressTire] Seeding database...')

        # --- BRANDS ---
        brands_data = [
            ('Michelin', 'michelin', 'https://www.michelin.com.hk', 1),
            ('Pirelli', 'pirelli', 'https://www.pirelli.com', 2),
            ('Yokohama', 'yokohama', 'https://www.yokohama.com.hk', 3),
            ('Dunlop', 'dunlop', 'https://www.dunloptyres.com', 4),
            ('Goodyear', 'goodyear', 'https://www.goodyear.com', 5),
            ('Hankook', 'hankook', 'https://www.hankooktire.com/hk', 6),
            ('Bridgestone', 'bridgestone', 'https://www.bridgestone.com.hk', 7),
            ('Continental', 'continental', 'https://www.continental.com', 8),
            ('Toyo', 'toyo', 'https://www.toyotires.com', 9),
            ('Maxtrek', 'maxtrek', '', 10),
        ]
        brand_objs = {}
        for name, slug, url, order in brands_data:
            b, _ = Brand.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'website': url, 'order': order, 'is_active': True}
            )
            brand_objs[slug] = b
        self.stdout.write(f'  {Brand.objects.count()} brands')

        # --- TYPRES (with models matching hktyre.com) ---
        tyres_data = [
            # (brand_slug, name, slug, type, description)
            ('michelin', 'Pilot Sport 5', 'michelin-ps5', 'performance',
             'Latest flagship performance tyre. Exceptional wet grip, precise steering, long tread life. PS5 sets a new benchmark.'),
            ('michelin', 'Pilot Sport 4', 'michelin-ps4', 'performance',
             'Multi-award-winning performance tyre. Incredible grip in wet and dry conditions. Track-proven technology.'),
            ('michelin', 'Pilot Sport 4S', 'michelin-ps4s', 'performance',
             'Ultra-high performance tyre for sports cars. Born from 10+ years of motorsport heritage.'),
            ('michelin', 'Pilot Sport EV', 'michelin-psev', 'ev',
             'Designed specifically for electric vehicles. Low rolling resistance, max range, quiet ride.'),
            ('michelin', 'Primacy 4', 'michelin-primacy4', 'touring',
             'Comfort-focused touring tyre. Long-lasting, quiet, and fuel-efficient. Perfect daily driver.'),
            ('michelin', 'Pilot Sport 4 SUV', 'michelin-ps4-suv', 'suv',
             'Performance SUV tyre. Precise handling for SUVs without compromising comfort or grip.'),
            ('michelin', 'Energy Saver XM2', 'michelin-xm2', 'touring',
             'Fuel-efficient touring tyre. Low rolling resistance for maximum fuel economy.'),
            ('michelin', 'Agilis', 'michelin-agilis', 'light_truck',
             'Durability-focused tyre for vans and light trucks. Long life, puncture-resistant, high load capacity.'),
            ('pirelli', 'Powergy', 'pirelli-powergy', 'touring',
             "Pirelli's latest touring tyre. Excellent value, good wet grip, quiet and comfortable."),
            ('pirelli', 'P Zero', 'pirelli-pzero', 'performance',
             'Supercar OEM tyre. F1-derived technology for maximum dry and wet performance.'),
            ('yokohama', 'Advan Fleva V701', 'yokohama-v701', 'performance',
             'Sporty touring tyre. Great handling with comfort. Popular among sport sedan owners.'),
            ('yokohama', 'Advan Apex V601', 'yokohama-v601', 'performance',
             'Ultra-high performance tyre. Maximum grip for aggressive driving.'),
            ('dunlop', 'SP Sport LM705', 'dunlop-lm705', 'performance',
             'Premium sports tyre. Great wet and dry handling. Excellent value in the performance segment.'),
            ('goodyear', 'Eagle F1 Asymmetric 6', 'goodyear-f1a6', 'performance',
             '6th generation Eagle F1. Outstanding wet grip with innovative resin technology.'),
            ('hankook', 'Ventus S1 evo3', 'hankook-s1evo3', 'performance',
             'Award-winning flagship performance tyre. Incredible all-round capability at great value.'),
            ('hankook', 'Ventus S1 evo3 EV', 'hankook-s1evo3-ev', 'ev',
             'EV-specific version of the evo3. Low noise, high efficiency, EV-optimized compound.'),
            ('bridgestone', 'Turanza T005A', 'bridgestone-t005a', 'touring',
             'Premium touring tyre. Smooth, quiet, and fuel-efficient. Perfect for daily commuting.'),
            ('toyo', 'Proxes CF2 SUV', 'toyo-cf2-suv', 'suv',
             'Quiet SUV touring tyre. Low noise with confident wet weather performance.'),
            ('maxtrek', 'Maxtrek S6', 'maxtrek-s6', 'light_truck',
             'Value light truck tyre. Reliable, durable, and affordable for commercial vans.'),
        ]
        
        tyre_objs = {}
        for brand_slug, name, slug, tyre_type, desc in tyres_data:
            t, created = Tyre.objects.get_or_create(
                slug=slug,
                defaults={
                    'brand': brand_objs[brand_slug],
                    'name': name,
                    'tyre_type': tyre_type,
                    'description': desc,
                    'is_active': True,
                    'is_featured': brand_slug == 'michelin' and tyre_type == 'performance',
                }
            )
            tyre_objs[slug] = t
        self.stdout.write(f'  {Tyre.objects.count()} tyres')

        # --- VARIANTS (actual hktyre.com products) ---
        # Format: (tyre_slug, size_display, width, aspect, diameter, price, original_price)
        variants_data = [
            # Michelin Pilot Sport 5
            ('michelin-ps5', '215/45R17', 215, 45, 17, 1280, None),
            ('michelin-ps5', '225/45R17', 225, 45, 17, 1350, None),
            ('michelin-ps5', '225/45R18', 225, 45, 18, 1580, None),
            ('michelin-ps5', '235/45R18', 235, 45, 18, 1620, None),
            ('michelin-ps5', '245/40R18', 245, 40, 18, 1780, None),
            ('michelin-ps5', '235/40R19', 235, 40, 19, 1950, None),
            ('michelin-ps5', '245/45R19', 245, 45, 19, 2180, 2380),
            
            # Michelin Pilot PS4
            ('michelin-ps4', '205/55R16', 205, 55, 16, 880, None),
            
            # Michelin Pilot PS4S
            ('michelin-ps4s', '235/35R19', 235, 35, 19, 2100, None),
            
            # Michelin Pilot PSEV
            ('michelin-psev', '255/40R20', 255, 40, 20, 2550, 2980),
            
            # Michelin Primacy 4
            ('michelin-primacy4', '235/50R18', 235, 50, 18, 1380, None),
            
            # Michelin Pilot 4 SUV
            ('michelin-ps4-suv', '235/55R19', 235, 55, 19, 1980, None),
            
            # Pirelli Powergy
            ('pirelli-powergy', '195/55R15', 195, 55, 15, 520, None),
            ('pirelli-powergy', '195/65R15', 195, 65, 15, 580, None),
            ('pirelli-powergy', '205/60R16', 205, 60, 16, 720, None),
            
            # Yokohama V701
            ('yokohama-v701', '215/45R17', 215, 45, 17, 980, None),
            ('yokohama-v701', '205/55R17', 205, 55, 17, 920, None),
            
            # Yokohama V601
            ('yokohama-v601', '245/40R20', 245, 40, 20, 2680, None),
            
            # Dunlop LM705
            ('dunlop-lm705', '195/50R16', 195, 50, 16, 620, None),
            ('dunlop-lm705', '195/60R16', 195, 60, 16, 680, None),
            ('dunlop-lm705', '215/60R16', 215, 60, 16, 780, None),
            ('dunlop-lm705', '245/45R19', 245, 45, 19, 1850, None),
            
            # Goodyear Eagle F1A6
            ('goodyear-f1a6', '225/40R18', 225, 40, 18, 1450, None),
            ('goodyear-f1a6', '235/35R19', 235, 35, 19, 1850, None),
            
            # Hankook S1evo3
            ('hankook-s1evo3', '255/45R19', 255, 45, 19, 2100, None),
            
            # Hankook S1evo3 EV
            ('hankook-s1evo3-ev', '255/45R19', 255, 45, 19, 2250, None),
            
            # Bridgestone T005A
            ('bridgestone-t005a', '225/50R18', 225, 50, 18, 1180, None),
            
            # Maxtrek S6
            ('maxtrek-s6', '215/70R16C', 215, 70, 16, 680, None),
            ('maxtrek-s6', '225/50R18C', 225, 50, 18, 850, None),
        ]

        for tyre_slug, size, w, a, d, price, orig_price in variants_data:
            tyre = tyre_objs.get(tyre_slug)
            if tyre:
                TyreVariant.objects.get_or_create(
                    tyre=tyre,
                    size_display=size,
                    defaults={
                        'width': w,
                        'aspect': a,
                        'diameter': d,
                        'price': price,
                        'original_price': orig_price,
                        'in_stock': True,
                        'stock_qty': random.randint(2, 20),
                        'is_active': True,
                    }
                )
        self.stdout.write(f'  {TyreVariant.objects.count()} variants')

        # --- PROMOTIONS ---
        promos_data = [
            ('Michelin PS5 — Buy 4 Save $400!', 'michelin-ps5-bundle',
             'Purchase 4 Michelin Pilot Sport 5 tyres and save $400 total. Professional installation & balancing included.',
             'bundle', 400, 0, 4, 'MICHELIN4'),
            ('First Order 10% Off', 'new-customer-10',
             'New customers get 10% off first order. Valid for any tyre purchase.',
             'percent', 10, 0, 1, 'NEW10'),
        ]
        for title, slug, desc, dtype, dval, min_p, min_q, code in promos_data:
            Promotion.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'discount_type': dtype,
                    'discount_value': dval,
                    'min_purchase': min_p,
                    'min_qty': min_q,
                    'code': code,
                    'is_active': True,
                }
            )
        self.stdout.write(f'  {Promotion.objects.count()} promotions')

        # --- COUPONS ---
        Coupon.objects.get_or_create(
            code='SAVE100',
            defaults={
                'discount_type': 'fixed',
                'discount_value': 100,
                'min_purchase': 500,
                'max_uses': 100,
                'is_active': True,
            }
        )

        # --- SHOP LOCATIONS ---
        ShopLocation.objects.get_or_create(
            name='ExpressTire 土瓜灣總店',
            defaults={
                'address': 'G/F, Man Shun Factory Building, 20 Chi Kiang Street, To Kwa Wan, Kowloon',
                'phone': '+852 2362 4809',
                'email': 'info@expresstire.com',
                'opening_hours': 'Mon-Sat 8:00am-6:00pm',
                'is_main': True,
                'is_active': True,
            }
        )
        ShopLocation.objects.get_or_create(
            name='ExpressTire 火炭分店',
            defaults={
                'address': 'Unit i, International Industrial Centre, 2-8 Kwei Tei Street, Fo Tan, Sha Tin',
                'phone': '+852 2362 4809',
                'opening_hours': 'Mon-Sat 8:00am-6:00pm',
                'is_main': False,
                'is_active': True,
            }
        )
        self.stdout.write(f'  {ShopLocation.objects.count()} shop locations')

        self.stdout.write(self.style.SUCCESS(
            f'[ExpressTire] Done! {Brand.objects.count()} brands, {Tyre.objects.count()} tyres, '
            f'{TyreVariant.objects.count()} variants, {Promotion.objects.count()} promos'
        ))
