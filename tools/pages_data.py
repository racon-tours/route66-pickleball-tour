"""Content for the city guides, the direction pages and the FAQ page.

Edit the words here, then run:  python3 tools/build_pages.py
Venue facts were checked in November 2026. Re-check hours before each season.
Day-of-week notes assume the locked pattern: westbound leaves Chicago on a Sunday,
eastbound leaves Santa Monica on a Tuesday.
"""

CHECKED = "November 2026"

# Each city: slug, display name, heading font (brand guide), when we're there, the hotel(s),
# an intro, then sections of picks. A pick is (name, where, why).
CITIES = [
  {
    "slug": "chicago", "name": "Chicago", "state": "Illinois", "font": "Monoton",
    "title": "Chicago: where to eat, drink and explore near the Chicago Athletic Association",
    "desc": "Your Route 66 Pickleball Tour night in Chicago: what's inside the Chicago Athletic Association, plus the best food, blues and sights a short walk from Millennium Park.",
    "when": [("Westbound", "Day 1 (Sunday) — arrival, Kickoff Reception 6:00–8:00 pm"),
             ("Eastbound", "Day 10 (Thursday) — Farewell Happy Hour, then your last night")],
    "hotels": [("Chicago Athletic Association", "12 S. Michigan Ave., across from Millennium Park",
                "An 1893 Venetian Gothic gentlemen's club turned hotel. The Route 66 BEGIN sign is a three-minute walk away.")],
    "intro": "You're on Michigan Avenue with Millennium Park and the Art Institute across the street. Everything below is walkable, and the hotel itself could fill your whole evening.",
    "sections": [
      ("Inside the hotel", [
        ("Cindy's", "13th-floor rooftop", "Glass-roofed dining room and terrace looking straight over Millennium Park to the lake. Book ahead for dinner; the bar is the easier way in."),
        ("Cherry Circle Room", "In the hotel", "The club's old dining room, back in business with a menu drawn from a century of its own menus."),
        ("Milk Room", "In the hotel", "An eight-seat bar pouring rare and vintage spirits. Tiny, so reserve."),
        ("Game Room", "In the hotel", "Billiards, bocce, shuffleboard and a long bar — a good place to find the rest of the tour."),
      ]),
      ("Dinner nearby", [
        ("The Gage", "24 S. Michigan Ave. — next door", "A gastropub with one of the Loop's best burgers and a long list of creative comfort food."),
        ("Acanto", "18 S. Michigan Ave. — next door", "Italian from the same team as The Gage, steps from the park."),
        ("The Walnut Room", "Macy's on State Street — about 6 minutes on foot", "Chicago's grand old department-store dining room, famous for its chicken pot pie."),
      ]),
      ("After dinner", [
        ("Buddy Guy's Legends", "700 S. Wabash Ave. — about 15 minutes on foot", "The city's best-known blues club, live music every night."),
        ("Symphony Center", "220 S. Michigan Ave. — 3 minutes on foot", "Home of the Chicago Symphony Orchestra. Check the calendar before you fly."),
        ("The Theatre District", "Around State and Randolph — about 10 minutes on foot", "Touring Broadway shows and the Chicago Theatre's famous marquee."),
      ]),
      ("See and do", [
        ("Millennium Park and Cloud Gate", "Across the street", "\"The Bean,\" Crown Fountain and the Pritzker Pavilion. Lovely at dusk."),
        ("The Art Institute of Chicago", "Across the street", "One of the world's great museums. Arrive early on Day 1 and give it two hours."),
        ("Chicago Architecture Center river cruise", "Departs at Michigan Ave. and the river — about 15 minutes on foot", "The classic 90-minute look at the skyline from the water."),
        ("The Route 66 BEGIN sign", "Adams St. at Michigan Ave. — 3 minutes on foot", "Where the whole road starts. We take the group photo here together."),
      ]),
    ],
    "tips": ["The hotel adds a nightly resort fee that includes skip-the-line entry to Cindy's — ask at the desk.",
             "O'Hare and Midway both connect to the Loop by the L train; a cab or rideshare is easier with luggage."],
  },
  {
    "slug": "st-louis", "name": "St. Louis", "state": "Missouri", "font": "Chango",
    "title": "St. Louis: where to eat, drink and explore in the Central West End",
    "desc": "Your Route 66 Pickleball Tour night in St. Louis at the Chase Park Plaza: dinner, drinks and sights in the Central West End, your tour directors' home neighborhood.",
    "when": [("Westbound", "Day 2 (Monday) — after the morning session and the drive down from Chicago"),
             ("Eastbound", "Day 9 (Wednesday) — after the Ozarks and the big river")],
    "hotels": [("Royal Sonesta Chase Park Plaza", "212 N. Kingshighway Blvd., Central West End",
                "A 1920s landmark across the street from Forest Park, with its own cinema, steakhouse and pool-side bar.")],
    "intro": "Welcome to our neighborhood — Mike and Trina live a few blocks away. The Central West End is the city's most walkable dining district, and Forest Park, one of the largest city parks in the country, is across the street.",
    "sections": [
      ("Inside the hotel", [
        ("The Tenderloin Room", "In the hotel", "A St. Louis steakhouse institution, all dark wood and white tablecloths."),
        ("Chase Club", "In the hotel", "Gastropub menu, a big bar and a patio by the pool with an outdoor fireplace."),
        ("Chase Park Plaza Cinemas", "In the hotel", "A real movie theater downstairs. Catch a film after dinner without stepping outside."),
      ]),
      ("Dinner nearby", [
        ("Brasserie by Niche", "4580 Laclede Ave. — about 5 minutes on foot", "A French bistro from one of the city's best chefs: steak frites, mussels, roast chicken."),
        ("Bar Italia", "13 Maryland Plaza — about 5 minutes on foot", "A neighborhood Italian fixture with a big sidewalk patio."),
        ("Vicia", "Cortex district — a short ride", "Vegetable-forward tasting menus, recognized nationally. Worth a reservation."),
      ]),
      ("A Route 66 detour", [
        ("Ted Drewes Frozen Custard", "6726 Chippewa St. — about 15 minutes by car", "On old Route 66 since the 1940s. Order a \"concrete\" — it's served upside down to prove how thick it is."),
      ]),
      ("See and do", [
        ("Forest Park", "Across the street", "Home of the 1904 World's Fair. The Saint Louis Art Museum, the Zoo and the Missouri History Museum are all inside and free to enter."),
        ("Cathedral Basilica of Saint Louis", "4431 Lindell Blvd. — about 10 minutes on foot", "One of the largest mosaic collections in the world, covering the walls and domes."),
        ("World Chess Hall of Fame", "4652 Maryland Ave. — about 5 minutes on foot", "Look for the giant king on the sidewalk out front."),
        ("Euclid Avenue and Maryland Plaza", "Steps from the hotel", "Shops, sidewalk cafés and bars for an easy evening stroll."),
      ]),
    ],
    "tips": ["Westbound is here on a Monday, when some kitchens close. Check before you walk over.",
             "Forest Park is beautiful but big. Use a rideshare to reach the museums if you're short on time."],
  },
  {
    "slug": "grand-lake", "name": "Grand Lake", "state": "Oklahoma", "font": "Limelight",
    "title": "Grand Lake: your two nights at Shangri-La Resort",
    "desc": "Two nights at Shangri-La Resort on Grand Lake, Oklahoma: the indoor court dome, the Anchor Activity Park, lakeside bars, the spa and where to eat on the resort.",
    "when": [("Westbound", "Days 3–4 (Tuesday and Wednesday) — two nights, three sessions"),
             ("Eastbound", "Days 7–8 (Monday and Tuesday) — two nights, three sessions and the finals")],
    "hotels": [("Shangri-La Resort", "57301 E. Highway 125, Monkey Island, Afton, Oklahoma",
                "A lakefront resort at the tip of Monkey Island on Grand Lake O' the Cherokees.")],
    "intro": "The first of the tour's two resort stays, and the place to unpack properly. Everything is on the property, so there's nowhere you need to be after the morning session except the pool, the lake or the bar.",
    "sections": [
      ("The Anchor Activity Park", [
        ("The dome", "At The Anchor", "Our courts under a giant heated dome — play in any weather."),
        ("Outdoor courts and lawn games", "At The Anchor", "Pickleball and tennis courts, cornhole, sand volleyball and fire pits."),
        ("Arcade, simulators and bar games", "Inside The Anchor", "Golf simulators, an arcade, ping pong, shuffleboard and darts."),
      ]),
      ("Eat and drink on the resort", [
        ("The Summit Restaurant", "Resort hotel", "The resort's main dining room."),
        ("Doc's Bar & Grill", "By the pool", "Casual food and drinks poolside."),
        ("Eddy's Lakeside Bar", "On the water", "The sunset spot."),
        ("The Galley", "At The Anchor", "Quick food between games."),
        ("Buffalo Bar", "Resort hotel", "A nightcap close to your room."),
      ]),
      ("Unwind", [
        ("The Spa at Shangri-La", "Resort hotel", "Massages and body treatments. Book early in the day — the whole tour has the same idea."),
        ("Indoor and outdoor pools", "Resort hotel", "The outdoor pool is seasonal; the indoor pool runs year-round."),
        ("Golf", "On the property", "Championship golf on the lake. Ask the golf shop about tee times on your free afternoon."),
        ("The marina", "On Grand Lake", "Boat and watercraft rentals in season."),
      ]),
    ],
    "tips": ["Some outlets keep seasonal hours. We'll post what's open each night in the group text.",
             "Breakfast is on us here. Your pre-trip notes explain how it works at this resort."],
  },
  {
    "slug": "amarillo", "name": "Amarillo", "state": "Texas", "font": "Rye",
    "title": "Amarillo: where to eat and drink near The Barfield after Cadillac Ranch",
    "desc": "Your Route 66 Pickleball Tour night in Amarillo: steak, patios and live music near The Barfield on Polk Street, plus Route 66's Sixth Street district.",
    "when": [("Westbound", "Day 5 (Thursday) — the road all day, Cadillac Ranch at golden hour"),
             ("Eastbound", "Day 6 (Sunday) — the Blue Swallow at Tucumcari, then Cadillac Ranch")],
    "hotels": [("The Barfield, Autograph Collection", "600 S. Polk St., downtown Amarillo",
                "A restored 1920s downtown landmark with a steakhouse and a speakeasy on site.")],
    "intro": "You'll arrive with spray paint on your hands from Cadillac Ranch. Polk Street, downtown's dining strip, starts at the hotel's front door, and on a calm evening its patios are the best seats in the Panhandle.",
    "sections": [
      ("Inside the hotel", [
        ("Toscana", "In the hotel", "A Texas-style Italian steakhouse — the steak the route promised."),
        ("Paramount Recreation Club", "In the hotel", "A Prohibition-style speakeasy bar."),
      ]),
      ("On Polk Street", [
        ("Crush Wine Bar & Grill", "627 S. Polk St. — 2 minutes on foot", "Steaks, small plates and a serious wine list, with a patio."),
        ("Six Car Pub & Brewery", "Polk St. — 2 minutes on foot", "House-brewed beer and a rooftop bar."),
        ("Braceros", "727 S. Polk St. — 4 minutes on foot", "A big, lively Mexican restaurant and bar."),
        ("Nomad Napoletana", "Polk St. — a few minutes on foot", "Wood-fired Neapolitan pizza and one of the street's best patios."),
      ]),
      ("Route 66's Sixth Street", [
        ("GoldenLight Cafe & Cantina", "2906 SW 6th Ave. — about 10 minutes by car", "Open since 1946 — the longest continuously operating restaurant on Route 66, still flipping burgers. The cantina next door has live music on Thursday to Saturday nights."),
        ("Historic Route 66–Sixth Street District", "SW 6th Ave. between Georgia and Western", "A mile of antique shops, murals and old service stations on the original road."),
      ]),
    ],
    "tips": ["Amarillo is windy. If the patio is blowing, the speakeasy is right downstairs.",
             "Hodgetown, the minor-league ballpark, is 7 minutes on foot. Check the schedule for a home game in spring and summer."],
  },
  {
    "slug": "albuquerque", "name": "Albuquerque", "state": "New Mexico", "font": "Vast Shadow",
    "title": "Albuquerque: green chile, rooftop cocktails and Route 66 near Hotel Parq Central",
    "desc": "Your Route 66 Pickleball Tour night in Albuquerque at Hotel Parq Central, a restored 1926 railway hospital on Route 66: New Mexican food, EDo dining and Old Town.",
    "when": [("Westbound", "Day 6 (Friday) — after the morning session"),
             ("Eastbound", "Day 5 (Saturday) — after the Wigwam Motel at Holbrook")],
    "hotels": [("Hotel Parq Central", "806 Central Ave. SE — on Route 66 itself",
                "Built in 1926 as the Santa Fe Railway's hospital, now a boutique hotel with a rooftop bar.")],
    "intro": "Central Avenue out front is Route 66, and you're on the edge of EDo, East Downtown, a neighborhood of brick Victorians and good restaurants. Tonight's one question is the state question: red or green? (Say \"Christmas\" and you get both.)",
    "sections": [
      ("Inside the hotel", [
        ("Apothecary Lounge", "Rooftop", "Cocktails with a view across the city to the Sandia Mountains — go at sunset."),
      ]),
      ("Dinner nearby", [
        ("Artichoke Cafe", "424 Central Ave. SE — about 8 minutes on foot", "Albuquerque's long-running EDo dining room, with a deep wine cellar."),
        ("66 Diner", "Central Ave. — about 10 minutes on foot", "Neon, chrome, green chile cheeseburgers and milkshakes. Route 66 straight up."),
        ("Frontier Restaurant", "Central Ave. across from the university — a short ride", "A beloved, cheap and cheerful New Mexican institution. Get a sweet roll."),
        ("The Grove Cafe & Market", "600 Central Ave. SE — 4 minutes on foot", "Daytime only, but the best coffee and pastry in EDo before the motorcoach leaves."),
      ]),
      ("See and do", [
        ("Old Town Plaza", "About 10 minutes by car", "San Felipe de Neri Church, whose parish dates to the city's founding in 1706, plus adobe shops and galleries around the original plaza."),
        ("Sawmill Market", "Near Old Town", "A food hall in an old lumber warehouse — good when the group can't agree on dinner."),
        ("KiMo Theatre", "Central Ave. downtown — about 15 minutes on foot", "A 1927 Pueblo Deco movie palace on Route 66. Check for a show."),
      ]),
    ],
    "tips": ["Ask the front desk about the hotel's shuttle for short trips around town.",
             "At 5,300 feet the air is dry and drinks hit harder. Keep a water bottle going."],
  },
  {
    "slug": "flagstaff", "name": "Flagstaff", "state": "Arizona", "font": "Knewave",
    "title": "Flagstaff: breweries, Route 66 and dark skies near Little America",
    "desc": "Your Route 66 Pickleball Tour night in Flagstaff at Little America: the hotel's forest grounds, downtown breweries on Route 66 and Lowell Observatory.",
    "when": [("Westbound", "Day 7 (Saturday) — after the morning session"),
             ("Eastbound", "Day 4 (Friday) — Kingman, Seligman, then the climb")],
    "hotels": [("Little America Flagstaff", "2515 E. Butler Ave.",
                "A classic 1950s hotel set in its own 500-acre ponderosa pine forest, about ten minutes east of downtown.")],
    "intro": "At 7,000 feet, Flagstaff is the highest town on Route 66 and our one night off the courts. Downtown is a short ride away: old brick, railroad tracks, a dozen breweries and Route 66 running right through it.",
    "sections": [
      ("At the hotel", [
        ("Silver Pine Restaurant & Bar", "In the hotel", "The easy dinner, with a fire-pit patio under the pines."),
        ("Forest trails", "On the grounds", "Walking paths through the hotel's own pine forest. A good stretch after a day on the motorcoach."),
      ]),
      ("Downtown — about 10 minutes by car", [
        ("Mother Road Brewing", "Downtown", "Named for Route 66. A local favorite with a big patio."),
        ("Historic Brewing", "Downtown", "Good beer and good food under one roof."),
        ("Lumberyard Brewing", "5 S. San Francisco St.", "A brewpub in an old lumberyard by the tracks."),
        ("Diablo Burger", "Heritage Square", "Local beef, a tiny room and a cult following."),
        ("Josephine's", "Downtown", "A cozy, more grown-up dinner in a historic house."),
      ]),
      ("See and do", [
        ("Lowell Observatory", "Mars Hill — about 15 minutes by car", "Where Pluto was discovered in 1930. Flagstaff was the world's first International Dark Sky City; evening programs put you behind the telescopes."),
        ("Historic downtown", "Around Heritage Square", "Route 66 and the railroad run side by side. Look for the 1927 Hotel Monte Vista."),
      ]),
    ],
    "tips": ["It's cold at night, even in summer. Bring a layer.",
             "Rideshares are the easy way between the hotel and downtown. The front desk can call a cab."],
  },
  {
    "slug": "la-quinta", "name": "La Quinta", "state": "California", "font": "Pacifico",
    "title": "La Quinta: your two nights at La Quinta Resort & Club",
    "desc": "Two nights at La Quinta Resort & Club in the Coachella Valley: courts under the lights, more than 40 pools, the spa, the restaurants and Old Town La Quinta.",
    "when": [("Westbound", "Days 8–9 (Sunday and Monday) — two nights, three sessions and the finals"),
             ("Eastbound", "Days 2–3 (Wednesday and Thursday) — two nights, three sessions")],
    "hotels": [("La Quinta Resort & Club", "49499 Eisenhower Dr., La Quinta, California",
                "The desert's first resort, opened in 1926 as a Hollywood hideaway at the foot of the Santa Rosa Mountains."),
               ("Omni Rancho Las Palmas", "Rancho Mirage — April eastbound departure only",
                "The April eastbound tour stays here instead. We'll send that group its own notes.")],
    "intro": "The tour's second resort stay, and the one people talk about afterwards. Casitas among the palms, a pool around every corner and, for the finals, courts under the lights against the mountains.",
    "sections": [
      ("Eat and drink on the resort", [
        ("Morgan's in the Desert", "Resort", "The signature restaurant, dinner only, with live music on weekends. Book this one ahead."),
        ("TWENTY6", "Resort", "Relaxed American bistro and bar."),
        ("Adobe Grill", "Resort", "Mexican food and more than 100 tequilas on a terrace facing the mountains."),
        ("Ernie's", "Resort", "Sports bar and a hearty breakfast."),
      ]),
      ("Unwind", [
        ("The pools", "All over the property", "More than 40 of them. Wander until you find a quiet one."),
        ("Spa La Quinta", "Resort", "The valley's famous spa. Treatments book up — reserve before you arrive."),
        ("Golf", "Next to the resort", "The Mountain and Dunes courses start steps from the casitas."),
      ]),
      ("Just off the property", [
        ("Old Town La Quinta", "About a mile — a short ride", "Restaurants, galleries and boutiques around a walkable village square."),
        ("Palm Springs", "About 30 minutes by car", "Mid-century architecture, the Aerial Tramway and Palm Canyon Drive."),
      ]),
    ],
    "tips": ["The desert is hot by midday from spring on. Our sessions are in the morning for a reason — save the pool for the afternoon.",
             "Breakfast is on us here. Your pre-trip notes explain how it works at this resort."],
  },
  {
    "slug": "santa-monica", "name": "Santa Monica", "state": "California", "font": "Baumans",
    "title": "Santa Monica: where to eat, drink and explore near the pier",
    "desc": "Your Route 66 Pickleball Tour nights in Santa Monica at The Georgian and The Eden on Ocean Avenue: the End of the Trail sign, the pier, dinner and the Wednesday farmers market.",
    "when": [("Westbound", "Day 10 (Tuesday) — End of the Trail, Farewell Happy Hour and your last night (The Georgian)"),
             ("Eastbound", "Day 1 (Tuesday) — arrival and Kickoff Reception (The Eden)")],
    "hotels": [("The Georgian", "1415 Ocean Ave. — westbound",
                "A turquoise 1933 Art Deco landmark across from the beach, with a front porch made for sunset."),
               ("The Eden", "1301 Ocean Ave. — eastbound",
                "A 1940 Streamline Moderne beauty on the bluffs, known for decades as the Hotel Shangri-La, with a saltwater pool and a rooftop bar.")],
    "intro": "Both hotels sit a block apart on Ocean Avenue, above the beach and a short walk from the pier where Route 66 ends. Everything here is on foot.",
    "sections": [
      ("Dinner nearby", [
        ("Élephante", "1332 2nd St. — 2 minutes on foot", "Mediterranean food on a rooftop with an ocean view. The scene of the street."),
        ("Water Grill", "1401 Ocean Ave. — 3 minutes on foot", "Very fresh seafood and a raw bar."),
        ("Birdie G's", "Bergamot Station — a short ride", "One of the best restaurants in Los Angeles, a warm and playful take on family-style food."),
      ]),
      ("See and do", [
        ("The End of the Trail sign", "Santa Monica Pier — about 8 minutes on foot", "The finish line. Paddles up."),
        ("Santa Monica Pier", "About 8 minutes on foot", "The Ferris wheel, the carousel and the arcade. Best as the lights come on."),
        ("Palisades Park", "Along Ocean Ave., right outside", "A clifftop park with palm trees and the sunset over the Pacific."),
        ("Third Street Promenade", "1–2 minutes on foot", "Pedestrian shopping street, good for a last-minute gift."),
        ("Main Street and Venice", "20 minutes on foot or a short ride", "Local shops and cafés, then the Venice boardwalk and canals."),
      ]),
      ("Westbound, before you fly home", [
        ("Santa Monica Farmers Market", "Arizona Ave. at 2nd St. — Wednesday morning", "One of the country's great farmers markets, the one L.A. chefs shop at. It runs on your departure morning."),
      ]),
    ],
    "tips": ["LAX is about 30 minutes by car, more at rush hour. Leave plenty of time on Day 11.",
             "Bike rentals line the beach path if you want one more ride along the sand."],
  },
]


# Day-by-day pages. (day, weekday, overnight city slug, headline, what happens, play, along the way)
WESTBOUND = [
  ("Day 1", "Sunday", "chicago", "The BEGIN sign", "Arrive in Chicago, a sidewalk photo at the sign on Adams Street, then the Kickoff Reception at the hotel, 6:00–8:00 pm.", "Arrival day", []),
  ("Day 2", "Monday", "st-louis", "The Mississippi", "Indoor courts on the way out of Chicago, then down the old road across Illinois to the big river by evening.", "Morning session", ["Route 66 Hall of Fame & Museum, Pontiac, Illinois"]),
  ("Days 3–4", "Tuesday–Wednesday", "grand-lake", "The dome", "A Missouri morning on the courts, the Ozarks, then two nights at the lake.", "Three sessions", ["Gary's Gay Parita, a restored Sinclair station in Ash Grove, Missouri"]),
  ("Day 5", "Thursday", "amarillo", "Cadillac Ranch", "The road all day across Oklahoma and into Texas, then spray paint at golden hour.", "The road all day", ["The Blue Whale of Catoosa, Oklahoma", "POPS 66 Soda Ranch and its 66-foot neon bottle, Arcadia, Oklahoma"]),
  ("Day 6", "Friday", "albuquerque", "Green chile", "A morning session, then west into New Mexico and a night in a restored 1926 railway hospital.", "Morning session", ["The 1939 neon of the Blue Swallow Motel, Tucumcari, New Mexico"]),
  ("Day 7", "Saturday", "flagstaff", "Ponderosa country", "A morning session, then up to seven thousand feet in the pines.", "Morning session", ["Wigwam Motel, Holbrook, Arizona", "Standin' on the Corner Park, Winslow, Arizona"]),
  ("Days 8–9", "Sunday–Monday", "la-quinta", "Under the lights", "A Flagstaff morning, the old road down through Arizona, then two nights in the desert and the finals under the lights.", "Three sessions · finals", ["Angel Delgadillo's barbershop in Seligman, Arizona", "Arizona Route 66 Museum, Kingman"]),
  ("Day 10", "Tuesday", "santa-monica", "End of the Trail", "The farewell session, the pier, the Pacific, the group photo — paddles up — then the Farewell Happy Hour.", "Farewell session", []),
  ("Day 11", "Wednesday", None, "Home", "Your last hotel night is included. Fly home from LAX whenever suits you.", "Departure day", []),
]

EASTBOUND = [
  ("Day 1", "Tuesday", "santa-monica", "End of the Trail", "Arrive in Santa Monica, the sign on the pier in the last of the light, then the Kickoff Reception.", "Arrival day", []),
  ("Days 2–3", "Wednesday–Thursday", "la-quinta", "Under the lights", "A morning in Los Angeles, then east into the desert for two nights.", "Three sessions", []),
  ("Day 4", "Friday", "flagstaff", "Ponderosa country", "Kingman's museum and Angel Delgadillo's barbershop in Seligman, then the climb into the pines.", "The road all day", ["Arizona Route 66 Museum, Kingman", "Angel Delgadillo's barbershop, Seligman, Arizona"]),
  ("Day 5", "Saturday", "albuquerque", "Green chile", "A high-country morning, the Wigwam Motel at Holbrook, then a restored 1926 railway hospital.", "Morning session", ["Wigwam Motel, Holbrook, Arizona"]),
  ("Day 6", "Sunday", "amarillo", "Cadillac Ranch", "The Blue Swallow at Tucumcari, then spray paint at golden hour.", "Morning session", ["The 1939 neon of the Blue Swallow Motel, Tucumcari, New Mexico", "Buc-ee's, Amarillo — a very Texas pit stop"]),
  ("Days 7–8", "Monday–Tuesday", "grand-lake", "The dome", "An Amarillo morning, the Blue Whale on the way in, two nights at the lake and the finals.", "Three sessions · finals", ["POPS 66 Soda Ranch, Arcadia, Oklahoma", "The Blue Whale of Catoosa, Oklahoma"]),
  ("Day 9", "Wednesday", "st-louis", "Challenge Day", "One last morning on the resort courts, then the Ozarks and the big river.", "Morning session", ["Gary's Gay Parita, Ash Grove, Missouri"]),
  ("Day 10", "Thursday", "chicago", "The BEGIN sign", "A last St. Louis morning, up the old road to the sidewalk where it all starts, then the Farewell Happy Hour.", "Morning session", ["Route 66 Hall of Fame & Museum, Pontiac, Illinois"]),
  ("Day 11", "Friday", None, "Home", "Your last hotel night is included. Fly home from O'Hare or Midway whenever suits you.", "Departure day", []),
]

# The questions page: the home-page FAQ plus a few more. (group, [(q, a), ...]) — answers may hold HTML.
FAQ = [
  ("The pickleball", [
    ("What level do I need to be?", "Beginner to 4.0+. There's no rating gate and no minimum. We ask for your DUPR (or your best guess) when you book, but it doesn't set your seed: the directors seed the bracket from watching everyone play at the Day 2 session."),
    ("Do I need to bring a partner?", "No. Come alone and the draw deals you in. Come as a pair and the doubles bracket is yours together, start to finish. Blind doubles mixes everyone up either way."),
    ("Do I have to play every session?", "Never. Play is always optional, and you decide when to sit one out. Every session is a morning session, so afternoons belong to the road either way."),
    ("How many sessions are there, and where?", "Ten, all in the mornings, on courts booked for the tour alone: club sessions with local pros along the way, and three sessions at each of the two resorts. See the <a href=\"/westbound\">westbound</a> and <a href=\"/eastbound\">eastbound</a> day-by-day pages."),
    ("What about altitude?", "We never schedule play above about 6,000 feet, so Flagstaff is a sightseeing stop, not a court stop. Albuquerque sits at about 5,300 feet, so that session is a shorter 90-minute block."),
    ("What happens if I'm knocked out of the bracket?", "You keep playing. Every session has clinics with local pros and rec play, and nobody's tour ends in elimination."),
  ]),
  ("Who's coming", [
    ("How big is the group?", "Thirty-two players per departure, plus just a few non-playing companions, and your tour directors, Mike and Trina, who ride every departure."),
    ("Can a non-player come along?", "Yes. There are just a few non-playing companion seats on each departure. Companions ride, stay, eat and celebrate with the group; they just skip the draw."),
    ("Is there a minimum age?", "Every guest must be 21 or older."),
    ("I'm traveling solo. Will you match me with a roommate?", "We don't match roommates. Solo travelers book a single room, or bring a friend and share."),
  ]),
  ("What's included", [
    ("What does the price include?", "The motorcoach, ten nights of hotels, all ten sessions, club-pro coaching, breakfast and lunch every day, the Kickoff Reception and the Farewell Happy Hour."),
    ("Are dinners included?", "No, and that's on purpose. Every other evening you're loose in some of the best roadfood country in America. Each overnight has a guide to the neighborhood around the hotel — start with <a href=\"/cities/chicago\">Chicago</a>."),
    ("What are the hotels like?", "Every night is in a hotel with a story: an 1893 athletic club in Chicago, a lakeside resort under a court dome in Oklahoma, a restored 1926 railway hospital in Albuquerque, the desert's first resort in La Quinta, and Art Deco on the ocean in Santa Monica."),
    ("What's the motorcoach like?", "A full-size luxury motorcoach with a restroom on board and room to spread out."),
  ]),
  ("Booking and payment", [
    ("How much is the deposit?", "$500 per person holds your seat. It's fully refundable for 3 days after you book; after that it's non-refundable."),
    ("When is the balance due?", "75 days before departure. Inside 60 days, payments are non-refundable."),
    ("What if I can't go?", "You can hand your seat to someone else up to 45 days before departure. Full details are in our <a href=\"https://pickle.tours/booking-terms\">booking terms</a>."),
    ("Should I buy travel insurance?", "We recommend it, though it isn't required. A policy that covers trip cancellation and medical care away from home is the one to look for."),
  ]),
  ("Getting there and home", [
    ("Where does the tour start and finish?", "It's a one-way tour. Westbound starts in Chicago and finishes in Santa Monica; eastbound runs the other way. Fly into one end and home from the other."),
    ("Which airports should I use?", "Chicago O'Hare or Midway at the Chicago end, and LAX at the Santa Monica end."),
    ("When should I arrive?", "Day 1 is arrival day, with the Kickoff Reception at the hotel from 6:00 to 8:00 pm. Plan to land that afternoon. The motorcoach leaves on the morning of Day 2."),
    ("When can I fly home?", "The Farewell Happy Hour is on the last evening, and your final hotel night is included, so book your flight home for Day 11. Want a few extra days at either end? Tell us and we'll help you add nights."),
    ("How much luggage can I bring?", "A normal suitcase plus your paddle bag. The motorcoach has full-size luggage bays, and baggage handling at every hotel is covered."),
  ]),
]
