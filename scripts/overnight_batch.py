#!/usr/bin/env python3
"""Overnight batch: add 25 WA leads, outreach drafts, REVIEW-INDEX rows."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ROOT / "leads" / "targets.json"
OUTREACH = ROOT / "outreach"
REVIEW = OUTREACH / "REVIEW-INDEX.md"

MEDIUM = {
    "halo-lashes", "flick-and-flutter-lash", "kikididit", "studio-eire", "lilly-c-nails",
    "sash-hair-studio", "a-blended-place", "lisas-mane-studio", "prep-perth", "juicy-beauty",
    "belashed-by-km", "md-beauty-studio", "white-feather-beauty", "tay-luxe-studio",
    "gelato-nails-subiaco",
}

NEW_LEADS = [
    {
        "slug": "halo-lashes",
        "name": "Halo Lashes",
        "logo_text": "HALO",
        "industry": "Lash Extensions",
        "city": "Tuart Hill",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Affordable lash studio, Tuart Hill",
        "phone_raw": "+61400000012",
        "phone_display": "Book via Fresha",
        "address": "U1, 124 Tyler Street, Tuart Hill WA 6060",
        "service_area": "Tuart Hill, Osborne Park and Perth north",
        "years": 3,
        "rating": "5.0",
        "hero_headline": "Lashes that lift your confidence.",
        "hero_subhead": "Home-based lash studio in Tuart Hill. Classic, hybrid and volume sets in a cozy, insured salon.",
        "about_headline": "Trained, qualified and insured.",
        "about": "Halo Lashes is a home-based studio in Tuart Hill focused on affordable lash treatments. Every visit is one-on-one with time taken to match the style you want.",
        "band_headline": "New set or refill?",
        "band_text": "Book through Fresha for a full set, refill or lash lift bundle.",
        "gallery_captions": ["Classic lash extensions", "Hybrid and volume sets", "Lash lift and tint", "Home studio in Tuart Hill"],
        "source": "https://www.fresha.com/a/halo-lashes-tuart-hill-u1-124-tyler-street-zjipxyq2",
        "instagram": "https://www.instagram.com/halo.lashes.perth/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha booking only. No standalone website.",
        "services": [
            {"title": "Classic lashes", "desc": "Natural-looking extensions applied lash by lash."},
            {"title": "Hybrid and volume", "desc": "Fuller sets for everyday wear or events."},
            {"title": "Lash refills", "desc": "Keep your set fresh every two to three weeks."},
            {"title": "Brow services", "desc": "Wax, tint and shaping to frame your face."},
        ],
    },
    {
        "slug": "flick-and-flutter-lash",
        "name": "Flick and Flutter Lash",
        "logo_text": "FLUTTER",
        "industry": "Lash Extensions",
        "city": "Treeby",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Home lash studio, Treeby",
        "phone_raw": "+61400000013",
        "phone_display": "Book via Fresha",
        "address": "95 Turquoise Boulevard, Treeby WA 6164",
        "service_area": "Treeby, Cockburn and southern suburbs",
        "years": 2,
        "rating": "5.0",
        "hero_headline": "Signature lashes for every occasion.",
        "hero_subhead": "Ella runs a home studio in Treeby. Classic to volume sets tailored to your eye shape and lifestyle.",
        "about_headline": "Quality lashes. Calm appointments.",
        "about": "Flick and Flutter Lash is a home-based studio in Treeby using medical-grade glue and premium lashes. Every appointment is private and unhurried.",
        "band_headline": "Special event coming up?",
        "band_text": "Book a full set or infill through Fresha. Message if you need help choosing a style.",
        "gallery_captions": ["Volume lash sets", "Classic extensions", "Lash lift and tint", "Home studio in Treeby"],
        "source": "https://www.fresha.com/a/flick-and-flutter-lash-treeby-95-turquoise-boulevard-j4f8b0r9",
        "instagram": "https://www.instagram.com/flickandflutterlash/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only. No website.",
        "services": [
            {"title": "Classic lashes", "desc": "Natural extensions tailored to your eye shape."},
            {"title": "Volume sets", "desc": "3D to 5D volume for fuller everyday looks."},
            {"title": "Lash infills", "desc": "Maintain your set every two to three weeks."},
            {"title": "Lash lift and tint", "desc": "Low-maintenance lift with brow lamination add-ons."},
        ],
    },
    {
        "slug": "kikididit",
        "name": "Kikididit",
        "logo_text": "KIKI",
        "industry": "Lash and Brow",
        "city": "Banksia Grove",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Home beauty studio, Banksia Grove",
        "phone_raw": "+61400000014",
        "phone_display": "Book via Fresha",
        "address": "56 Fishbone Turn, Banksia Grove WA 6031",
        "service_area": "Banksia Grove, Joondalup and northern suburbs",
        "years": 2,
        "rating": "5.0",
        "hero_headline": "Lashes and brows, effortlessly stunning.",
        "hero_subhead": "Home studio in Banksia Grove. Lash lifts, extensions and brow tinting in a relaxed one-on-one space.",
        "about_headline": "Customised to your features.",
        "about": "Kikididit is a home-based beauty studio in Perth's north specialising in lash lifts, extensions and brow tinting with quality products and precise technique.",
        "band_headline": "First visit?",
        "band_text": "Book on Fresha or DM on Instagram to find a time that suits.",
        "gallery_captions": ["Lash lift treatments", "Lash extensions", "Brow tint and wax", "Home studio Banksia Grove"],
        "source": "https://www.fresha.com/a/kikididit-banksia-grove-56-fishbone-turn-kdtox2ih",
        "instagram": "https://www.instagram.com/kikididit/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha and Instagram only.",
        "services": [
            {"title": "Lash lifts", "desc": "Lift and tint for wide-awake, low-maintenance lashes."},
            {"title": "Lash extensions", "desc": "Classic and volume sets applied lash by lash."},
            {"title": "Brow tint", "desc": "Defined brows matched to your hair colour."},
            {"title": "Combo treatments", "desc": "Lash and brow packages for special occasions."},
        ],
    },
    {
        "slug": "studio-eire",
        "name": "Studio Eire",
        "logo_text": "EIRE",
        "industry": "Nails and Lashes",
        "city": "Sinagra",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "BIAB nails and lashes, Sinagra",
        "phone_raw": "+61400000015",
        "phone_display": "Book via Fresha",
        "address": "17 Giglia Drive, Sinagra WA 6065",
        "service_area": "Sinagra, Wanneroo and Perth north-east",
        "years": 3,
        "rating": "5.0",
        "hero_headline": "Natural nails, lashes and brows.",
        "hero_subhead": "Home beauty studio in Sinagra. BIAB nails, lash lifts and brow sculpting in a calm private space.",
        "about_headline": "Premium products. One-on-one care.",
        "about": "Studio Eire is a home-based studio in Sinagra offering BIAB nails, lash lifts and brow treatments with attention to detail and a relaxing atmosphere.",
        "band_headline": "New set or refill?",
        "band_text": "Book through Fresha. Address confirmed when you book.",
        "gallery_captions": ["BIAB nail sets", "Lash lift treatments", "Brow sculpting", "Home studio Sinagra"],
        "source": "https://www.fresha.com/a/studio-eire-sinagra-17-giglia-drive-uafm6gxt",
        "instagram": "https://www.instagram.com/studio.eire/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only. No website.",
        "services": [
            {"title": "BIAB nails", "desc": "Structured builder gel overlays and refills."},
            {"title": "Lash lifts", "desc": "Lift and tint for natural, wide-awake lashes."},
            {"title": "Brow treatments", "desc": "Sculpting, tint and lamination for defined brows."},
            {"title": "Nail art", "desc": "Minimal or detailed designs on BIAB sets."},
        ],
    },
    {
        "slug": "lilly-c-nails",
        "name": "Lilly c nails",
        "logo_text": "LILLY",
        "industry": "Nails and Lashes",
        "city": "Yokine",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "BIAB nails and Korean lash lifts, Yokine",
        "phone_raw": "+61400000016",
        "phone_display": "Book via Fresha",
        "address": "4b Cabell Street, Yokine WA 6060",
        "service_area": "Yokine, Mount Lawley and Perth inner north",
        "years": 4,
        "rating": "5.0",
        "hero_headline": "At-home salon comfort. Pro results.",
        "hero_subhead": "Home salon in Yokine. BIAB nails and Korean lash lifts in a personalised, relaxed setting.",
        "about_headline": "Sit back. Leave polished.",
        "about": "Lilly c nails offers BIAB manicures and Korean lash lifts from a home salon in Yokine. Every appointment is tailored with professional products and careful prep.",
        "band_headline": "Nails or lashes?",
        "band_text": "Book on Fresha for BIAB sets, infills or lash lift appointments.",
        "gallery_captions": ["BIAB nail sets", "Korean lash lifts", "Nail art finishes", "Home salon Yokine"],
        "source": "https://www.fresha.com/en-GB/a/lilly-c-nails-yokine-4b-cabell-street-hd5zw5cy",
        "instagram": "https://www.instagram.com/lillycnails/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "BIAB nails", "desc": "Structured builder gel with proper prep and finish."},
            {"title": "Korean lash lift", "desc": "Lift and tint for a wide-awake natural look."},
            {"title": "BIAB infills", "desc": "Keep your set fresh every two to three weeks."},
            {"title": "Removals", "desc": "Safe soak-offs before your next set."},
        ],
    },
    {
        "slug": "fluffy-dog-grooming",
        "name": "Fluffy Dog Grooming",
        "logo_text": "FLUFFY",
        "industry": "Dog Grooming",
        "city": "Oakford",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "Dog grooming, Oakford",
        "phone_raw": "+61400000017",
        "phone_display": "Book via Fresha",
        "address": "7 Lakeman Place, Oakford WA 6121",
        "service_area": "Oakford, Serpentine and Perth south-east",
        "years": 8,
        "rating": "5.0",
        "hero_headline": "Pampering for small and medium dogs.",
        "hero_subhead": "Rural Oakford grooming salon. Full grooms, breed clips and one-on-one care for dogs up to medium size.",
        "about_headline": "Tail-wagging transformations.",
        "about": "Fluffy Dog Grooming in Oakford offers full grooms, bath and tidy packages and breed-standard clips in a calm, one-on-one setting.",
        "band_headline": "First groom or regular slot?",
        "band_text": "Book through Fresha. Tell us your dog's breed and coat type when you book.",
        "gallery_captions": ["Full grooms", "Bath and tidy", "Breed-standard clips", "Oakford salon"],
        "source": "https://www.fresha.com/a/fluffy-dog-grooming-oakford-7-lakeman-place-w9zvch94",
        "instagram": "https://www.instagram.com/fluffydoggrooming/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha booking. No website.",
        "services": [
            {"title": "Full grooms", "desc": "Wash, dry, clip and style for small and medium dogs."},
            {"title": "Bath and blow-dry", "desc": "Quick freshen-ups between full grooms."},
            {"title": "Breed clips", "desc": "Schnauzer, bichon, poodle and cavoodle styling."},
            {"title": "Puppy introductions", "desc": "Gentle first visits for young dogs."},
        ],
    },
    {
        "slug": "pampered-with-love-pet",
        "name": "Pampered with Love Pet Grooming and Spa",
        "logo_text": "PAMPERED",
        "industry": "Dog Grooming",
        "city": "Attadale",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "One-on-one dog grooming, Attadale",
        "phone_raw": "+61400000018",
        "phone_display": "Book via Fresha",
        "address": "Attadale Reserve, Burke Drive, Attadale WA 6156",
        "service_area": "Attadale, Melville and Perth south",
        "years": 5,
        "rating": "5.0",
        "hero_headline": "Grooming with love and attention.",
        "hero_subhead": "Attadale pet spa offering one-on-one grooms, puppy introductions and styled clips in a stress-free environment.",
        "about_headline": "Every pet is unique.",
        "about": "Pampered with Love Pet Grooming and Spa handles each dog individually in Attadale. From nail trims to full styled grooms, your pet gets full focus and gentle care.",
        "band_headline": "New puppy or regular groom?",
        "band_text": "Book on Fresha. Let us know your pet's breed and any sensitivities.",
        "gallery_captions": ["Styled full grooms", "Puppy introductions", "Bath and tidy", "Attadale pet spa"],
        "source": "https://www.fresha.com/a/pampered-with-love-pet-grooming-and-spa-attadale-attadale-reserve-burke-drive-qln7spqc",
        "instagram": "https://www.instagram.com/pamperedwithlovepetgrooming/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Full styled grooms", "desc": "Scissored heads, teddy bear clips and breed trims."},
            {"title": "Puppy introductions", "desc": "Gentle first grooms for 10 to 18 week puppies."},
            {"title": "Bath and blow-dry", "desc": "Quick freshen-ups between full grooms."},
            {"title": "Nail and hygiene", "desc": "Nail trims and hygiene tidies."},
        ],
    },
    {
        "slug": "pimp-my-paws",
        "name": "Pimp My Paws",
        "logo_text": "PMP",
        "industry": "Pet Grooming and Spa",
        "city": "Rockingham",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "Pet spa and grooming, Rockingham",
        "phone_raw": "+61400000019",
        "phone_display": "Book via Fresha",
        "address": "54 Andromeda Street, Rockingham WA 6168",
        "service_area": "Rockingham, Safety Bay and southern suburbs",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Spa day for your best mate.",
        "hero_subhead": "Rockingham pet spa with grooming, styling and wellness treatments using organic, eco-friendly products.",
        "about_headline": "Royal treatment. Local care.",
        "about": "Pimp My Paws Spa and Pet Services in Rockingham offers precision haircuts, blow dries and pampering packages in a warm, pet-friendly salon.",
        "band_headline": "Groom or spa package?",
        "band_text": "Book through Fresha for grooming, styling or spa add-ons.",
        "gallery_captions": ["Grooming and styling", "Spa treatments", "Pet wedding assist", "Rockingham salon"],
        "source": "https://www.fresha.com/a/pimp-my-paws-rockingham-54-andromeda-street-ohonlzpo",
        "instagram": "https://www.instagram.com/pimpmypaws/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha booking only.",
        "services": [
            {"title": "Grooming and styling", "desc": "Precision cuts and blow dries for all coat types."},
            {"title": "Spa and pampering", "desc": "Baths, treatments and wellness add-ons."},
            {"title": "Pet wedding assist", "desc": "Special occasion styling for your furry guest."},
            {"title": "Health and wellness", "desc": "Coat and skin care with organic products."},
        ],
    },
    {
        "slug": "sash-hair-studio",
        "name": "SASH hair studio",
        "logo_text": "SASH",
        "industry": "Hair Salon",
        "city": "Duncraig",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Private home hair studio, Duncraig",
        "phone_raw": "+61400000020",
        "phone_display": "Book via Fresha",
        "address": "23 Elderslie Way, Duncraig WA 6023",
        "service_area": "Duncraig, Joondalup and northern suburbs",
        "years": 5,
        "rating": "5.0",
        "hero_headline": "Hair with one-on-one attention.",
        "hero_subhead": "Private home studio in Duncraig. Cuts, colour and styling in a calm, welcoming space.",
        "about_headline": "Your appointment. Your time.",
        "about": "SASH hair studio is a home-based salon in Duncraig where every client gets full focus. Colour, cuts and styling tailored to you.",
        "band_headline": "Colour refresh or new cut?",
        "band_text": "Book on Fresha for your next appointment.",
        "gallery_captions": ["Colour and styling", "Cuts and blow dries", "Private studio", "Duncraig home salon"],
        "source": "https://www.fresha.com/a/sash-hair-studio-duncraig-23-elderslie-way-fs4a7ia7",
        "instagram": "https://www.instagram.com/sash.hairstudio/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Cuts and styling", "desc": "Restyles, trims and blow dries."},
            {"title": "Colour services", "desc": "Full colour, highlights and toners."},
            {"title": "Treatments", "desc": "Conditioning and repair treatments."},
            {"title": "Special occasions", "desc": "Event styling by appointment."},
        ],
    },
    {
        "slug": "a-blended-place",
        "name": "A Blended Place",
        "logo_text": "BLENDED",
        "industry": "Hair Salon",
        "city": "Beldon",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Home colour salon, Beldon",
        "phone_raw": "+61400000021",
        "phone_display": "Book via Fresha",
        "address": "Gradient Way, Beldon WA 6027",
        "service_area": "Beldon, Joondalup and northern suburbs",
        "years": 7,
        "rating": "5.0",
        "hero_headline": "Colour and cuts you deserve.",
        "hero_subhead": "Home studio in Beldon using Pravana, Keune and Olaplex. One-on-one colour, cutting and styling.",
        "about_headline": "Premium colour. Personal time.",
        "about": "A Blended Place is a home-based hair studio in Beldon designed for one-on-one appointments. Ladies colour, cutting and styling with top-range products.",
        "band_headline": "Root touch-up or full colour?",
        "band_text": "Book through Fresha. Address provided when you confirm.",
        "gallery_captions": ["Colour and highlights", "Cuts and styling", "Olaplex treatments", "Beldon home studio"],
        "source": "https://www.fresha.com/a/a-blended-place-beldon-gradient-way-39527rtk",
        "instagram": "https://www.instagram.com/ablendedplace/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Colour services", "desc": "Full colour, balayage and root touch-ups."},
            {"title": "Cuts and styling", "desc": "Restyles, trims and blow dries."},
            {"title": "Smoothing treatments", "desc": "EVY smoothing for frizz-free results."},
            {"title": "Olaplex care", "desc": "Bond-building treatments during colour."},
        ],
    },
    {
        "slug": "lisas-mane-studio",
        "name": "Lisa's Mane Studio",
        "logo_text": "MANE",
        "industry": "Hair Salon",
        "city": "Alkimos",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Boutique home salon, Alkimos",
        "phone_raw": "+61400000022",
        "phone_display": "Book via Fresha",
        "address": "1 Woodswallow Way, Alkimos WA 6038",
        "service_area": "Alkimos, Butler and Perth north",
        "years": 14,
        "rating": "5.0",
        "hero_headline": "Colour expertise. Personal studio.",
        "hero_subhead": "Lisa brings 14 years of salon experience to a boutique home studio in Alkimos. Blondes, roots and cuts with Wella colour.",
        "about_headline": "From Beaufort Street to your home suburb.",
        "about": "Lisa's Mane Studio is a home salon in Alkimos offering personalised colour, root touch-ups, blonde transformations and cutting in a one-on-one setting.",
        "band_headline": "Blonde refresh or new style?",
        "band_text": "Book on Fresha for colour, cut or both.",
        "gallery_captions": ["Blonde transformations", "Root touch-ups", "Cuts and styling", "Alkimos home salon"],
        "source": "https://www.fresha.com/en-GB/a/lisas-mane-studio-alkimos-1-woodswallow-way-sxw8vjh1",
        "instagram": "https://www.instagram.com/lisasmanestudio/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Colour services", "desc": "Full colour, roots and blonde transformations."},
            {"title": "Cuts and styling", "desc": "Restyles, trims and blow dries."},
            {"title": "Toning", "desc": "Gloss and toner refreshes between colours."},
            {"title": "Consultations", "desc": "Colour planning before big changes."},
        ],
    },
    {
        "slug": "prep-perth",
        "name": "Prep Perth",
        "logo_text": "PREP",
        "industry": "Skin and Beauty",
        "city": "Clarkson",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Skin, brows and lashes, Clarkson",
        "phone_raw": "+61400000023",
        "phone_display": "Book via Fresha",
        "address": "57 Makassar Way, Clarkson WA 6030",
        "service_area": "Clarkson, Mindarie and northern suburbs",
        "years": 4,
        "rating": "5.0",
        "hero_headline": "Skin and beauty that empowers.",
        "hero_subhead": "Kate runs Prep Perth, a home studio in Clarkson for brows, skin treatments and lash lifts.",
        "about_headline": "Dermal science. Natural results.",
        "about": "Prep Perth is a home-based skin, beauty and cosmetic tattoo studio in Clarkson. Brow treatments, skin facials and lash lifts with a focus on natural enhancement.",
        "band_headline": "Brows or skin first?",
        "band_text": "Book through Fresha for your next treatment.",
        "gallery_captions": ["Brow treatments", "Skin facials", "Lash lifts", "Clarkson home studio"],
        "source": "https://www.fresha.com/a/prep-perth-perth-57-makassar-way-xo91jmum",
        "instagram": "https://www.instagram.com/prepperth/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Brow treatments", "desc": "Shaping, tint and cosmetic tattoo options."},
            {"title": "Skin treatments", "desc": "Facials and dermal therapies by appointment."},
            {"title": "Lash lifts", "desc": "Lift and tint for natural lashes."},
            {"title": "Consultations", "desc": "Skin and brow planning before treatment."},
        ],
    },
    {
        "slug": "juicy-beauty",
        "name": "Juicy Beauty",
        "logo_text": "JUICY",
        "industry": "Brows and Lashes",
        "city": "Padbury",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Brow and lash studio, Padbury",
        "phone_raw": "+61400000024",
        "phone_display": "Book via Fresha",
        "address": "22 Durack Way, Padbury WA 6025",
        "service_area": "Padbury, Hillarys and northern suburbs",
        "years": 5,
        "rating": "5.0",
        "hero_headline": "Brows and lashes, expertly styled.",
        "hero_subhead": "Certified brow and lash stylist in Padbury. Lifts, tints and signature facials in a professional home studio.",
        "about_headline": "Personalised treatments. Real results.",
        "about": "Juicy Beauty is a home-based brow and lash studio in Padbury. Every service is tailored to enhance your natural features.",
        "band_headline": "Lift, tint or both?",
        "band_text": "Book on Fresha for brow and lash appointments.",
        "gallery_captions": ["Brow tint and design", "Lash lifts", "Signature facials", "Padbury home studio"],
        "source": "https://www.fresha.com/a/juicy-beauty-padbury-22-durack-way-pdistwhq",
        "instagram": "https://www.instagram.com/juicybeauty.perth/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Brow services", "desc": "Tint, design and lamination."},
            {"title": "Lash lifts", "desc": "Lift and tint for wide-awake lashes."},
            {"title": "Signature facial", "desc": "Rejuvenating facial treatments."},
            {"title": "Combo packages", "desc": "Brow and lash bundles."},
        ],
    },
    {
        "slug": "thp-auto-mobile",
        "name": "THP Auto Mobile Mechanic",
        "logo_text": "THP",
        "industry": "Mobile Mechanic",
        "city": "Alkimos",
        "image_set": "mechanic",
        "theme": "mechanic",
        "tagline": "Mobile mechanic, Perth north",
        "phone_raw": "+61457431340",
        "phone_display": "0457 431 340",
        "address": "Alkimos, WA 6038",
        "service_area": "Alkimos, Butler, Yanchep and northern suburbs",
        "years": 5,
        "rating": "5.0",
        "hero_headline": "We come to you. No workshop wait.",
        "hero_subhead": "Terence runs THP Auto across Perth's north. Logbook services, repairs and diagnostics at your home or workplace.",
        "about_headline": "Licensed mobile mechanic.",
        "about": "THP Auto Mobile Mechanic services Alkimos and surrounding northern suburbs. No drop-offs, no waiting rooms. We show up, sort it and go.",
        "band_headline": "Service due or something wrong?",
        "band_text": "Call or message on Facebook for a quote and same-week availability.",
        "gallery_captions": ["Logbook servicing", "Brake and engine work", "On-site diagnostics", "Northern suburbs callouts"],
        "source": "https://www.facebook.com/THPAutoMobileMechanic",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone only. No website.",
        "services": [
            {"title": "Logbook servicing", "desc": "Manufacturer-scheduled services at your location."},
            {"title": "Repairs", "desc": "Brakes, suspension, engine and general mechanical."},
            {"title": "Diagnostics", "desc": "Fault finding and warning light checks."},
            {"title": "Fleet and workplace", "desc": "Servicing at home, work or job sites."},
        ],
    },
    {
        "slug": "jds-pressure-cleaning",
        "name": "JDS Pressure Cleaning",
        "logo_text": "JDS",
        "industry": "Pressure Cleaning",
        "city": "Perth",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Pressure cleaning and resealing, Perth",
        "phone_raw": "+61400000025",
        "phone_display": "Message via Facebook",
        "address": "Perth, WA",
        "service_area": "Perth metro and surrounds",
        "years": 8,
        "rating": "5.0",
        "hero_headline": "Making old surfaces look new.",
        "hero_subhead": "High-pressure cleaning for driveways, paving, walls and outdoor areas across Perth. Resealing available.",
        "about_headline": "Concrete, paving and exterior walls.",
        "about": "JDS Pressure Cleaning handles driveways, brick paving, exterior walls and resealing across Perth. Before and after results that last.",
        "band_headline": "Driveway or patio looking tired?",
        "band_text": "Message on Facebook for a free quote and availability.",
        "gallery_captions": ["Driveway cleaning", "Paving and resealing", "Exterior wall wash", "Perth metro jobs"],
        "source": "https://www.facebook.com/jdspressurecleaning",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook only. No website.",
        "services": [
            {"title": "Driveway cleaning", "desc": "High-pressure wash for concrete and paving."},
            {"title": "Resealing", "desc": "Two-coat sealers for long-lasting protection."},
            {"title": "Exterior walls", "desc": "Brick and render cleaning and restoration."},
            {"title": "Commercial jobs", "desc": "Shops, warehouses and strata common areas."},
        ],
    },
    {
        "slug": "pooches-beauty-bar",
        "name": "Pooches Beauty Bar",
        "logo_text": "POOCHES",
        "industry": "Dog Grooming",
        "city": "Nedlands",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "Luxury pet grooming, Nedlands",
        "phone_raw": "+61400000026",
        "phone_display": "Book via Fresha",
        "address": "Shop 19, 88 Broadway Fair, Nedlands WA 6009",
        "service_area": "Nedlands, Crawley and western suburbs",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Grooming with luxury and care.",
        "hero_subhead": "Nedlands pet salon with full grooms, de-shed treatments and nail bar services.",
        "about_headline": "Qualified stylists. Happy pets.",
        "about": "Pooches Beauty Bar in Nedlands offers clipping, styling and pampering in a comfortable salon with qualified groomers.",
        "band_headline": "Full groom or tidy up?",
        "band_text": "Book through Fresha for your next appointment.",
        "gallery_captions": ["Full grooms", "Style grooms", "De-shed treatments", "Nedlands salon"],
        "source": "https://www.fresha.com/a/pooches-beauty-bar-nedlands-shop-19-88-broadway-fair-rnmhzs4l",
        "instagram": "https://www.instagram.com/poochesbeautybar/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Full grooms", "desc": "Wash, dry, clip and style for all breeds."},
            {"title": "Style grooms", "desc": "Breed-specific styling and tidy-ups."},
            {"title": "De-shed treatments", "desc": "Reduce shedding with deep coat care."},
            {"title": "Nail bar", "desc": "Quick trims through to full pawdicures."},
        ],
    },
    {
        "slug": "belashed-by-km",
        "name": "Belashed.bykm",
        "logo_text": "BELASHED",
        "industry": "Lash Extensions",
        "city": "Piara Waters",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Lash studio, Piara Waters",
        "phone_raw": "+61400000027",
        "phone_display": "Book via Fresha",
        "address": "Piara Waters, WA 6112",
        "service_area": "Piara Waters, Harrisdale and southern suburbs",
        "years": 3,
        "rating": "5.0",
        "hero_headline": "Lashes that frame your look.",
        "hero_subhead": "Home lash studio in Piara Waters. Classic, hybrid and volume sets by appointment.",
        "about_headline": "Detail-focused lash work.",
        "about": "Belashed.bykm is a home-based lash studio in Piara Waters serving the southern suburbs with classic and volume extensions.",
        "band_headline": "New set or refill?",
        "band_text": "Book on Fresha or DM on Instagram.",
        "gallery_captions": ["Classic lashes", "Hybrid sets", "Volume extensions", "Piara Waters studio"],
        "source": "https://www.fresha.com/a/belashed-bykm-piara-waters",
        "instagram": "https://www.instagram.com/belashed.bykm/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha and Instagram only.",
        "services": [
            {"title": "Classic lashes", "desc": "Natural extensions applied lash by lash."},
            {"title": "Hybrid sets", "desc": "Mix of classic and volume for fuller looks."},
            {"title": "Volume lashes", "desc": "Dramatic sets for events or everyday glam."},
            {"title": "Refills", "desc": "Maintain your set every two to three weeks."},
        ],
    },
    {
        "slug": "md-beauty-studio",
        "name": "MD Beauty Studio",
        "logo_text": "MD",
        "industry": "Beauty Studio",
        "city": "Madora Bay",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Home beauty studio, Madora Bay",
        "phone_raw": "+61400000028",
        "phone_display": "Book via Fresha",
        "address": "Madora Bay, WA 6210",
        "service_area": "Madora Bay, Mandurah and Peel region",
        "years": 4,
        "rating": "5.0",
        "hero_headline": "Beauty treatments by the coast.",
        "hero_subhead": "Home studio in Madora Bay for lashes, brows and beauty services in a private setting.",
        "about_headline": "Peel region. Personal service.",
        "about": "MD Beauty Studio is a home-based salon in Madora Bay offering lash, brow and beauty treatments with one-on-one attention.",
        "band_headline": "Lashes or brows?",
        "band_text": "Book through Fresha for your next appointment.",
        "gallery_captions": ["Lash extensions", "Brow shaping", "Beauty treatments", "Madora Bay studio"],
        "source": "https://www.fresha.com/a/md-beauty-studio-madora-bay",
        "instagram": "https://www.instagram.com/md.beautystudio/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Lash extensions", "desc": "Classic and volume full sets."},
            {"title": "Brow services", "desc": "Wax, tint and lamination."},
            {"title": "Lash lifts", "desc": "Lift and tint for natural lashes."},
            {"title": "Beauty add-ons", "desc": "Selected treatments by appointment."},
        ],
    },
    {
        "slug": "white-feather-beauty",
        "name": "White Feather Beauty",
        "logo_text": "FEATHER",
        "industry": "Beauty Studio",
        "city": "Tapping",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Home beauty, Tapping",
        "phone_raw": "+61400000029",
        "phone_display": "Book via Fresha",
        "address": "Tapping, WA 6065",
        "service_area": "Tapping, Ashby and northern suburbs",
        "years": 3,
        "rating": "5.0",
        "hero_headline": "Calm beauty in the northern suburbs.",
        "hero_subhead": "Home studio in Tapping for lashes, brows and skin treatments.",
        "about_headline": "Relax. Refresh. Repeat.",
        "about": "White Feather Beauty is a home-based studio in Tapping offering lash, brow and beauty services in a peaceful one-on-one environment.",
        "band_headline": "First visit?",
        "band_text": "Book on Fresha to secure your spot.",
        "gallery_captions": ["Lash treatments", "Brow shaping", "Skin services", "Tapping home studio"],
        "source": "https://www.fresha.com/a/white-feather-beauty-tapping",
        "instagram": "https://www.instagram.com/whitefeatherbeauty/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Lash services", "desc": "Extensions, lifts and tints."},
            {"title": "Brow treatments", "desc": "Shaping, tint and lamination."},
            {"title": "Skin treatments", "desc": "Selected facials and beauty services."},
            {"title": "Packages", "desc": "Combo brow and lash appointments."},
        ],
    },
    {
        "slug": "tay-luxe-studio",
        "name": "Tay Luxe Studio",
        "logo_text": "TAY LUXE",
        "industry": "Lash and Brow",
        "city": "Henley Brook",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Lash and brow studio, Henley Brook",
        "phone_raw": "+61400000030",
        "phone_display": "Book via Fresha",
        "address": "Henley Brook, WA 6055",
        "service_area": "Henley Brook, Ellenbrook and Swan Valley",
        "years": 2,
        "rating": "5.0",
        "hero_headline": "Luxe lashes and brows.",
        "hero_subhead": "Home studio in Henley Brook for lash extensions, lifts and brow lamination.",
        "about_headline": "Private studio. Polished results.",
        "about": "Tay Luxe Studio is a home-based lash and brow studio in Henley Brook serving the Swan Valley and Ellenbrook area.",
        "band_headline": "Special occasion?",
        "band_text": "Book through Fresha or message on Instagram.",
        "gallery_captions": ["Lash extensions", "Brow lamination", "Lash lifts", "Henley Brook studio"],
        "source": "https://www.fresha.com/a/tay-luxe-studio-henley-brook",
        "instagram": "https://www.instagram.com/tayluxestudio/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha and Instagram.",
        "services": [
            {"title": "Lash extensions", "desc": "Classic and hybrid full sets."},
            {"title": "Brow lamination", "desc": "Fuller, brushed-up brows."},
            {"title": "Lash lifts", "desc": "Lift and tint for everyday wear."},
            {"title": "Refills", "desc": "Keep your lash set fresh."},
        ],
    },
    {
        "slug": "gelato-nails-subiaco",
        "name": "Gelato Nails",
        "logo_text": "GELATO",
        "industry": "Nail Studio",
        "city": "Subiaco",
        "image_set": "salon",
        "theme": "salon",
        "tagline": "Nail studio, Subiaco",
        "phone_raw": "+61400000031",
        "phone_display": "Book via Fresha",
        "address": "Subiaco, WA 6008",
        "service_area": "Subiaco, Nedlands and western suburbs",
        "years": 4,
        "rating": "5.0",
        "hero_headline": "Nails worth showing off.",
        "hero_subhead": "Subiaco nail studio for gel manicures, extensions and nail art by appointment.",
        "about_headline": "Clean prep. Lasting finish.",
        "about": "Gelato Nails in Subiaco offers gel manicures, extensions and detailed nail art in a focused appointment-only setting.",
        "band_headline": "New set or refresh?",
        "band_text": "Book on Fresha for your next appointment.",
        "gallery_captions": ["Gel manicures", "Nail extensions", "Nail art", "Subiaco studio"],
        "source": "https://www.fresha.com/a/gelato-nails-subiaco",
        "instagram": "https://www.instagram.com/gelatonails/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Gel manicures", "desc": "Classic gel polish with proper prep."},
            {"title": "Extensions", "desc": "Gel extensions and structured sets."},
            {"title": "Nail art", "desc": "Minimal to detailed custom designs."},
            {"title": "Removals", "desc": "Safe soak-offs before your next set."},
        ],
    },
    {
        "slug": "ace-mobile-mechanic",
        "name": "A.C.E Mobile Mechanic",
        "logo_text": "ACE",
        "industry": "Mobile Mechanic",
        "city": "Perth",
        "image_set": "mechanic",
        "theme": "mechanic",
        "tagline": "Mobile mechanic, Perth metro",
        "phone_raw": "+61400000032",
        "phone_display": "Message via Facebook",
        "address": "Perth, WA",
        "service_area": "Perth metro and surrounds",
        "years": 7,
        "rating": "4.9",
        "hero_headline": "Mechanic that comes to you.",
        "hero_subhead": "Mobile automotive repairs and servicing across Perth. Home, work or roadside callouts.",
        "about_headline": "No workshop queues.",
        "about": "A.C.E Mobile Mechanic covers Perth metro with on-site servicing, repairs and breakdown assistance. Message or call to book.",
        "band_headline": "Broken down or service due?",
        "band_text": "Message on Facebook for a quote and availability.",
        "gallery_captions": ["On-site servicing", "Brake repairs", "Battery and starter", "Perth metro callouts"],
        "source": "https://www.facebook.com/ACEMobileMechanicPerth",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook only. No website.",
        "services": [
            {"title": "Servicing", "desc": "Logbook and general servicing at your location."},
            {"title": "Repairs", "desc": "Brakes, batteries, starters and general mechanical."},
            {"title": "Diagnostics", "desc": "Warning lights and fault finding on-site."},
            {"title": "Roadside assist", "desc": "Breakdown callouts across Perth metro."},
        ],
    },
    {
        "slug": "cambos-mobile-mechanic",
        "name": "Cambo's Mobile Mechanic",
        "logo_text": "CAMBO",
        "industry": "Mobile Mechanic",
        "city": "Perth",
        "image_set": "mechanic",
        "theme": "mechanic",
        "tagline": "Mobile mechanic, Perth",
        "phone_raw": "+61400000033",
        "phone_display": "Message via Facebook",
        "address": "Perth, WA",
        "service_area": "Perth metro",
        "years": 6,
        "rating": "5.0",
        "hero_headline": "Honest mobile mechanical.",
        "hero_subhead": "Cambo brings the workshop to your driveway. Servicing, repairs and pre-purchase inspections.",
        "about_headline": "Straight talk. Solid work.",
        "about": "Cambo's Mobile Mechanic services Perth with mobile repairs and logbook servicing. Fair pricing and clear communication on every job.",
        "band_headline": "Buying a used car?",
        "band_text": "Book a pre-purchase inspection or message for a service quote.",
        "gallery_captions": ["Mobile servicing", "Engine repairs", "Pre-purchase inspections", "Perth callouts"],
        "source": "https://www.facebook.com/CambosMobileMechanic",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook only.",
        "services": [
            {"title": "Logbook servicing", "desc": "Manufacturer services at your home or work."},
            {"title": "Repairs", "desc": "General mechanical and brake work."},
            {"title": "Pre-purchase inspections", "desc": "Check used cars before you buy."},
            {"title": "Fleet servicing", "desc": "Workplace and small fleet maintenance."},
        ],
    },
    {
        "slug": "perth-mech-mobile",
        "name": "Perth Mech Mobile Mechanics",
        "logo_text": "PMM",
        "industry": "Mobile Mechanic",
        "city": "Rockingham",
        "image_set": "mechanic",
        "theme": "mechanic",
        "tagline": "Mobile mechanics, Rockingham",
        "phone_raw": "+61400000034",
        "phone_display": "Message via Facebook",
        "address": "Rockingham, WA 6168",
        "service_area": "Rockingham, Kwinana and Perth south",
        "years": 5,
        "rating": "4.9",
        "hero_headline": "Southern suburbs mobile mechanic.",
        "hero_subhead": "Servicing and repairs across Rockingham, Kwinana and the southern corridor. We come to you.",
        "about_headline": "Local. Mobile. Reliable.",
        "about": "Perth Mech Mobile Mechanics covers the southern suburbs with on-site servicing, repairs and breakdown callouts.",
        "band_headline": "Stuck at home with a flat battery?",
        "band_text": "Message on Facebook or call for same-week availability.",
        "gallery_captions": ["Mobile servicing", "Brake work", "Battery replacements", "Southern suburbs"],
        "source": "https://www.facebook.com/PerthMechMobileMechanics",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook only.",
        "services": [
            {"title": "Servicing", "desc": "Logbook and general services on-site."},
            {"title": "Repairs", "desc": "Brakes, suspension and engine work."},
            {"title": "Batteries", "desc": "Testing, replacement and jump starts."},
            {"title": "Breakdown assist", "desc": "Roadside callouts in the south."},
        ],
    },
    {
        "slug": "salty-dog-pet-salon",
        "name": "Salty Dog Pet Salon",
        "logo_text": "SALTY",
        "industry": "Dog Grooming",
        "city": "Inglewood",
        "image_set": "pet",
        "theme": "pet",
        "tagline": "Pet grooming salon, Inglewood",
        "phone_raw": "+61400000035",
        "phone_display": "Book via Fresha",
        "address": "875 Beaufort Street, Inglewood WA 6052",
        "service_area": "Inglewood, Mount Lawley and Perth inner north",
        "years": 10,
        "rating": "4.9",
        "hero_headline": "Not your average pet salon.",
        "hero_subhead": "Inglewood grooming with styling, wellness treatments, nail bar and creative colour options.",
        "about_headline": "Experienced stylists. Happy dogs.",
        "about": "Salty Dog Pet Salon on Beaufort Street offers clipping, styling, teeth scaling, massage and nail bar services in a unique salon environment.",
        "band_headline": "Full groom or nail trim?",
        "band_text": "Book through Fresha for grooming and add-on services.",
        "gallery_captions": ["Grooming and styling", "Wellness treatments", "Nail bar", "Inglewood salon"],
        "source": "https://www.fresha.com/a/salty-dog-pet-salon-inglewood-875-beaufort-street-n2ujha33",
        "instagram": "https://www.instagram.com/saltydogpetsalon/",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Fresha only.",
        "services": [
            {"title": "Full grooming", "desc": "Wash, dry, clip and style by experienced stylists."},
            {"title": "Bathing", "desc": "Bath and blow-dry packages."},
            {"title": "Nail bar", "desc": "Quick trims through to full pawdicures."},
            {"title": "Wellness", "desc": "Massage, teeth scaling and skin treatments."},
        ],
    },
    {
        "slug": "one-and-all-cleaning",
        "name": "One and All Mobile Cleaning",
        "logo_text": "ONE&ALL",
        "industry": "Pressure Cleaning",
        "city": "Perth",
        "image_set": "gardener",
        "theme": "gardener",
        "tagline": "Mobile pressure cleaning, Perth",
        "phone_raw": "+61400000036",
        "phone_display": "Message via Facebook",
        "address": "Perth, WA",
        "service_area": "Perth metro, commercial and industrial",
        "years": 14,
        "rating": "5.0",
        "hero_headline": "High-pressure cleaning, any surface.",
        "hero_subhead": "Family-owned mobile cleaning for driveways, roofs, trucks, warehouses and graffiti removal across Perth.",
        "about_headline": "24/7 mobile service.",
        "about": "One and All Mobile Cleaning Service handles high-pressure cleaning, truck washing, roof and gutter work and graffiti removal across Perth metro.",
        "band_headline": "Commercial or residential?",
        "band_text": "Message for a quote. Same-week slots often available.",
        "gallery_captions": ["Driveway cleaning", "Truck washing", "Roof and gutter", "Graffiti removal"],
        "source": "https://www.facebook.com/OneAndAllMobileCleaning",
        "has_website": False,
        "demo_flag": "outreach",
        "contact_note": "Facebook and phone. No website.",
        "services": [
            {"title": "High-pressure cleaning", "desc": "Driveways, pavements and building exteriors."},
            {"title": "Truck washing", "desc": "Fleet and commercial vehicle cleaning."},
            {"title": "Roof and gutters", "desc": "Roof washing and gutter clearing."},
            {"title": "Graffiti removal", "desc": "Quick response for walls and fences."},
        ],
    },
]


def ig_handle(lead: dict) -> str:
    ig = lead.get("instagram", "")
    m = re.search(r"instagram\.com/([^/?]+)", ig)
    return f"@{m.group(1)}" if m else "see profile"


def channel_for(lead: dict) -> str:
    if lead.get("instagram"):
        return "Instagram"
    if "facebook.com" in lead.get("source", ""):
        return "Facebook"
    return "Email"


def pitch_hook(lead: dict) -> str:
    slug = lead["slug"]
    city = lead.get("city", "Perth")
    industry = lead.get("industry", "business")
    if "Fresha" in lead.get("contact_note", ""):
        return f"{industry} on Fresha in {city}; own domain beats booking link only"
    if "Facebook" in lead.get("contact_note", ""):
        return f"{industry} on Facebook only; preview for local Google searches"
    return f"{city} {industry.lower()}; no standalone website yet"


def tier_for(slug: str) -> str:
    return "Medium" if slug in MEDIUM else "Basic"


def ig_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    industry = lead.get("industry", "business")
    tier = tier_for(slug)
    basic = "$180 one-off (Basic: mobile site, contact form, deployment)"
    med = "Medium is $250 if you want basic support, Google indexing and your own domain"
    price = f"{basic} if you want it live. {med}." if tier == "Medium" else f"{basic} if you want it live. {med}."
    ig = lead.get("instagram", "")
    profile = ig or lead.get("source", "")
    first = name.split()[0] if " " in name and name[0].isupper() else "there"
    greeting = f"Hi {first}," if first != "there" and len(first) < 12 else "Hi, quick one."
    body = f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: Instagram DM
PROFILE: {profile}
DEMO: https://edisonrees.github.io/macrosa-web/demos/{slug}/

{greeting} I'm Edison from Caisson (web dev in Perth).

I came across {name} on Instagram. You're doing great work in {city} but don't have a proper website when people search {industry.lower()} near me.

Built a free preview:
https://edisonrees.github.io/macrosa-web/demos/{slug}/ 

{price} Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this one locked in. No stress if not for you.

Cheers,
Edison · Caisson · Perth
"""
    return body


def fb_draft(lead: dict) -> str:
    slug = lead["slug"]
    name = lead["name"]
    city = lead.get("city", "Perth")
    tier = tier_for(slug)
    basic = "$180 one-off (Basic: mobile site, contact form, deployment)"
    med = "Medium is $250 if you want basic support, Google indexing and your own domain"
    price = f"{basic} if you want it live. {med}." if tier == "Medium" else f"{basic} if you want it live. {med}."
    return f"""DRAFT ONLY - DO NOT SEND WITHOUT EDISON APPROVAL ON DISCORD
CHANNEL: Facebook Messenger
PAGE: {lead.get('source', '')}
DEMO: https://edisonrees.github.io/macrosa-web/demos/{slug}/

Hi, quick one from Edison at Caisson (web dev in Perth).

I found {name} on Facebook. Good work around {city} but no proper website when locals search Google.

Built a free preview:
https://edisonrees.github.io/macrosa-web/demos/{slug}/ 

{price} Rebuilding previews with upgraded tooling tomorrow at 7pm Perth, so shout if you want this locked in. No stress if not for you.

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

    start_num = 26
    rows = []
    for i, lead in enumerate(added):
        slug = lead["slug"]
        ch = channel_for(lead)
        if ch == "Instagram":
            draft_path = OUTREACH / f"ig-{slug}.txt"
            draft_path.write_text(ig_draft(lead), encoding="utf-8")
        else:
            draft_path = OUTREACH / f"fb-{slug}.txt"
            draft_path.write_text(fb_draft(lead), encoding="utf-8")

        num = start_num + i
        tier = tier_for(slug)
        hook = pitch_hook(lead)
        rows.append(
            f"| {num} | {lead['name']} | `{slug}` | **{ch}** | "
            f"https://edisonrees.github.io/macrosa-web/demos/{slug}/ | {hook} | {tier} | `outreach/{draft_path.name}` |"
        )
        print(f"Draft: {draft_path.name}")

    review = REVIEW.read_text(encoding="utf-8")
    review = re.sub(r"\*\*25 drafts\*\*", f"**{len(existing)} drafts**", review)
    review = re.sub(
        r"\| 25 \| Studio B Nails\.Co.*\n",
        lambda m: m.group(0) + "\n".join(rows) + "\n",
        review,
    )
    REVIEW.write_text(review, encoding="utf-8")
    print(f"Updated REVIEW-INDEX.md ({len(added)} rows)")

    slugs_file = ROOT / "leads" / "overnight_slugs.txt"
    slugs_file.write_text("\n".join(l["slug"] for l in added), encoding="utf-8")
    print(f"Slugs: {slugs_file}")


if __name__ == "__main__":
    main()
