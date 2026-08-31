#!/usr/bin/env python3
"""Burst batch: add 20 WA leads (51->70), outreach drafts, pipeline rows."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ROOT / "leads" / "targets.json"
OUTREACH = ROOT / "outreach"
REVIEW = OUTREACH / "REVIEW-INDEX.md"
DEMO_BASE = "https://edisonrees.github.io/macrosa-web/demos"

NEW_LEADS = [
    {
        "slug": "bee-painting-services",
        "name": "Bee Painting Services",
        "logo_text": "BEE",
        "industry": "Painting",
        "city": "Gosnells",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Residential and commercial painting, Gosnells",
        "phone_raw": "+61405789789",
        "phone_display": "0405 789 789",
        "email": "beepaintingservices@gmail.com",
        "address": "Gosnells, WA",
        "service_area": "Gosnells, Mandurah to Yanchep and Perth metro",
        "years": 12,
        "rating": "4.9",
        "hero_headline": "Fresh paint. Fair quotes. Gosnells locals.",
        "hero_subhead": "Bee Painting Services handles interior and exterior work for homes and businesses across Perth. Free quotes by phone or Facebook message.",
        "about_headline": "Quality prep. Clean finish.",
        "about": "Bee Painting Services is a Gosnells based painting team covering Bedfordale to Mundaring and everywhere in between. Commercial, residential, interior and exterior with proper prep and tidy clean-up.",
        "band_headline": "Planning a repaint?",
        "band_text": "Call or message for a free quote. Pensioner discounts available.",
        "gallery_captions": ["Interior painting", "Exterior house painting", "Commercial jobs", "Gosnells and surrounds"],
        "source": "https://www.facebook.com/beepaintingservice",
        "has_website": False,
        "website_note": "beepaintingservices.com.au dead/archived. FB and phone only.",
        "demo_flag": "outreach",
        "contact_note": "Facebook Messenger and phone. Dead domain on record.",
        "services": [
            {"title": "Interior painting", "desc": "Walls, ceilings, doors and trims with proper prep."},
            {"title": "Exterior painting", "desc": "Facades, eaves, fences and outdoor areas."},
            {"title": "Commercial painting", "desc": "Shops, offices and strata common areas."},
            {"title": "Free quotes", "desc": "Colour advice and transparent pricing before work starts."},
        ],
    },
    {
        "slug": "perth-city-painters",
        "name": "Perth City Painters",
        "logo_text": "PCP",
        "industry": "Painting",
        "city": "Beckenham",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Professional painters, Beckenham and Perth",
        "phone_raw": "+61411427787",
        "phone_display": "0411 427 787",
        "address": "Beckenham, WA",
        "service_area": "Beckenham, Perth metro and southern suburbs",
        "years": 10,
        "rating": "5.0",
        "hero_headline": "Professional painting you can trust.",
        "hero_subhead": "Perth City Painters delivers interior and exterior work across Perth with free no-obligation quotes.",
        "about_headline": "Reliable. Friendly. Local.",
        "about": "Perth City Painters is a Beckenham based team known for before-and-after transformations on homes across Perth. Straight communication and solid prep on every job.",
        "band_headline": "Need a painter this month?",
        "band_text": "Call 0411 427 787 or message on Facebook for a free quote.",
        "gallery_captions": ["House repaints", "Interior refreshes", "Exterior facades", "Beckenham projects"],
        "source": "https://www.facebook.com/perthcitypainters",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone only. No standalone website.",
        "services": [
            {"title": "House painting", "desc": "Full interior and exterior repaints."},
            {"title": "Interior work", "desc": "Rooms, ceilings and feature walls."},
            {"title": "Exterior work", "desc": "Weatherboards, brick and render."},
            {"title": "Free quotes", "desc": "Personalised quotes with no obligation."},
        ],
    },
    {
        "slug": "ezyclean-carpet-cleaning",
        "name": "Ezyclean Carpet Cleaning",
        "logo_text": "EZY",
        "industry": "Carpet Cleaning",
        "city": "Perth",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Carpet and upholstery cleaning, Perth",
        "phone_raw": "+61456104380",
        "phone_display": "0456 104 380",
        "address": "Perth, WA",
        "service_area": "Perth metro and surrounds",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Carpets that look new again.",
        "hero_subhead": "Wayne runs Ezyclean across Perth with powerful stain removal for carpets, rugs and lounges. Call or message for a quote.",
        "about_headline": "Local owner. Real results.",
        "about": "Ezyclean Carpet Cleaning is a Perth based service specialising in carpet, rug and upholstery cleaning with modern chemical technology and honest before-and-after results.",
        "band_headline": "Rent inspection or spring clean?",
        "band_text": "Call 0456 104 380 or message on Facebook to book.",
        "gallery_captions": ["Carpet steam clean", "Upholstery refresh", "Stain removal", "Perth metro jobs"],
        "source": "https://www.facebook.com/profile.php?id=661816873830471",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone only. No business website.",
        "services": [
            {"title": "Carpet cleaning", "desc": "Rooms, stairs and whole-home packages."},
            {"title": "Upholstery cleaning", "desc": "Lounges, dining chairs and mattresses."},
            {"title": "Stain treatment", "desc": "Grease, pet and high-traffic stains."},
            {"title": "Rug cleaning", "desc": "On-site or pickup by arrangement."},
        ],
    },
    {
        "slug": "after-builder-projects",
        "name": "After Builder Projects",
        "logo_text": "ABP",
        "industry": "Landscaping",
        "city": "Perth",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Landscaping, paving and outdoor solutions",
        "phone_raw": "+61401208079",
        "phone_display": "0401 208 079",
        "email": "afterbuilderprojects@gmail.com",
        "address": "Perth, WA",
        "service_area": "Perth metro and surrounds",
        "years": 12,
        "rating": "5.0",
        "hero_headline": "Outdoor spaces, done properly.",
        "hero_subhead": "After Builder Projects handles landscaping, paving, artificial grass, fencing and decking across Perth.",
        "about_headline": "Nandal Group. Local crew.",
        "about": "After Builder Projects is a Perth landscaping team specialising in paving, earthworks, artificial turf, reticulation and decking for residential and commercial clients.",
        "band_headline": "New build or backyard refresh?",
        "band_text": "Call Andrew on 0401 208 079 or message on Facebook for a quote.",
        "gallery_captions": ["Paving installs", "Artificial turf", "Reticulation", "Decking and fencing"],
        "source": "https://www.facebook.com/afterbuilderprojects",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook, phone and email. No standalone website.",
        "services": [
            {"title": "Landscaping", "desc": "Design, prep and full outdoor makeovers."},
            {"title": "Paving", "desc": "Driveways, paths and entertaining areas."},
            {"title": "Artificial grass", "desc": "Supply and install for low-maintenance yards."},
            {"title": "Fencing and decking", "desc": "Timber and composite outdoor structures."},
        ],
    },
    {
        "slug": "apex-home-maintenance",
        "name": "Apex Home Maintenance WA",
        "logo_text": "APEX",
        "industry": "Handyman and Cleaning",
        "city": "Rockingham",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Handyman, pressure cleaning and gutters",
        "phone_raw": "+61419951171",
        "phone_display": "0419 951 171",
        "address": "Rockingham, WA",
        "service_area": "Rockingham, Mandurah and Perth metro",
        "years": 8,
        "rating": "5.0",
        "hero_headline": "Property maintenance, sorted.",
        "hero_subhead": "Janko and the Apex team handle pressure cleaning, gutters, handyman jobs and rural earthmoving across Perth south.",
        "about_headline": "Insured. Reliable. One call.",
        "about": "Apex Home Maintenance WA is a Rockingham based crew offering high-pressure cleaning, gutter clearing, window cleaning, handyman repairs and rural fencing.",
        "band_headline": "Gutters blocked or driveway stained?",
        "band_text": "Call 0419 951 171 or message on Facebook for same-week availability.",
        "gallery_captions": ["Pressure cleaning", "Gutter clearing", "Handyman repairs", "Southern suburbs"],
        "source": "https://www.facebook.com/p/Apex-Home-Maintenance-WA-61573773347360/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone only.",
        "services": [
            {"title": "Pressure cleaning", "desc": "Driveways, colorbond and exterior walls."},
            {"title": "Gutter cleaning", "desc": "Clear, flush and soft-wash options."},
            {"title": "Handyman", "desc": "Small repairs, furniture assembly and fixes."},
            {"title": "Rural earthmoving", "desc": "Fencing, decking and property tidy-ups."},
        ],
    },
    {
        "slug": "c-bees-cupcakes",
        "name": "C Bee's Cupcakes",
        "logo_text": "C BEE",
        "industry": "Cupcakes and Baking",
        "city": "Parkwood",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Custom cupcakes, Parkwood",
        "phone_raw": "+61423834891",
        "phone_display": "0423 834 891",
        "address": "Torridon Avenue, Parkwood WA 6147",
        "service_area": "Parkwood, southern suburbs and Perth metro",
        "years": 8,
        "rating": "4.9",
        "hero_headline": "Cupcakes made to order.",
        "hero_subhead": "C Bee's Cupcakes in Parkwood bakes custom cupcakes for birthdays, events and celebrations. Call or text to order.",
        "about_headline": "Home baker. Personal service.",
        "about": "C Bee's Cupcakes is a Parkwood based cupcake maker serving Perth's southern suburbs with custom flavours and designs for parties and events.",
        "band_headline": "Party coming up?",
        "band_text": "Call or WhatsApp 0423 834 891 with your date, quantity and theme.",
        "gallery_captions": ["Birthday cupcakes", "Custom toppers", "Event boxes", "Parkwood orders"],
        "source": "https://www.facebook.com/search/top?q=c%20bee%27s%20cupcakes%20perth",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Phone and WhatsApp primary. No website.",
        "services": [
            {"title": "Custom cupcakes", "desc": "Themed designs for birthdays and events."},
            {"title": "Cupcake boxes", "desc": "Dozen and custom quantity orders."},
            {"title": "Celebration orders", "desc": "Baby showers, weddings and corporate treats."},
            {"title": "Local pickup", "desc": "Parkwood collection or delivery by arrangement."},
        ],
    },
    {
        "slug": "cupcakin-fun",
        "name": "Cupcakin Fun",
        "logo_text": "CUPCAKIN",
        "industry": "Cupcake Classes",
        "city": "Perth",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Cupcake decorating classes, Perth",
        "phone_raw": "+61423640565",
        "phone_display": "0423 640 565",
        "email": "cupcakinfun@gmail.com",
        "address": "Perth, WA",
        "service_area": "Perth metro",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Learn to decorate like a pro.",
        "hero_subhead": "Honey runs Cupcakin Fun cupcake decorating workshops across Perth. Perfect for hens, birthdays and team nights.",
        "about_headline": "Chef-led. Fun nights.",
        "about": "Cupcakin Fun is a Perth based cupcake decorating class business run by an experienced chef. Walk away with six decorated cupcakes and new skills.",
        "band_headline": "Girls night or team event?",
        "band_text": "Call or message 0423 640 565 to book a class.",
        "gallery_captions": ["Class nights", "Decorated cupcakes", "Group events", "Perth workshops"],
        "source": "https://cupcakinfun.wixsite.com/cupcakinfun",
        "has_website": False,
        "website_note": "Wix site only. Atrocious enough to pitch upgrade.",
        "demo_flag": "outreach",
        "contact_note": "Phone and Wix contact. No proper website.",
        "services": [
            {"title": "Decorating classes", "desc": "Tuesday night workshops with themed designs."},
            {"title": "Private events", "desc": "Hens, birthdays and corporate team building."},
            {"title": "Cupcake takeaway", "desc": "Six cupcakes to take home per participant."},
            {"title": "Gift vouchers", "desc": "Classes as gifts for food-loving friends."},
        ],
    },
    {
        "slug": "tiny-bobcat-landscaping",
        "name": "A Tiny Bobcat Landscaping",
        "logo_text": "BOBCAT",
        "industry": "Landscaping",
        "city": "Landsdale",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Bobcat and landscaping, Landsdale",
        "phone_raw": "+61412776377",
        "phone_display": "0412 776 377",
        "address": "Landsdale, WA 6065",
        "service_area": "Landsdale, northern suburbs and Perth metro",
        "years": 10,
        "rating": "5.0",
        "hero_headline": "Earthworks and landscaping, done right.",
        "hero_subhead": "A Tiny Bobcat Landscaping handles bobcat work, site prep and landscaping across Perth's north.",
        "about_headline": "Compact gear. Big results.",
        "about": "A Tiny Bobcat Landscaping is a Landsdale based operator specialising in tight-access earthmoving, landscaping and site preparation for residential jobs.",
        "band_headline": "Need a bobcat this week?",
        "band_text": "Call 0412 776 377 for a quote and availability.",
        "gallery_captions": ["Site preparation", "Tight access digs", "Landscaping", "Northern suburbs"],
        "source": "https://www.facebook.com/search/top?q=tiny%20bobcat%20landscaping%20perth",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Phone only. Listed on Pink Pages.",
        "services": [
            {"title": "Bobcat hire", "desc": "Tight-access earthmoving and levelling."},
            {"title": "Site preparation", "desc": "Clearing, trenching and prep for paving or turf."},
            {"title": "Landscaping", "desc": "Residential makeovers and clean-ups."},
            {"title": "Rubbish removal", "desc": "Green waste and site tidy-ups."},
        ],
    },
    {
        "slug": "satay-kings-perth",
        "name": "Satay Kings",
        "logo_text": "SATAY",
        "industry": "Malaysian Food Truck",
        "city": "Perth",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Malaysian street food truck, Perth",
        "phone_raw": "+61415819868",
        "phone_display": "0415 819 868",
        "address": "Perth, WA",
        "service_area": "Perth metro markets and events",
        "years": 5,
        "rating": "5.0",
        "hero_headline": "Real Malaysian satay on wheels.",
        "hero_subhead": "Satay Kings serves charcoal satay, curry puffs and Malaysian favourites at markets and events across Perth.",
        "about_headline": "Family recipes. Bold flavour.",
        "about": "Satay Kings is a Perth food truck built on authentic Malaysian street food. Follow their Facebook for weekly locations and catering enquiries.",
        "band_headline": "Feeding a crowd?",
        "band_text": "Call 0415 819 868 or message on Facebook for event catering.",
        "gallery_captions": ["Charcoal satay", "Curry puffs", "Market service", "Perth events"],
        "source": "https://www.facebook.com/sataykingswa",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone. No standalone website.",
        "services": [
            {"title": "Satay chicken and beef", "desc": "Charcoal grilled with peanut sauce."},
            {"title": "Curry puffs and sides", "desc": "Samosas, spring rolls and Malaysian favourites."},
            {"title": "Event catering", "desc": "Markets, festivals and private bookings."},
            {"title": "Takeaway", "desc": "Check Facebook for pop-up locations."},
        ],
    },
    {
        "slug": "big-5-curry-den",
        "name": "Big 5 Curry Den",
        "logo_text": "BIG 5",
        "industry": "South African Food Truck",
        "city": "Burns Beach",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "South African curries and bunny chow",
        "phone_raw": "+61402214522",
        "phone_display": "0402 214 522",
        "address": "Burns Beach, WA",
        "service_area": "Perth metro events and catering",
        "years": 8,
        "rating": "5.0",
        "hero_headline": "Authentic South African street food.",
        "hero_subhead": "Big 5 Curry Den brings bunny chow, curries and samoosas to Perth markets and private events.",
        "about_headline": "Halal friendly. Big flavour.",
        "about": "Big 5 Curry Den is a Perth catering and food truck operator specialising in Durban-style curries, bunny chow and South African street food for festivals and private hire.",
        "band_headline": "Catering an event?",
        "band_text": "Call 0402 214 522 or message on Facebook for menus and quotes.",
        "gallery_captions": ["Bunny chow", "Lamb curry", "Market service", "Perth catering"],
        "source": "https://www.facebook.com/big5curryden",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone only.",
        "services": [
            {"title": "Bunny chow", "desc": "Durban favourite with curry fillings."},
            {"title": "Curries", "desc": "Chicken, lamb and vegan options."},
            {"title": "Samoosas and sides", "desc": "Indian sweetmeats and mango lassi."},
            {"title": "Event hire", "desc": "Festivals, fairs and private functions."},
        ],
    },
    {
        "slug": "honeybee-cupcakes",
        "name": "HoneyBee Cupcakes",
        "logo_text": "HONEY",
        "industry": "Cupcakes and Cakes",
        "city": "Treeby",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Designer cupcakes, southern suburbs",
        "phone_raw": "+61424508229",
        "phone_display": "0424 508 229",
        "address": "Treeby, WA 6164",
        "service_area": "Treeby, Cockburn and Perth metro",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Cupcakes for every celebration.",
        "hero_subhead": "HoneyBee Cupcakes creates designer cupcakes and custom cakes for birthdays, weddings and events in Perth's south.",
        "about_headline": "Pretty. Delicious. Local.",
        "about": "HoneyBee Cupcakes is a home-based bakery in Treeby serving the southern suburbs with custom cupcake and cake orders.",
        "band_headline": "Need cupcakes this weekend?",
        "band_text": "Call or WhatsApp 0424 508 229 with your date and design ideas.",
        "gallery_captions": ["Designer cupcakes", "Wedding towers", "Kids parties", "Southern suburbs"],
        "source": "https://www.facebook.com/search/top?q=honeybee%20cupcakes%20perth",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Phone and WhatsApp. Facebook enquiries.",
        "services": [
            {"title": "Designer cupcakes", "desc": "Custom colours, toppers and themes."},
            {"title": "Celebration cakes", "desc": "Birthdays, weddings and milestones."},
            {"title": "Corporate orders", "desc": "Branded cupcakes for events."},
            {"title": "Delivery", "desc": "Southern suburbs delivery by arrangement."},
        ],
    },
    {
        "slug": "cupcakes-by-sharona",
        "name": "Cupcakes By Sharona",
        "logo_text": "SHARONA",
        "industry": "Cupcakes and Baking",
        "city": "Coogee",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Cupcakes and baking, Coogee",
        "phone_raw": "+61894942159",
        "phone_display": "(08) 9494 2159",
        "address": "Amity Boulevard, Coogee WA 6166",
        "service_area": "Coogee, southern suburbs and Perth metro",
        "years": 15,
        "rating": "4.9",
        "hero_headline": "Coogee cupcakes done properly.",
        "hero_subhead": "Cupcakes By Sharona on Amity Boulevard serves the southern suburbs with custom cupcakes and baking orders.",
        "about_headline": "Local baker. Repeat customers.",
        "about": "Cupcakes By Sharona is a long-running Coogee bakery known locally for cupcakes, celebration cakes and special occasion orders.",
        "band_headline": "Celebration coming up?",
        "band_text": "Call (08) 9494 2159 to discuss flavours and pickup times.",
        "gallery_captions": ["Custom cupcakes", "Celebration cakes", "Coogee orders", "Southern suburbs"],
        "source": "https://www.facebook.com/search/top?q=cupcakes%20by%20sharona%20coogee",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Phone and Facebook. No website.",
        "services": [
            {"title": "Cupcakes", "desc": "Custom flavours and designs."},
            {"title": "Celebration cakes", "desc": "Birthdays, weddings and events."},
            {"title": "Wholesale", "desc": "Orders for cafes and events."},
            {"title": "Pickup", "desc": "Coogee collection by arrangement."},
        ],
    },
    {
        "slug": "the-barber-queen-mobile",
        "name": "The Barber Queen Mobile Barber",
        "logo_text": "QUEEN",
        "industry": "Mobile Barber",
        "city": "Thornlie",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Mobile barber, Perth metro",
        "phone_raw": "+61400000037",
        "phone_display": "Book via Facebook",
        "address": "Thornlie, WA 6108",
        "service_area": "Thornlie, Perth metro, aged care and schools",
        "years": 4,
        "rating": "5.0",
        "hero_headline": "The barbershop comes to you.",
        "hero_subhead": "The Barber Queen brings patient, professional cuts to homes, workplaces, hospitals and aged care across Perth.",
        "about_headline": "Inclusive. Mobile. Skilled.",
        "about": "The Barber Queen Mobile Barber specialises in fades, kids cuts and disability-friendly appointments at your location across Perth.",
        "band_headline": "Need a mobile barber?",
        "band_text": "Message on Facebook or book through HeyGoldie to lock in a time.",
        "gallery_captions": ["Mobile fades", "Kids cuts", "Aged care visits", "Thornlie based"],
        "source": "https://www.facebook.com/thebarberqueenmobilebarber",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook Messenger and HeyGoldie booking. No website.",
        "services": [
            {"title": "Mobile haircuts", "desc": "Fades, tapers and scissor cuts at your door."},
            {"title": "Kids cuts", "desc": "Patient service for children and NDIS clients."},
            {"title": "Aged care visits", "desc": "Cuts at homes, hospitals and facilities."},
            {"title": "Creative styles", "desc": "Designs, braids and special occasion looks."},
        ],
    },
    {
        "slug": "simon-says-burger",
        "name": "Simon Says Burger",
        "logo_text": "SIMON",
        "industry": "Food Truck and Takeaway",
        "city": "Midvale",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "BBQ burgers and Malaysian truck, Midvale",
        "phone_raw": "+61414174666",
        "phone_display": "0414 174 666",
        "address": "227 Morrison Road, Midvale WA 6056",
        "service_area": "Midvale, Morley and Perth metro",
        "years": 7,
        "rating": "4.9",
        "hero_headline": "Smoke, spice and stacked burgers.",
        "hero_subhead": "Chef Simon runs a Midvale shop and roaming food truck with BBQ burgers, birria tacos and Malaysian specials.",
        "about_headline": "Halal friendly. Big personality.",
        "about": "Simon Says Burger is a Midvale based food business with a shopfront and truck serving bold BBQ, burgers and fusion street food across Perth.",
        "band_headline": "Truck location today?",
        "band_text": "Call 0414 174 666 or check Facebook for the truck schedule.",
        "gallery_captions": ["BBQ burgers", "Birria tacos", "Truck specials", "Midvale shop"],
        "source": "https://www.facebook.com/search/top?q=simon%20says%20burger%20perth",
        "instagram": "https://www.instagram.com/simonsaysburger/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook, Instagram and phone. No standalone website.",
        "services": [
            {"title": "BBQ burgers", "desc": "Stacked beef burgers with smoke and char."},
            {"title": "Food truck", "desc": "Rolling menu at markets and Morley pop-ups."},
            {"title": "Catering", "desc": "Packages from $15 per person."},
            {"title": "Midvale shop", "desc": "Shop 7, 227 Morrison Road for lunch specials."},
        ],
    },
    {
        "slug": "thats-delish",
        "name": "That's Delish",
        "logo_text": "DELISH",
        "industry": "Custom Cakes and Cupcakes",
        "city": "Yangebup",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Wedding cakes and cupcakes, Yangebup",
        "phone_raw": "+61400601071",
        "phone_display": "0400 601 071",
        "email": "lisagliddon@bigpond.com",
        "address": "Yangebup, WA 6164",
        "service_area": "Yangebup, Kwinana and Perth metro",
        "years": 12,
        "rating": "5.0",
        "hero_headline": "Cakes that look and taste amazing.",
        "hero_subhead": "Lisa at That's Delish creates wedding cakes, corporate cupcakes and gluten-free options from Yangebup.",
        "about_headline": "Easy to deal with. Custom work.",
        "about": "That's Delish is a Yangebup based custom cake studio specialising in weddings, corporate branding and celebration cupcakes with gluten-free and vegan options.",
        "band_headline": "Engaged or corporate event?",
        "band_text": "Call 0400 601 071 or message on Facebook for a tasting or quote.",
        "gallery_captions": ["Wedding cakes", "Corporate cupcakes", "Gluten-free options", "Yangebup studio"],
        "source": "https://www.facebook.com/thatsdelish",
        "has_website": False,
        "website_note": "thatsdelishperth.com unreachable. FB and phone primary.",
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone. Dead/unreachable domain.",
        "services": [
            {"title": "Wedding cakes", "desc": "Custom designs with tasting appointments."},
            {"title": "Corporate cupcakes", "desc": "Edible logo cookies and cupcake towers."},
            {"title": "Celebration cakes", "desc": "Birthdays, baby showers and events."},
            {"title": "Dietary options", "desc": "Gluten-free and vegan on request."},
        ],
    },
    {
        "slug": "blabs-mobile-dog-grooming",
        "name": "B.L.A.B's Mobile Dog Grooming",
        "logo_text": "BLAB",
        "industry": "Mobile Dog Grooming",
        "city": "Perth",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "Mobile dog grooming, Perth metro",
        "phone_raw": "+61477071021",
        "phone_display": "0477 071 021",
        "address": "Perth, WA",
        "service_area": "Perth metro and surrounds",
        "years": 5,
        "rating": "5.0",
        "hero_headline": "Gentle grooms at your doorstep.",
        "hero_subhead": "B.L.A.B's brings a fully equipped mobile van to your home for baths, tidies and full grooms.",
        "about_headline": "Stress-free. Stylish.",
        "about": "B.L.A.B's Mobile Dog Grooming services Perth metro with one-on-one care in a mobile salon van for all breeds.",
        "band_headline": "First groom or regular slot?",
        "band_text": "Call or WhatsApp 0477 071 021 to book.",
        "gallery_captions": ["Full grooms", "Bath and tidy", "Puppy introductions", "Mobile van"],
        "source": "https://www.facebook.com/search/top?q=blabs%20mobile%20grooming%20perth",
        "has_website": False,
        "website_note": "Simple Netlify page only. Pitch proper site.",
        "demo_flag": "outreach",
        "contact_note": "Phone, WhatsApp and Facebook.",
        "services": [
            {"title": "Full grooms", "desc": "Wash, dry, clip and style at your home."},
            {"title": "Bath and tidy", "desc": "Nail clip and light trim between grooms."},
            {"title": "De-shed treatments", "desc": "Deep coat care for shedding breeds."},
            {"title": "Puppy introductions", "desc": "Gentle first visits for young dogs."},
        ],
    },
    {
        "slug": "celestes-dog-grooming",
        "name": "Celeste's Dog Grooming",
        "logo_text": "CEL",
        "industry": "Dog Grooming",
        "city": "Perth",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "Dog grooming salon, Perth",
        "phone_raw": "+61433007934",
        "phone_display": "0433 007 934",
        "address": "Grevillea Place, Perth WA 6155",
        "service_area": "Southern suburbs and Perth metro",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Calm grooms for every breed.",
        "hero_subhead": "Celeste's Dog Grooming on Grevillea Place offers full grooms, baths and breed-specific styling.",
        "about_headline": "One-on-one care.",
        "about": "Celeste's Dog Grooming is a Perth salon focused on gentle handling and quality clips for dogs of all sizes.",
        "band_headline": "Book your groom?",
        "band_text": "Call 0433 007 934 or message on Facebook.",
        "gallery_captions": ["Full grooms", "Breed clips", "Bath and blow-dry", "Perth salon"],
        "source": "https://www.facebook.com/search/top?q=celeste%27s%20dog%20grooming%20perth",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Phone and Facebook only.",
        "services": [
            {"title": "Full grooms", "desc": "Wash, dry, clip and style."},
            {"title": "Bath and tidy", "desc": "Quick freshen-ups between full grooms."},
            {"title": "Nail trims", "desc": "Nails and basic hygiene."},
            {"title": "Breed styling", "desc": "Clips matched to coat type."},
        ],
    },
    {
        "slug": "rubys-bakehouse",
        "name": "Ruby's Bakehouse",
        "logo_text": "RUBY",
        "industry": "Bakery and Cafe",
        "city": "Leeming",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Bakery and coffee, Leeming",
        "phone_raw": "+61488414732",
        "phone_display": "0488 414 732",
        "address": "1 Dundee Street, Leeming WA 6149",
        "service_area": "Leeming, Melville and southern suburbs",
        "hours": "Mon-Sat 7am-2pm",
        "years": 10,
        "rating": "4.7",
        "hero_headline": "Fresh bake. Local favourite.",
        "hero_subhead": "Ruby's Bakehouse on Dundee Street serves coffee, cakes and cabinet favourites six days a week.",
        "about_headline": "Neighbourhood bakery.",
        "about": "Ruby's Bakehouse is a Leeming bakery and cafe known locally for fresh bakes, coffee and friendly counter service.",
        "band_headline": "Celebration cake needed?",
        "band_text": "Call 0488 414 732 or message on Instagram to order ahead.",
        "gallery_captions": ["Fresh pastries", "Celebration cakes", "Coffee and cabinet", "Leeming local"],
        "source": "https://www.instagram.com/rubys_bakehouse/",
        "instagram": "https://www.instagram.com/rubys_bakehouse/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Instagram and phone. No proper website.",
        "services": [
            {"title": "Fresh baking", "desc": "Daily pastries, pies and sweets."},
            {"title": "Coffee and cabinet", "desc": "Sit-in and takeaway from 7am."},
            {"title": "Celebration cakes", "desc": "Custom orders by phone or DM."},
            {"title": "Local pickup", "desc": "1 Dundee Street, Leeming."},
        ],
    },
    {
        "slug": "cupcakes-with-love",
        "name": "Cupcakes with Love",
        "logo_text": "LOVE",
        "industry": "Cupcakes and Flowers",
        "city": "Yangebup",
        "image_set": "cafe",
        "theme": "cafe",
        "tagline": "Cupcakes and occasion treats, Yangebup",
        "phone_raw": "+61402299202",
        "phone_display": "0402 299 202",
        "address": "Yangebup, WA 6163",
        "service_area": "Yangebup, Cockburn and Perth south",
        "years": 8,
        "rating": "5.0",
        "hero_headline": "Sweet treats for every occasion.",
        "hero_subhead": "Cupcakes with Love is a home-based Yangebup business doing custom cupcakes and occasion orders.",
        "about_headline": "Home based. Personal touch.",
        "about": "Cupcakes with Love creates custom cupcakes and celebration treats from a home kitchen in Yangebup for local families and events.",
        "band_headline": "Party this weekend?",
        "band_text": "Call or WhatsApp 0402 299 202 to order.",
        "gallery_captions": ["Custom cupcakes", "Occasion boxes", "Kids parties", "Yangebup orders"],
        "source": "https://www.facebook.com/search/top?q=cupcakes%20with%20love%20yangebup",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Phone and WhatsApp. Facebook enquiries.",
        "services": [
            {"title": "Custom cupcakes", "desc": "Vanilla, chocolate and themed designs."},
            {"title": "Occasion orders", "desc": "Birthdays, baby showers and events."},
            {"title": "Gift boxes", "desc": "Cupcake gift sets for delivery."},
            {"title": "Local pickup", "desc": "Yangebup collection by arrangement."},
        ],
    },
]


def is_real_mobile(lead: dict) -> bool:
    raw = lead.get("phone_raw", "")
    if not raw.startswith("+614"):
        return False
    if raw.startswith("+614000000"):
        return False
    return True


def primary_channel(lead: dict) -> str:
    if is_real_mobile(lead):
        return "WhatsApp"
    if lead.get("instagram"):
        return "Instagram"
    if "facebook.com" in lead.get("source", "") and "search" not in lead.get("source", ""):
        return "Facebook"
    return "Email"


def wa_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    return f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: WhatsApp
MOBILE: {lead.get('phone_display', '')} ({lead.get('phone_raw', '')})
DEMO: {DEMO_BASE}/{slug}/

Hi, quick one from Edison at Caisson (web dev in Perth).

I came across {name} around {city}. You're doing great work but don't have a proper website when locals search Google.

Built a free preview:
{DEMO_BASE}/{slug}/ 

$180 one-off (Basic: mobile site, contact form, deployment) if you want it live. Medium is $250 if you want basic support, Google indexing and your own domain. Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this locked in. No stress if not for you.

Cheers,
Edison · Caisson · Perth
"""


def fb_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    return f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: Facebook Messenger
PAGE: {lead.get('source', '')}
DEMO: {DEMO_BASE}/{slug}/

Hi, quick one from Edison at Caisson (web dev in Perth).

I found {name} on Facebook. Good work around {city} but no proper website when locals search Google.

Built a free preview:
{DEMO_BASE}/{slug}/ 

$180 one-off (Basic: mobile site, contact form, deployment) if you want it live. Medium is $250 if you want basic support, Google indexing and your own domain. Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this locked in. No stress if not for you.

Cheers,
Edison · Caisson · Perth
"""


def ig_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    ig = lead.get("instagram", lead.get("source", ""))
    return f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: Instagram DM
PROFILE: {ig}
DEMO: {DEMO_BASE}/{slug}/

Hi, quick one. I'm Edison from Caisson (web dev in Perth).

I came across {name} on Instagram. You're doing solid work in {city} but don't have a proper website when people search near me.

Built a free preview:
{DEMO_BASE}/{slug}/ 

$180 one-off (Basic: mobile site, contact form, deployment) if you want it live. Medium is $250 if you want basic support, Google indexing and your own domain. Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this one locked in. No stress if not for you.

Cheers,
Edison · Caisson · Perth
"""


def main() -> None:
    existing = json.loads(TARGETS.read_text(encoding="utf-8"))
    slugs = {l["slug"] for l in existing}
    added = []
    for lead in NEW_LEADS:
        if lead["slug"] in slugs:
            print(f"SKIP duplicate: {lead['slug']}")
            continue
        existing.append(lead)
        added.append(lead)
        slugs.add(lead["slug"])

    TARGETS.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    print(f"Added {len(added)} leads to targets.json")

    wa_count = 0
    for lead in added:
        slug = lead["slug"]
        ch = primary_channel(lead)
        if is_real_mobile(lead):
            (OUTREACH / f"wa-{slug}.txt").write_text(wa_draft(lead), encoding="utf-8")
            wa_count += 1
            print(f"Draft: wa-{slug}.txt")
        if lead.get("instagram"):
            (OUTREACH / f"ig-{slug}.txt").write_text(ig_draft(lead), encoding="utf-8")
            print(f"Draft: ig-{slug}.txt")
        elif ch == "Facebook" or "facebook.com" in lead.get("source", ""):
            (OUTREACH / f"fb-{slug}.txt").write_text(fb_draft(lead), encoding="utf-8")
            print(f"Draft: fb-{slug}.txt")

    slugs_file = ROOT / "leads" / "burst70_slugs.txt"
    slugs_file.write_text("\n".join(l["slug"] for l in added), encoding="utf-8")
    print(f"WA drafts: {wa_count} | Slugs: {slugs_file}")


if __name__ == "__main__":
    main()
