from ytmusicapi import YTMusic

# Initialize YTMusic with OAuth credentials
ytmusic = YTMusic('oauth.json')

# Define the songs to be added to the playlist
songs = [
    "Hyperballad by Björk", "FML by Deadmau5", "Deus Ex Machina by Deadmau5", "Eight Oh Eight by Mason",
    "Static on the Wire by Holy Ghost!", "Push Pull by Purity Ring", "Vamp by Trentemøller",
    "Snowflake by Trentemøller", "Evil Dub by Trentemøller", "Ghost Hardware by Burial",
    "Divinity by Porter Robinson", "I'll Be Alright Tonight by Mura Masa", "Fine Whine by ASAP Rocky",
    "Feel No Ways by Drake", "Love Lockdown by Kanye West", "Ghosttown by Yung Lean", 
    "Grnfthr by Spark Master Tape", "Kanye West - Mercy", "Travis Scott - Sicko Mode", 
    "Dr. Dre - Still D.R.E.", "HUMBLE. by Kendrick Lamar", "Nonstop by Drake", 
    "Clint Eastwood by Gorillaz", "Madness by Muse", "Seven Nation Army by The White Stripes", 
    "Do I Wanna Know? by Arctic Monkeys", "Muse - Hysteria", "Tool - Schism", 
    "Rage Against The Machine - Killing In The Name", "Aerials by System of a Down", 
    "Bleed by Meshuggah", "Obzen by Meshuggah", "Empires Erased by Born of Osiris", 
    "Gods Amongst Men by Within the Ruins", "Why So Serious? by Hans Zimmer", 
    "Opening track to the Blade Runner 2049 OST", "Time by Hans Zimmer", 
    "Imperial March by John Williams", "Three Ralph’s by DJ Shadow", "Tearing Me Up by Bob Moses", 
    "Her by Vincent", "Windowlicker by Aphex Twin", "Come to Daddy by Aphex Twin", 
    "Can't Leave The Night by BADBADNOTGOOD", "Hey Now by London Grammar", "God Is A Woman by Ariana Grande", 
    "Therefore I Am by Billie Eilish", "Billie Eilish - Bad Guy", "The Weeknd - Blinding Lights", 
    "Dua Lipa - Don't Start Now", "Boss Mode by Knife Party", "Propane Nightmares by Pendulum", 
    "Stranger by Skrillex", "Doin' it Right by Daft Punk", "Bangarang by Skrillex", 
    "Flight of the Cosmic Hippo by Bela Fleck", "Morph The Cat by Donald Fagan", "So What by Miles Davis", 
    "Angel by Massive Attack", "Flashback by Fat Freddy's Drop", "Dread Lion by Lee \"Scratch\" Perry", 
    "Morning by Beck", "Fantasy by The XX", "Lateralus by Tool", "High All Day by Popcaan", 
    "Klapp Klapp by Little Dragon", "Electric Feel by MGMT", "A Thousand Years by Sting", 
    "Hurricane by Eprom", "Thanks to You by Boz Scaggs", "Bass Boom Bottom by Power Supply", 
    "Royals by Lorde", "Bassnectar - Bass Head", "Skrillex - Scary Monsters and Nice Sprites", 
    "Excision - X Rated", "Deadmau5 - Ghosts 'n' Stuff", "Zedd - Clarity", "Calvin Harris - I'm Not Alone", 
    "Partition by Beyoncé", "Frank Ocean - Nights", "The Weeknd - Starboy"
]

# Function to search for a song and get its video ID
def get_video_id(query):
    search_results = ytmusic.search(query, filter="songs", limit=1)
    if search_results:
        return search_results[0]['videoId']
    return None

# Get video IDs for all songs
video_ids = [get_video_id(song) for song in songs]
# Filter out None values in case some songs were not found
video_ids = [video_id for video_id in video_ids if video_id is not None]

# Create a new playlist
playlist_id = ytmusic.create_playlist("Songs to Test Bass and Sub Bass", "Playlist to test bass and sub bass in different genres")

# Add songs to the playlist
if video_ids:
    ytmusic.add_playlist_items(playlist_id, video_ids)

print(f"Playlist created successfully with ID: {playlist_id}")
