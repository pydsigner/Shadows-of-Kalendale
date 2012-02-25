# Text RPG Engine test
import random
import time
import textwrap

# Bonus feature for Unix users
try:
    import readline
except ImportError:
    # Sorry, Windows users!
    pass
    
# Since we have so many checks for this, we make a convenience variable
OP4 = list('1234')

HeroCmd = False
GameChoice = False
GameTurns = 0
AttackCmd = ""
HeroDmg = 0
MonsterDmg = 0

# All base stats for hero
HeroExperience = 0
HeroName = False
HeroGold = 15
HeroLevel = 1
HeroRace = False
HeroClass = False
HeroSTR = 3
HeroSTA = 3
HeroDEX = 3
HeroINT = 3
HeroAttack = 0
HeroSTRBonus = 0
HeroDEXBonus = 0
HeroINTBonus = 0
HeroBaseArmor = 0
HeroArmor = 0
HeroMagic = 4
HeroMaxMagic = 0
HeroBaseSpell = 0
HeroSpell = 6
HeroHealth = 1
HeroMaxHealth = 1
HeroBaseMinDmg = 1
HeroBaseMaxDmg = 3
HeroMinDmg = 1
HeroMaxDmg = 2
HeroMagicAttack = 0
TimeOfDayTimer = 180
TimeOfDay = "Daytime"
WeatherTimer = 60
CurrentWeather = 1
HeroBuffTimer = 0
HeroPoisonTimer = 1
HeroBuff = 0
HeroPoison = 0

AltCmd = {"north":"n", "south":"s", "east":"e", "west":"w", "up":"u", "down":"d",
          "inventory":"i", "inv":"i",
          'l': 'look',
          "look weapon prices":"weapon prices", "look armor prices":"armor prices", "look shield prices":"shield prices", "look training prices":"training prices",
          "quit":"q","suicide":"q","die":"q","exit":"q","save":"savegame"}

WeatherOptions = {0:["The sun begins to shine.", "The heat of the bright sun beats down on you."],
                  1:["Clouds begin to form.", "The sky is overcast with clouds."],
                  2:["It begins to rain.", "It's raining here."],
                  3:["Dark clouds begin to gather. You hear thunder in the distance.", "The rain is coming down in sheets.\nThunder and lightning envelope your senses."],
                  4:["You begin to be enveloped by a light mist.", "You are surrounded by thick fog."],
                  5:["The clouds in the sky begin to gather. You're able to see your breath.", "Thick flakes of white float down around you.\nYou feel the soft crunch of your feet on the snow."],
                  6:["The light of the moon begins to shine down around you.", "You are able to see the stars, bright as candles."]}                   

# Define the RoomNumber the player begins in
RoomNumberStart = 3
RoomNumber = False

# Declare what items slots are being used
WeaponSlot = 0
ArmorSlot = 0
ShieldSlot = 0

# Declare what the player starts with in their inventory list (as well as declaring inventory list)
Inventory = ["branch", "cloth vestments", "pretty stone", "red vial"]

# Hero Spells Inventory (SpellBook)
HeroSpells = []

# Declare what the user is wearing
ItemsWorn = []

# Declare what spell is chanted
SpellChanted = []

# Declare what buff the hero has
HeroBuff = []

# Declare what room numbers are shops and trainers
BlacksmithRooms = [5]
PawnshopRooms = [13]
ApothecaryRooms = [15]
ArcaneSpellshopRooms = [12]
DivineSpellshopRooms = [8]

FighterTrainerRooms = [1]
RogueTrainerRooms = [17]
SorcererTrainerRooms = [16]
ClericTrainerRooms = [8]

# Declare what rooms the player can be resurrected in
ResurrectionRooms = [8]

# Intro text
IntroText = ["Ever since you can remember, tales of fame and wealth have littered the taverns in every corner of the land. Filled with the sense of adventure, you packed your bag and began your journey to the city of Avalron. But misfortune struck along the way. You were robbed by bandits and left for dead. By luck of the Gods, a lone mysterious traveler found you and brought you to the city of Avalron, nursing you back to health. As sudden as the traveler appeared, he was gone, leaving you with a small purse of coins. You wake up in your small bed of hay, in an unused corner of the royal stables, finally ready to seek fame... and fortune..."]

# Dictionary for room descriptions
RoomDescription = {1:"Here appears to be the castle's armory. The royal guard, as well as the city militia, spend most of their time here practicing combat under careful watch of their trainers. You see a sign that says 'TRAINING PRICES'. The royal courtyard lies to the east.",
                   2:"You are in the royal courtyard. The main entrance to the keep lies to the north. A massive wooden door lined with large iron bars has it sealed tight. To the south, an open portculis gives access to the city. To the west you hear the sound of weapons clashing. To the east flows the sound of hooves on cobblestone.",
                   3:"The scent of manure and fresh hay fills your nostrils. Some of the greatest steeds in all the land of Kalendale are bred in these stables. To the west lies the royal courtyard.",
                   4:"The entrance to the crypt gives off a very different feeling, over the peace of the chapel to the south. A cold air rises from the steps leading down. Something dark... and foul... lies beneath.",
                   5:"The sound of a hammer on metal, along with the wind of the bellows fill your ears as you enter. The heat of the forge here, threatens to melt your skin. A blacksmith looks at you, nods to 3 signs on the wall and goes back to his work. The signs are titled: 'WEAPON PRICES', 'ARMOR PRICES', and 'SHIELD PRICES'. You see doors to the street at both the east and the south.",
                   6:"You are at north end of Royal Avenue.",
                   7:"Although small and quaint, the churchyard's well kept garden of flowers and hedges is pleasing to the eye. To the west lies the entrance to the castle. To the east is a small white chapel, with a holy cross perched atop its bell tower.",
                   8:"While the church is small, you feel a powerful sense of peace here. Candles along the wall give a colorful reflection on the stain glass windows. A priest here gives you a warm smile as he tends to his duties. Next to him on the wall is a parchment that reads: 'DIVINE SPELLS'. To the west lies the door to the churchyard. To the north lies the entrance to the crypts.",
                   9:"You are at the West Gate.",
                   10:"You are at the north end of Main Street that crosses Market Road.",
                   11:"You are at the east end of Market Road.",
                   12:"As soon as you enter the library, you are filled with the scent of ancient knowledge. Books, scrolls and manuscripts line the shelves as far as you can see. Some covered in mounds of dust, long forgotten. Some well used and well kept. A wise looking man with a long grey beard stands here, whom you can only assume is the Chanter. He looks at you with intelligent eyes and nods a warm greeting. Next to him is a sign with the label: 'ARCANE SPELLS'. To the south appears to be the Arcane Academy. There is an exit to the west that leads to the street.",
                   13:"Trinkets, jewels, and items of every kind line the shelves here. A shady looking character stands here, looking eager to see what you have to sell.",
                   14:"You are on Main Street.",
                   15:"You are at the Apothecary. You see a sign that says 'POTION PRICES'",
                   16:"You are at the Academy.",
                   17:"You are in the Thieves' Guild.",
                   18:"You are at the west end of Signature Way that crosses Main Street.",
                   19:"You are on Signature way.",
                   20:"You are near the east end of Signature Way.",
                   21:"You are at the East Gate.",
                   22:"You are at the South Gate.",
                   23:"You are in the City Jail. A spiral stone staircase leads down in to the dungeon depths.",
                   24:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   25:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   26:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   27:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   28:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   29:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   30:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   31:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   32:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   33:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   34:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   35:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   36:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   37:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   38:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   39:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   40:"You are in the Crypt. Beneath you lies steps leading even further in to the darkness.",
                   41:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   42:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   43:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   44:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   45:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   46:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   47:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   48:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   49:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   50:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   51:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   52:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   53:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   54:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   55:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   56:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   57:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   58:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   59:"You are in the Crypt. You hear distant sounds of moaning and wailing.",
                   60:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   61:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   62:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   63:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   64:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   65:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   66:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   67:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   68:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   69:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   70:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   71:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   72:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   73:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   74:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   75:"You are in a large room, deep wihin the Crypt.",
                   76:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   77:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   78:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   79:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   80:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   81:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   82:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   83:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   84:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   85:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   86:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   87:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   88:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   89:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   90:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   91:"You are deep within the Crypt. Undescribable sounds of horror echo through the chambers.",
                   92:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   93:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   94:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   95:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   96:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   97:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   98:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   99:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   100:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   101:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   102:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   103:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   104:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   105:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   106:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   107:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   108:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   109:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   110:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   111:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   112:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   113:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   114:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   115:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   116:"You are at the bottom of a spiral stone staircase. It appears this is where the city dungeons begin.",
                   117:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   118:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   119:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   120:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   121:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   122:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   123:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   124:"You are deep within the city dungeons. A trap door is open here, revealing a ladder leading further down.",
                   125:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   126:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   127:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   128:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   129:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   130:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   131:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   132:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   133:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   134:"It appears this dungeon passage has collapsed, cutting off access to the west.",
                   135:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   136:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   137:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   138:"You in the city dungeons. Torches line the walls to drive out the darkness. The walls are lined with mildew, as water from an unknown source blankets their exterior. Distant sounds of unfriendly creatures seem to hint that the city has no control over this area anymore.",
                   139:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   140:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   141:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   142:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   143:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   144:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   145:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   146:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   147:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   148:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   149:"The sewers appear to drain into an underground cavern. You see rocks that appear to allow you to descend into the depths below.",
                   150:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   151:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   152:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   153:"You are in the city sewers. Even rats seem to be trying to flee from the stench. You see a ladder leading up to a trap door.",
                   154:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   155:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   156:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   157:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   158:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   159:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   160:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   161:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   162:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   163:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   164:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   165:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   166:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   167:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   168:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   169:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   170:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   171:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   172:"You are in the city sewers. Even rats seem to be trying to flee from the stench.",
                   173:"You are in the city sewers. Even rats seem to be trying to flee from the stench."}

# Define the RoomIndex Dictionary {roomnumber:[n,s,e,w,u,d,show exits (1 = yes and 0 = no), combat area level spawn(0 = no combat spawn)]}
RoomIndex = {1:[0,0,2,0,0,0,0,0],
             2:[0,6,3,1,0,0,0,0],
             3:[0,0,0,2,0,0,0,0],
             4:[0,8,0,0,0,24,0,0],
             5:[0,10,6,0,0,0,0,0],
             6:[2,11,7,5,0,0,1,0],
             7:[0,0,8,6,0,0,0,0],
             8:[4,0,0,7,0,0,0,0],
             9:[0,0,10,0,0,0,1,0],
            10:[5,14,11,9,0,0,1,0],
            11:[6,15,12,10,0,0,1,0],
            12:[0,16,0,11,0,0,0,0],
            13:[0,17,14,0,0,0,0,0],
            14:[10,18,15,13,0,0,1,0],
            15:[11,19,16,14,0,0,1,0],
            16:[12,20,0,15,0,0,1,0],
            17:[13,0,0,0,0,0,1,0],
            18:[14,22,19,0,0,0,1,0],
            19:[15,0,20,18,0,0,1,0],
            20:[16,23,21,19,0,0,1,0],
            21:[0,0,0,20,0,0,1,0],
            22:[18,0,0,0,0,0,1,0],
            23:[20,0,0,0,0,116,1,0],
            24:[0,30,0,59,4,0,1,1],
            25:[54,31,26,24,0,0,1,1],
            26:[0,0,0,25,0,0,1,1],
            27:[57,0,28,0,0,0,1,1],
            28:[58,34,29,27,0,0,1,1],
            29:[0,0,30,28,0,0,1,1],
            30:[24,0,29,0,0,0,1,1],
            31:[25,36,32,0,0,0,1,1],
            32:[0,0,33,31,0,0,1,1],
            33:[0,0,0,32,0,0,1,1],
            34:[28,0,35,0,0,0,1,1],
            35:[0,0,0,34,0,0,1,1],
            36:[31,0,37,0,0,0,1,1],
            37:[0,0,38,36,0,0,1,1],
            38:[0,0,0,37,0,0,1,1],
            39:[0,41,0,0,0,0,1,1],
            40:[0,0,41,0,0,60,1,1],
            41:[39,45,0,40,0,0,1,1],
            42:[0,49,43,0,0,0,1,1],
            43:[0,50,44,42,0,0,1,1],
            44:[0,0,45,43,0,0,1,1],
            45:[41,0,46,44,0,0,1,1],
            46:[0,53,47,45,0,0,1,1],
            47:[0,0,0,46,0,0,1,1],
            48:[0,55,0,0,0,0,1,1],
            49:[42,0,0,0,0,0,1,1],
            50:[43,57,0,0,0,0,1,1],
            51:[0,58,0,0,0,0,1,1],
            52:[0,0,53,0,0,0,1,1],
            53:[46,0,0,52,0,0,1,1],
            54:[0,25,55,0,0,0,1,1],
            55:[48,0,56,54,0,0,1,1],
            56:[0,0,0,55,0,0,1,1],
            57:[50,27,0,0,0,0,1,1],
            58:[51,28,59,0,0,0,1,1],
            59:[0,0,24,58,0,0,1,1],
            60:[84,67,61,91,40,0,1,2],
            61:[0,0,62,60,0,0,1,2],
            62:[0,69,63,61,0,0,1,2],
            63:[87,0,0,62,0,0,1,2],
            64:[89,0,0,0,0,0,1,2],
            65:[90,70,0,0,0,0,1,2],
            66:[0,71,0,0,0,0,1,2],
            67:[60,72,68,0,0,0,1,2],
            68:[0,0,69,67,0,0,1,2],
            69:[62,74,0,73,0,0,1,2],
            70:[65,0,71,0,0,0,1,2],
            71:[66,0,72,70,0,0,1,2],
            72:[67,0,0,71,0,0,1,2],
            73:[0,75,74,0,0,0,1,2],
            74:[69,0,0,73,0,0,1,2],
            75:[73,0,0,0,0,0,1,0],
            76:[0,82,0,0,0,0,1,2],
            77:[0,83,78,0,0,0,1,2],
            78:[0,84,79,77,0,0,1,2],
            79:[0,85,80,78,0,0,1,2],
            80:[0,86,0,79,0,0,1,2],
            81:[0,87,0,0,0,0,1,2],
            82:[76,90,0,0,0,0,1,2],
            83:[77,0,0,0,0,0,1,2],
            84:[78,60,0,0,0,0,1,2],
            85:[79,0,86,0,0,0,1,2],
            86:[80,0,0,85,0,0,1,2],
            87:[81,63,88,0,0,0,1,2],
            88:[0,0,0,87,0,0,1,2],
            89:[0,64,90,0,0,0,1,2],
            90:[82,65,91,89,0,0,1,2],
            91:[0,0,60,90,0,0,1,2],
            92:[0,99,93,0,0,0,1,3],
            93:[0,0,94,92,0,0,1,3],
            94:[0,0,95,93,0,0,1,3],
            95:[0,102,96,94,0,0,1,3],
            96:[0,0,97,95,0,0,1,3],
            97:[0,0,98,96,0,0,1,3],
            98:[0,0,0,97,0,0,1,3],
            99:[92,0,100,0,0,0,1,3],
            100:[0,0,101,99,0,0,1,3],
            101:[0,108,0,100,0,0,1,3],
            102:[95,190,103,0,0,0,1,3],
            103:[0,110,104,102,0,0,1,3],
            104:[0,111,105,103,0,0,1,3],
            105:[0,112,0,104,0,0,1,3],
            106:[0,0,107,0,0,0,1,3],
            107:[0,0,108,106,0,0,1,3],
            108:[101,0,0,107,0,0,1,3],
            109:[102,116,0,0,0,0,1,3],
            110:[103,0,0,0,0,0,1,3],
            111:[104,0,0,0,0,0,1,3],
            112:[105,0,0,0,0,0,1,3],
            113:[0,0,114,0,0,0,1,3],
            114:[0,0,115,113,0,0,1,3],
            115:[0,0,116,114,0,0,1,3],
            116:[109,123,117,115,23,0,1,3],
            117:[0,0,118,116,0,0,1,3],
            118:[0,125,119,117,0,0,1,3],
            119:[0,0,0,118,0,0,1,3],
            120:[0,127,0,0,0,0,1,3],
            121:[0,128,0,0,0,0,1,3],
            122:[0,129,0,0,0,0,1,3],
            123:[116,130,0,0,0,0,1,3],
            124:[0,131,0,0,0,153,1,3],
            125:[118,0,126,0,0,0,1,3],
            126:[0,133,0,125,0,0,1,3],
            127:[120,0,128,0,0,0,1,3],
            128:[121,0,129,127,0,0,1,3],
            129:[122,0,130,128,0,0,1,3],
            130:[123,136,0,129,0,0,1,3],
            131:[124,137,132,0,0,0,1,3],
            132:[0,0,133,131,0,0,1,3],
            133:[126,138,0,132,0,0,1,3],
            134:[0,0,135,0,0,0,1,3],
            135:[0,0,136,134,0,0,1,3],
            136:[130,0,0,135,0,0,1,3],
            137:[131,0,0,0,0,0,1,3],
            138:[133,0,0,0,0,0,1,3],
            139:[0,142,0,0,0,0,1,4],
            140:[0,143,141,0,0,0,1,4],
            141:[0,144,0,140,0,0,1,4],
            142:[139,0,143,0,0,0,1,4],
            143:[140,147,0,142,0,0,1,4],
            144:[141,0,0,0,0,0,1,4],
            145:[0,151,146,0,0,0,1,4],
            146:[0,0,0,145,0,0,1,4],
            147:[143,153,148,0,0,0,1,4],
            148:[0,154,0,147,0,0,1,4],
            149:[0,155,0,0,0,0,1,4],
            150:[0,0,151,0,0,0,1,4],
            151:[145,0,152,150,0,0,1,4],
            152:[0,158,0,151,0,0,1,4],
            153:[147,159,154,124,124,0,1,4],
            154:[148,160,0,153,0,0,1,4],
            155:[149,0,156,0,0,0,1,4],
            156:[0,162,0,155,0,0,1,4],
            157:[0,164,158,0,0,0,1,4],
            158:[152,165,0,157,0,0,1,4],
            159:[153,166,0,0,0,0,1,4],
            160:[154,0,0,0,0,0,1,4],
            161:[0,168,162,0,0,0,1,4],
            162:[156,169,0,161,0,0,1,4],
            163:[0,0,164,0,0,0,1,4],
            164:[157,170,0,163,0,0,1,4],
            165:[158,0,166,0,0,0,1,4],
            166:[159,0,167,165,0,0,1,4],
            167:[0,0,168,166,0,0,1,4],
            168:[161,173,0,167,0,0,1,4],
            169:[162,0,0,0,0,0,1,4],
            170:[164,0,0,0,0,0,1,4],
            171:[0,0,172,0,0,0,1,4],
            172:[0,0,173,171,0,0,1,4],
            173:[168,0,0,172,0,0,1,4]}

# Populate the rooms dictonary matrix from 1 to ~
RoomInv = {1:[],
           2:["lich","guardsman"],
           3:["pile of hay"],
           4:[],
           5:[],
           6:[],
           7:[],
           8:[],
           9:["guardsman"],
           10:[],
           11:[],
           12:[],
           13:[],
           14:[],
           15:[],
           16:[],
           17:[],
           18:[],
           19:[],
           20:[],
           21:["guardsman"],
           22:["guardsman"],
           23:[],
           24:["corpse"],
           25:[],
           26:[],
           27:[],
           28:[],
           29:[],
           30:[],
           31:[],
           32:[],
           33:[],
           34:[],
           35:[],
           36:[],
           37:[],
           38:[],
           39:[],
           40:["simple chest"],
           41:[],
           42:[],
           43:[],
           44:[],
           45:[],
           46:[],
           47:[],
           48:[],
           49:[],
           50:[],
           51:[],
           52:[],
           53:[],
           54:[],
           55:[],
           56:[],
           57:[],
           58:[],
           59:[],
           60:[],
           61:[],
           62:[],
           63:[],
           64:[],
           65:[],
           66:[],
           67:[],
           68:[],
           69:[],
           70:[],
           71:[],
           72:[],
           73:[],
           74:[],
           75:["lich","chest"],
           76:[],
           77:[],
           78:[],
           79:[],
           80:[],
           81:[],
           82:[],
           83:[],
           84:[],
           85:[],
           86:[],
           87:[],
           88:[],
           89:[],
           90:[],
           91:[],
           92:[],
           93:[],
           94:[],
           95:[],
           96:[],
           97:[],
           98:[],
           99:[],
           100:[],
           101:[],
           102:[],
           103:[],
           104:[],
           105:[],
           106:[],
           107:[],
           108:[],
           109:[],
           110:[],
           111:[],
           112:[],
           113:[],
           114:[],
           115:[],
           116:[],
           117:[],
           118:[],
           119:[],
           120:[],
           121:[],
           122:[],
           123:[],
           124:[],
           125:[],
           126:[],
           127:[],
           128:[],
           129:[],
           130:[],
           131:[],
           132:[],
           133:[],
           134:["rubble"],
           135:[],
           136:[],
           137:["orc","chest"],
           138:[],
           139:[],
           140:[],
           141:[],
           142:[],
           143:[],
           144:[],
           145:[],
           146:[],
           147:[],
           148:[],
           149:[],
           150:[],
           151:[],
           152:[],
           153:[],
           154:[],
           155:[],
           156:[],
           157:[],
           158:[],
           159:[],
           160:[],
           161:[],
           162:[],
           163:["dire rat","large chest"],
           164:[],
           165:[],
           166:[],
           167:[],
           168:[],
           169:[],
           170:[],
           171:[],
           172:[],
           173:[]}


# Build monster list with stats-
# "monster name":[MonsterHealth, Min Stat, Max Stat, Min Dmg, Max Dmg, MonsterArmor, KillExperience, monster difficulty level (zero for non spawn)]
#
# level 0 humanoid
MonsterIndex = {# crypts level 1
                "skeleton warrior":[10,10,12,2,6,13,8,1],
                "large skeleton":[13,10,12,2,6,13,10,1],
                "kobold zombie":[14,8,11,2,6,9,8,1],
                "human zombie":[17,8,12,2,6,13,12,1],
                "ghoul":[13,10,12,2,7,12,10,1],

                # crypts level 2
                "large skeleton warrior":[13,12,14,3,7,13,14,2],
                "wight":[26,12,14,2,5,13,18,2],
                "human zombie":[17,8,12,2,6,13,12,2],
                "ghoul":[13,10,12,2,7,12,10,2],
                "shadow":[13,12,14,2,7,14,14,2],

                # dungeons level 1
                "rogue":[20,14,16,4,8,18,18,3],
                "gnome":[14,14,14,4,6,16,14,3],
                "goblin":[14,14,14,4,6,16,14,3],
                "bandit":[18,14,16,4,8,18,16,3],

                # sewers level 1
                "kobold":[18,12,14,4,8,18,16,4],
                "giant rat":[22,12,14,6,8,16,20,4],
                "slime":[30,14,16,4,8,18,24,4],

                # boss monsters
                "guardsman":[200,18,18,20,30,50,500,0],
                "vampire":[29,14,16,6,10,15,50,0],
                "lich":[29,16,16,6,10,15,50,0],
                "orc":[32,16,16,6,12,17,65,0],
                "dire rat":[36,18,18,8,12,18,80,0]}

# Items that can be searched for loot or gold
SolidItem = ("corpse","rubble","pile of hay")

# Items that can be searched but not picked up with rare loot or extra gold
SolidItem2 = ("simple chest","large chest","chest")

# Create a non wearable item list- "item name":[buy price, sell price, minimum level they appear at]
LootItems = {"pretty rock":[1,1,1,"It's a pretty rock. Looks like it could be of some value."],
             "pretty stone":[1,2,1,"It's a pretty stone. Looks like it could be of some value."],
             "polished rock":[1,3,1,"It's a polished rock. Looks like it could be of some value."],
             "polished stone":[1,4,1,"It's a polished stone. Looks like it could be of some value."],
             "citrine":[1,5,1,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "rusty shortsword":[1,2,1,"This small sword looks like it has seen better days."],
             "polished citrine":[1,6,2,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "garnet":[1,8,2,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished garnet":[1,10,2,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "onyx":[1,12,3,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished onyx":[1,13,3,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "moonstone":[1,15,3,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished moonstone":[1,17,4,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "opal":[1,20,4,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished opal":[1,25,4,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "obsidian":[1,30,4,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished obsidian":[1,33,4,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "topaz":[1,35,4,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished topaz":[1,40,5,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "peridot":[1,45,5,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished peridot":[1,47,5,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "aquamarine":[1,50,5,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished aquamarine":[1,53,6,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "agate":[1,55,6,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished agate":[1,57,6,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "bloodstone":[1,60,6,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished bloodstone":[1,63,7,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "jade":[1,65,7,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished jade":[1,67,7,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "amethyst":[1,70,7,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "polished amethyst":[1,72,7,"It's some sort of semi-precious stone. Looks like it could be of some value."],
             "pearl":[1,75,8,"You're not sure how the this beautiful round pearl go here, but you can be sure it will get a good price."],
             "gold nugget":[1,80,8,"This large nugget of gold should fetch a good return, if sold."],
             "ruby":[1,85,9,"This red ruby appears to be almost on fire as the light hits it. It should fetch a good price."],
             "emerald":[1,90,9,"The emerald glows green like nothing you've ever seen. There's not many out there that wouldn't give a good price for it."],
             "black pearl":[1,95,10,"An extremely rare pearl. It shines black like obsidian, but seems to pulse with white light within."],
             "diamond":[1,100,10,"The jewel of all jewels. It's sparkle promises great wealth."]}

# for reasons unknown, rare loot items must be listed by level in decending order if there are duplicates (something to do with the search function)
RareLootItems = {"bone armor":[800,130,4,""],
                 "crystal longsword":[500,90,3,""],
                 "fine robe":[300,40,2,""],
                 "fine shortsword":[150,30,1,""],
                 "red vial":[100,10,0,""]}

# Declare weapons with stats-  "weapon name":[buy price, sell price, minimum damage, maximum damage, attack bonus, if item can be bought (0 = no, 1 = yes), type (0 = universal, 1 = light, 2 = regular), edge (0 = bladed, 1 = blunt), hands (0 = dual wield, 1 = 1h, 2 = 2h)]
WeaponStats = {"branch":[0,0,1,3,0,0,0,1,1,"You believe this will do no more damage than your fists, but it sure feels nice to have SOMETHING in your hand."],
               "quarterstaff":[20,1,1,6,0,1,0,1,2,"Although simple and cheap, this two-handed staff could pack quite a punch"],
               "dagger":[10,1,1,4,0,1,1,0,0,"This weapon is small, sharp, and easy to conceal."],
               "rusty shortsword":[1,2,1,4,0,0,1,0,0,"The shortsword is rusted and nicked, and looks like it would only be a slight improvement over your fists."],
               "club":[5,1,1,4,0,1,2,1,1,"Made of hard wood, the perfect blunt weapon, for those on a budget."],
               "spiked club":[10,1,2,4,0,1,2,0,1,"An improvement over the standard club design. This will ensure that blood is drawn upon impact."],
               "axe":[20,2,1,5,0,1,2,0,1,"Favored by the dwarves. The hard wooden handly is fitted well in to the metal wedge. Simple, yet deadly."],
               "heavy flail":[30,3,1,8,0,1,2,1,2,"A weighted ball attached by chain to a long sturdy handle.\nBuilt for two hands, this weapon strikes fear in to its opponents."],
               "mace":[35,4,1,5,0,1,2,1,1,"Favored by holy warriors. The weight will crush an opponents skull, and the bones of the undead."],
               "shortsword":[60,6,1,6,0,0,1,0,0,"It's a shortsword"],
               "fine shortsword":[150,15,1,7,0,1,1,0,0,"It's a well crafted shortsword"],
               "longsword":[80,8,1,8,0,1,2,0,1,"It's a longsword"],
               "battle axe":[100,10,1,8,0,1,2,0,1,"It's a battle axe"],
               "bastard sword":[120,12,1,10,0,1,2,0,1,"Larger than a longsword, but still made for one hand.\n It is not built for the weak."],
               "greatsword":[140,14,2,12,0,1,2,0,2,"A large, two-handed sword."],
               "crystal longsword":[500,90,2,12,0,0,2,0,1,"The size of a standard longsword, but it appears to be almost made of glass."]}

# Declare armor and shields with stats-  "item name":[buy price, sell price, armor value, health bonus, if item can be bought (0 = no, 1 = yes),type (0 = universal, 1 = cloth, 2 = light, 3 = medium, 4 = heavy)] 
ArmorStats = {"cloth vestments":[1,1,0,0,0,0,"These clothes look like they won't do much except preserve modesty."],
              "robe":[1,1,1,0,1,1,"A simple robe that will offer protection from the elements, but not against enemy attacks."],
              "padded armor":[10,1,3,0,1,2,"Made of heavy wool and canvas, this will offer limited protection against enemies."],
              "leather armor":[30,3,4,0,1,2,"This armor is made of hard boiled leather."],
              "scalemail":[50,5,5,0,1,3,"Small metal plates are attached to a leather shell. Like a large gutted metal fish."],
              "chainmail":[150,15,6,0,1,3,"A heavy robe made of metal links, designed to ward off bladed attacks."],
              "halfplate":[600,60,8,0,1,4,"Fashioned metal plates are formed to cover the shoulders, torso and upper legs, while chainmail protects the flexible areas."],
              "fullplate":[1500,150,10,0,1,4,"Lightweight forged steel covers all areas of the body offering maximum protection."],
              "bone armor":[800,130,9,0,0,2,"Made of pure bone, this armor appears to as strong as platemail, but feels lighter than leather."]}

ShieldStats = {"buckler":[20,2,1,0,1,2,"A small wooden shield with a metal handle."],
               "wooden shield":[20,2,2,0,1,2,"Larger than a buckler, and offering slightly more protection."],
               "round shield":[35,4,3,0,1,3,"A mid sized round shield made of wood and covered in thin steel."],
               "heater shield":[60,6,4,0,1,3,"A mid sized shield made of forged steel."],
               "kite shield":[100,10,5,0,1,4,"A large shield made of forged steel."],
               "tower shield":[150,15,6,0,1,4,"A massive shield that can offer protection for the entire body."]}

# potions {"item name":[buy price, sell price, can be purchased (0 = no, 1 = yes)]}
UseableItems = {"red vial":[100,10,1,"This glass vial contains a glowing red liquid."],
                "blue vial":[50,5,1,"This glass vial containts a glowing blue liquid."],
                "green vial":[100,10,1,"This glass vial contains a glowing green liquid."],
                "scroll":[20,2,1,"The runes on this scroll glow with power."]}

# List of offensive weapon spells.
#{"Spell Name":[Buy Cost, Mana Cost, Minimum Damage, Maximum Damage, turns (0 is instant), level available at (0 is available upon character creation]
ArcaneBattleSpells = {"magic missle":[10,1,2,8,0,0],
                      "shocking grasp":[30,2,1,12,0,1]}

DivineBattleSpells = {"smite":[20,1,1,7,0,1]}

# List of healing spells
#{"spell name":[buy cost, mana cost, minimum heal, maximum heal, turns (0 is instant), level available at (0 is available upon character creation)]
ArcaneHealingSpells = {"vampire touch":[100,4,1,5,0,1]}
DivineHealingSpells = {"cure light wounds":[10,2,4,10,0,0]}

# timered buff spells
#{"spell name":[buy cost, mana cost, min dmg buff, max dmg buff, armor buff, attack buff, turns timer, level available at (0 is available upon character creation)]
ArcaneBuffSpells = {"arcane armor":[40,2,0,0,3,0,30,2]}
DivineBuffSpells = {"divine attack":[40,2,0,0,0,2,20,2]}

# Specialty spells (non combat)
SpecialArcane = ["mark","teleport","invisible"]
SpecialDivine = []

#
# Function to save the game from variables
#
def SaveGame(HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns):
    import pickle
    try:
        SaveInfo = (HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns)
        with open('char.sav', 'wb') as output:
            pickle.dump(SaveInfo, output)
        print "\nThe game is now saved..."
    except:
        print"\nError! Possible issue: file permissions..."

#
# Function to load the game
#
def LoadGame(HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns):
    import pickle
    try:
        with open('char.sav', 'rb') as pkl_file:
            HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns = \
            pickle.load(pkl_file)
        return (HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns)
    except:
        print("\nError! Possible issue: no savegame present. Starting new game...")
        NewGame(RoomNumberStart,HeroName,IntroText)

# Calls the list of commands available in the game
def CmdHelp():
    print "\nAvailable commands are:\n"
    print "north (n)    south (s)     east (e)       west (w)"
    print "up (u)       down (d)"
    print "stats        status        spellbook      inventory (i)"
    print "look         rest          chant          cast"
    print "train        savegame      help           quit"
    print "time"
    print "get [item]   drop [item]   equip [item]   remove [item]"
    print "buy [item]   sell [item]   search [item]  look [item]"
    print "use [item]   attack [monster]"
    print "type 'r' to execute last typed command"
    
# Function to roll stats for hero creation
def RollStats(SpellChanted,HeroSpells,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroMaxHealth,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroSpell):

    ConfirmInput = ""
    ChooseInput = 0
    HeroRace = ""
    HeroClass = ""
    
    while ConfirmInput != "y":
        HeroSTR = random.randint(3,18)
        HeroSTA = random.randint(3,18)
        HeroDEX = random.randint(3,18)
        HeroINT = random.randint(3,18) #Intellect instead of MIND
        print "\nRolling Stats:\n"
        print "  Strength:", HeroSTR
        print "   Stamina:", HeroSTA
        print " Dexterity:", HeroDEX
        print " Intellect:", HeroINT
        print
        ConfirmInput = raw_input("Keep these stats? (Y/N): ").lower()
    print
    ConfirmInput = ""
    
    while ConfirmInput != "y":
        while ChooseInput not in OP4:
            print "Races:\n"
            print "1) Human"
            print "2) Elf"
            print "3) Dwarf"
            print "4) Halfling"
            print
            ChooseInput = raw_input("Please pick a race (1-4): ")
            if ChooseInput == "1":
                HeroRace = "Human"
            elif ChooseInput == "2":
                HeroRace = "Elf"
            elif ChooseInput == "3":
                HeroRace = "Dwarf"
            elif ChooseInput == "4":
                HeroRace = "Halfling"
            else:
                print "\nPlease pick a valid race...\n"
                break    
            print "\nYou have chosen:", HeroRace    
            ConfirmInput = raw_input("\nIs this correct? (Y/N): ").lower()
    print
    ChooseInput = ConfirmInput = ""
    while ConfirmInput != "y":
        while ChooseInput not in OP4:
            print "Classes:\n"
            print "1) Fighter (fully functional)"
            print "2) Rogue (incomplete)"
            print "3) Sorcerer (fully functional - limited spells)"
            print "4) Cleric (fully functional - limited spells)"
            print
            ChooseInput = raw_input("Please pick a class (1-4): ")
            if ChooseInput == "1":
                HeroClass = "Fighter"
            elif ChooseInput == "2":
                HeroClass = "Rogue"
            elif ChooseInput == "3":
                HeroClass = "Sorcerer"
            elif ChooseInput == "4":
                HeroClass = "Cleric"
            else:
                print "\nPlease pick a valid class...\n"
                continue
            print "\nYou have chosen:", HeroClass
            ConfirmInput = raw_input("\nIs this correct? (Y/N): ").lower()
    print
            
    HeroSTRBonus = (HeroSTR - 10) / 2
    HeroDEXBonus = (HeroDEX - 10) / 2
    HeroINTBonus = (HeroINT - 10) / 2

    if HeroRace == "Human":
        HeroSTR += 2
    elif HeroRace == "Elf":
        HeroINT += 2
    elif HeroRace == "Dwarf":
        HeroSTA += 2
    elif HeroRace == "Halfling":
        HeroDEX += 2

    HealthRoll = random.randint(1,6)
    HeroMaxHealth = HeroSTA + HealthRoll + 5
    HeroAttack = HeroSTRBonus + HeroLevel
    HeroBaseSpell = HeroINTBonus + HeroLevel
    HeroBaseArmor = HeroDEXBonus + 10
    HeroMaxMagic = (HeroINT / 2) + 5

    if HeroClass == "Fighter":
        HeroBaseMinDmg = HeroBaseMinDmg + 1
        HeroBaseSpell = 0
        HeroMaxMagic = 0
    elif HeroClass == "Rogue":
        HeroBaseArmor = HeroBaseArmor + 1
        HeroBaseSpell = 0
        HeroMaxMagic = 0
    elif HeroClass == "Sorcerer":
        HeroMaxMagic = HeroMaxMagic + 4
        HeroSpells = ["magic missle"]
        SpellChanted = ["magic missle"]
        HeroSpell = HeroBaseSpell
        HeroBaseSpell =+ ArcaneBattleSpells[SpellChanted[0]][2]
        HeroSpell =+ ArcaneBattleSpells[SpellChanted[0]][3]
    elif HeroClass == "Cleric":
        HeroBaseSpell = HeroBaseSpell + 1
        HeroSpells = ["cure light wounds"]
        SpellChanted = ["cure light wounds"]
        HeroSpell = HeroBaseSpell
    HeroHealth = HeroMaxHealth

    # last numbers based on 1d3 fists
    HeroBaseMinDmg += HeroSTRBonus + 1
    HeroBaseMaxDmg = HeroBaseMinDmg + 3
    if HeroBaseMinDmg < 0:
        HeroBaseMinDmg = 0
    HeroMinDmg = HeroBaseMinDmg
    HeroMaxDmg = HeroBaseMaxDmg

    return (SpellChanted,HeroSpells,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroMaxHealth,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroSpell)    

# Displays the stats of the player
def HeroStats(HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroExperience,HeroGold,HeroName):
    print
    print "          Name:", HeroName
    print "          Race:", HeroRace
    print "         Class:", HeroClass
    print "         Level:", HeroLevel
    print "    Experience:", HeroExperience
    print "      Strength:", HeroSTR
    print "       Stamina:", HeroSTA
    print "     Dexterity:", HeroDEX
    print "     Intellect:", HeroINT

def HeroStatus (HeroPoisonTimer,HeroLevel,HeroHealth,HeroMaxHealth,HeroMagic,HeroMaxMagic,HeroArmor,HeroAttack,HeroMinDmg,HeroMaxDmg,HeroBaseSpell,HeroSpell,SpellChanted,ItemsWorn):
    print
    print "         Health:", HeroHealth, "/", HeroMaxHealth
    print "           Mana:", HeroMagic, "/", HeroMaxMagic
    print "        Defence:", HeroArmor
    print "  Attack Rating:", HeroAttack
    print "   Melee Damage:", HeroMinDmg, "/", HeroMaxDmg
    print "   Spell Damage:", (HeroBaseSpell * HeroLevel), "/", (HeroSpell * HeroLevel) 
    print " Equipped Items:", ", ".join(ItemsWorn)
    print "  Chanted Spell:", ", ".join(SpellChanted)
    if HeroPoisonTimer > 0:
        print " You are suffering the effects of poison."

# Prints text when you try and go somewhere you can't
def WallBump():
    print
    WallBumpChoice = random.randint(1,3)
    if WallBumpChoice == 1:
        print "You cannot go in that direction."
    elif WallBumpChoice == 2:
        print "Your path is blocked."
    elif WallBumpChoice == 3:
        print "Try a different way if you actually want to GO somewhere."
        
# Function to display training prices
def TrainPrice(RoomNumber):
    if RoomNumber in FighterTrainerRooms or RoomNumber in RogueTrainerRooms or RoomNumber in SorcererTrainerRooms or RoomNumber in ClericTrainerRooms:
        print
        print "     Level:  Experience:  Gold Cost:"
        print "         1            0           0 "
        print "         2         1000         100 "
        print "         3         2000         500 "
        print "         4         4000        1000 "
        print "         5         8000        2000 "
        print "         6        15000        3000 "
        print "         7        30000        4000 "
        print "         8        60000        5000 "
        print "         9       125000        6000 "
        print "        10       250000        7000 "
    else:
        print "\nYou can't do that here..."
        
def HeroTrain(RoomNumber,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroGold,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMaxMagic,HeroSpell):
    print

# Fighter Training    
    if RoomNumber in FighterTrainerRooms and HeroClass == "Fighter" or RoomNumber in ClericTrainerRooms and HeroClass == "Cleric" or RoomNumber in SorcererTrainerRooms and HeroClass == "Sorcerer" or RoomNumber in RogueTrainerRooms and HeroClass == "Rogue": 
        # level 2
        if HeroLevel == 1 and HeroExperience >= 1000 and HeroGold >= 100:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            HeroHealth = HeroMaxHealth
            HeroGold = HeroGold - 100
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"
            
        # level 3    
        elif HeroLevel == 2 and HeroExperience >= 2000 and HeroGold >= 500:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            StatIncrease = False
            while StatIncrease not in OP4:
                print "Your current stats:\n"
                print " Strength:", HeroSTR
                print "  Stamina:", HeroSTA
                print "Dexterity:", HeroDEX
                print "Intellect:", HeroINT
                print
                print "1) Strength"
                print "2) Stamina"
                print "3) Dexterity"
                print "4) Intellect\n"
                StatIncrease = raw_input("Choose a stat you would like to increase (1-4):")
                if StatIncrease == "1":
                    HeroSTR += 1
                    HeroSTRBonus = (HeroSTR - 10) / 2
                    print "\nYou feel stronger...\n"
                    break
                elif StatIncrease == "2":
                    HeroSTA += 1
                    HeroMaxHealth = HeroMaxHealth + 1
                    print "\nYou feel sturdier...\n"
                    break
                elif StatIncrease == "3":
                    HeroDEX += 1
                    HeroDEXBonus = (HeroDEX - 10) / 2
                    print "\nYou feel more agile...\n"
                    break
                elif StatIncrease == "4":
                    HeroINT += 1
                    HeroINTBonus = (HeroINT - 10) / 2
                    print "\nYou feel more intelligent...\n"
                    break
                else:
                    print "\nThat is not a valid choice...\n"
            StatIncrease = False
            HeroHealth = HeroMaxHealth
            HeroGold = HeroGold - 500
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"
            
        # level 4    
        elif HeroLevel == 3 and HeroExperience >= 4000 and HeroGold >= 1000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            HeroHealth = HeroMaxHealth
            HeroGold -= 1000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"
            
        # level 5      
        elif HeroLevel == 4 and HeroExperience >= 8000 and HeroGold >= 2000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            HeroHealth = HeroMaxHealth
            if HeroClass == "Fighter":
                HeroAttack += 1
                HeroMinDmg += 1
                HeroMaxDmg += 1
                HeroBaseMinDmg += 1
                HeroBaseMaxDmg += 1
            HeroGold = HeroGold - 2000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"

        # level 6      
        elif HeroLevel == 5 and HeroExperience >= 15000 and HeroGold >= 3000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            StatIncrease = False
            while StatIncrease not in OP4:
                print "Your current stats:\n"
                print " Strength:", HeroSTR
                print "  Stamina:", HeroSTA
                print "Dexterity:", HeroDEX
                print "Intellect:", HeroINT
                print
                print "1) Strength"
                print "2) Stamina"
                print "3) Dexterity"
                print "4) Intellect\n"
                StatIncrease = raw_input("Choose a stat you would like to increase (1-4):")
                if StatIncrease == "1":
                    HeroSTR += 1
                    HeroSTRBonus = (HeroSTR - 10) / 2
                    print "\nYou feel stronger...\n"
                    break
                elif StatIncrease == "2":
                    HeroSTA += 1
                    HeroMaxHealth = HeroMaxHealth + 1
                    print "\nYou feel sturdier...\n"
                    break
                elif StatIncrease == "3":
                    HeroDEX += 1
                    HeroDEXBonus = (HeroDEX - 10) / 2
                    print "\nYou feel more agile...\n"
                    break
                elif StatIncrease == "4":
                    HeroINT += 1
                    HeroINTBonus = (HeroINT - 10) / 2
                    print "\nYou feel more intelligent...\n"
                    break
                else:
                    print "\nThat is not a valid choice...\n"
            StatIncrease = False
            HeroHealth = HeroMaxHealth
            HeroGold = HeroGold - 3000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"

        # level 7      
        elif HeroLevel == 6 and HeroExperience >= 30000 and HeroGold >= 4000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            HeroHealth = HeroMaxHealth
            HeroGold = HeroGold - 4000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"

        # level 8      
        elif HeroLevel == 7 and HeroExperience >= 60000 and HeroGold >= 5000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            HeroHealth = HeroMaxHealth
            HeroGold = HeroGold - 5000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"

        # level 9      
        elif HeroLevel == 8 and HeroExperience >= 125000 and HeroGold >= 6000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            StatIncrease = False
            while StatIncrease not in OP4:
                print "Your current stats:\n"
                print " Strength:", HeroSTR
                print "  Stamina:", HeroSTA
                print "Dexterity:", HeroDEX
                print "Intellect:", HeroINT
                print
                print "1) Strength"
                print "2) Stamina"
                print "3) Dexterity"
                print "4) Intellect\n"
                StatIncrease = raw_input("Choose a stat you would like to increase (1-4):")
                if StatIncrease == "1":
                    HeroSTR += 1
                    HeroSTRBonus = (HeroSTR - 10) / 2
                    print "\nYou feel stronger...\n"
                    break
                elif StatIncrease == "2":
                    HeroSTA += 1
                    HeroMaxHealth = HeroMaxHealth + 1
                    print "\nYou feel sturdier...\n"
                    break
                elif StatIncrease == "3":
                    HeroDEX += 1
                    HeroDEXBonus = (HeroDEX - 10) / 2
                    print "\nYou feel more agile...\n"
                    break
                elif StatIncrease == "4":
                    HeroINT += 1
                    HeroINTBonus = (HeroINT - 10) / 2
                    print "\nYou feel more intelligent...\n"
                    break
                else:
                    print "\nThat is not a valid choice...\n"
            StatIncrease = False
            HeroHealth = HeroMaxHealth
            HeroGold = HeroGold - 6000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"

        # level 10      
        elif HeroLevel == 9 and HeroExperience >= 250000 and HeroGold >= 7000:
            HeroLevel += 1
            HeroAttack += 1
            HeroMaxHealth += random.randint(1,6)
            HeroHealth = HeroMaxHealth
            if HeroClass == "Fighter":
                HeroAttack += 1
                HeroMinDmg += 1
                HeroMaxDmg += 1
                HeroBaseMinDmg += 1
                HeroBaseMaxDmg += 1
            HeroGold = HeroGold - 7000
            print "After spending time with the trainer, you feel more proficient."
            print "You have attained level", HeroLevel, "!"
        else:
            print "The trainer looks you over. He then opens his mouth and says:"
            print "'Looks like you don't meet the requirements to train. \nLook at the sign again...'"
            
    elif RoomNumber in FighterTrainerRooms and HeroClass != "Fighter":
        print "The trainer looks you over and says: 'I only train Fighters'"
    elif RoomNumber in ClericTrainerRooms and HeroClass != "Cleric":
        print "The trainer looks you over and says: 'I only train Clerics'"
    elif RoomNumber in SorcererTrainerRooms and HeroClass != "Sorcerer":
        print "The trainer looks you over and says: 'I only train Sorcerers'"
    elif RoomNumber in RogueTrainerRooms and HeroClass != "Rogue":
        print "The trainer looks you over and says: 'I only train Rogues'"
    else:
        print "You can't do that here..."

    return(HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroGold,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMaxMagic,HeroSpell)

# timer to determine weather, hero buffs, poisons, and gameturns in general
def TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber):

    # gameturns timer
    GameTurns += 1

    # buff timer
    if HeroBuffTimer > 1:
        HeroBuffTimer -= 1
    elif HeroBuffTimer == 1:
        if HeroClass == "Cleric":
            HeroMinDmg = HeroMinDmg - DivineBuffSpells[[HeroBuff][1]][2]
            HeroMaxDmg = HeroMaxDmg - DivineBuffSpells[[HeroBuff][1]][3]
            HeroArmor = HeroArmor - DivineBuffSpells[[HeroBuff][1]][4]
            HeroAttack = HeroAttack - DivineBuffSpells[[HeroBuff][1]][5]
            HeroBuff = []
        elif HeroClass == "Sorcerer":
            HeroMinDmg = HeroMinDmg - ArcaneBuffSpells[[HeroBuff][1]][2]
            HeroMaxDmg = HeroMaxDmg - ArcaneBuffSpells[[HeroBuff][1]][3]
            HeroArmor = HeroArmor - ArcaneBuffSpells[[HeroBuff][1]][4]
            HeroAttack = HeroAttack - ArcaneBuffSpells[[HeroBuff][1]][5]
            HeroBuff = []
        print "\n A magical effect has dissipated."
        HeroBuffTimer -= 1

    # poison timer
    if HeroPoisonTimer > 1:
        HeroHealth -= 1
        print "\n You suffered some damage from poison."
        HeroPoisonTimer -= 1
    elif HeroPoisonTimer == 1:
        print "\n Time has released the poison from your body."
        HeroPoisonTimer -= 1
        

    # weather timer
    if WeatherTimer > 0:
        WeatherTimer -= 1

    # time of day timer    
    if TimeOfDayTimer > 0:
        TimeOfDayTimer -= 1    

    # timer to change to and from day/night
    if TimeOfDay == "Daytime":
        if TimeOfDayTimer == 0:
            TimeOfDay = "Nighttime"
            TimeOfDayTimer = 180
    elif TimeOfDay == "Nighttime":
        if TimeOfDayTimer == 0:
            TimeOfDay = "Daytime"
            TimeOfDayTimer = 180

    # when the current weather timer is expired, generate new random weather based on the time of day
    if WeatherTimer == 0:
        if TimeOfDay == "Daytime":
            CurrentWeather = random.randint(0,5)
        elif TimeOfDay == "Nighttime":
            CurrentWeather = random.randint(1,6)
        WeatherTimer = 60

    return (HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)

# print current weather
def WeatherView(RoomNumber,WeatherTimer,CurrentWeather):
    if RoomNumber < 23 and RoomNumber > 0:
        print
        if WeatherTimer > 50:
            print WeatherOptions[CurrentWeather][0]
        elif WeatherTimer <= 50:
            print WeatherOptions[CurrentWeather][1]
    else:
        print

def LookTime (TimeOfDay,TimeOfDayTimer):
    print
    if TimeOfDay == "Daytime":
        if TimeOfDayTimer > 90:
            print "It's the morning."
        elif TimeOfDayTimer <= 90:
            print "It's the afternoon."
    elif TimeOfDay == "Nighttime":
        if TimeOfDayTimer > 90:
            print "It's the evening."
        elif TimeOfDayTimer <= 90:
            print "It's nighttime."

def CastSpell(SpellChanted,HeroCmd,HeroMagic,HeroHealth,HeroMaxHealth,HeroSpells):
    print
    # healing spells
    if HeroCmd[5:] in DivineHealingSpells:
        if HeroCmd[5:] in SpellChanted:
            SpellRoll = random.randint(DivineHealingSpells[HeroCmd[5:]][2],DivineHealingSpells[HeroCmd[5:]][3])
            SpellRoll *= HeroLevel
            HealthDiff = HeroMaxHealth - HeroHealth
            if HeroMagic > 0:
                if HeroHealth == HeroMaxHealth:
                    print "You are already at full heath..."
                elif SpellRoll <= HealthDiff:
                    HeroHealth += SpellRoll
                    HeroMagic -= 1
                    print "You have been healed for", SpellRoll, "health."
                    SpellRoll = False
                elif SpellRoll > HealthDiff:
                    HeroHealth = HeroMaxHealth
                    HeroMagic -= 1
                    print "You heal yourself to full health."
                    SpellRoll = False
            elif HeroMagic < 1:
                print "Not enough mana."
        elif HeroCmd[5:] not in HeroSpells:
            print "The spell '" + HeroCmd[5:] + "' is unknown to you."
        elif HeroCmd[5:] not in SpellChanted:
            print "The spell '" + HeroCmd[5:] +"' needs to be chanted first."
    return (HeroMagic,HeroHealth)

# Chant spell to put it in Hero memory
def ChantSpell(HeroClass,HeroCmd,SpellChanted,HeroSpells,HeroSpell,HeroBaseSpell,ArcaneBattleSpells,DivineBattleSpells):
    print
    if HeroClass == "Sorcerer" or HeroClass == "Cleric":
        if HeroCmd[6:] in HeroSpells:
            
            if HeroClass == "Sorcerer" and HeroCmd[6:] in ArcaneBattleSpells:
                if SpellChanted[0] in ArcaneBattleSpells:
                    HeroBaseSpell = HeroBaseSpell - ArcaneBattleSpells[SpellChanted[0]][2]
                    HeroSpell = HeroSpell - ArcaneBattleSpells[SpellChanted[0]][3] 
                    SpellChanted = []
                    HeroBaseSpell = HeroBaseSpell + ArcaneBattleSpells[HeroCmd[6:]][2]
                    HeroSpell = HeroSpell + ArcaneBattleSpells[HeroCmd[6:]][3]
                    SpellChanted.append(HeroCmd[6:])
                elif SpellChanted[0] in ArcaneHealingSpells:
                    HeroBaseSpell = HeroBaseSpell - ArcaneHealingSpells[SpellChanted[0]][2]
                    HeroSpell = HeroSpell - ArcaneHealingSpells[SpellChanted[0]][3]
                    SpellChanted = []
                    HeroBaseSpell = HeroBaseSpell + ArcaneBattleSpells[HeroCmd[6:]][2]
                    HeroSpell = HeroSpell + ArcaneBattleSpells[HeroCmd[6:]][3]
                    SpellChanted.append(HeroCmd[6:])
            elif HeroClass == "Sorcerer" and HeroCmd[6:] in ArcaneHealingSpells:
                if SpellChanted[0] in ArcaneBattleSpells:
                    HeroBaseSpell = HeroBaseSpell - ArcaneBattleSpells[SpellChanted[0]][2]
                    HeroSpell = HeroSpell - ArcaneBattleSpells[SpellChanted[0]][3]
                    SpellChanted = []
                    HeroBaseSpell = HeroBaseSpell + ArcaneHealingSpells[HeroCmd[6:]][2]
                    HeroSpell = HeroSpell + ArcaneHealingSpells[HeroCmd[6:]][3]
                    SpellChanted.append(HeroCmd[6:])
                elif SpellChanted[0] in ArcaneHealingSpells:
                    HeroBaseSpell = HeroBaseSpell - ArcaneHealingSpells[SpellChanted[0]][2]
                    HeroSpell = HeroSpell - ArcaneHealingSpells[SpellChanted[0]][3]
                    SpellChanted = []
                    HeroBaseSpell = HeroBaseSpell + ArcaneHealingSpells[HeroCmd[6:]][2]
                    HeroSpell = HeroSpell + ArcaneHealingSpells[HeroCmd[6:]][3]
                    SpellChanted.append(HeroCmd[6:])
            elif HeroClass == "Cleric" and HeroCmd[6:] in DivineBattleSpells:
                if SpellChanted[0] in DivineBattleSpells:
                    HeroBaseSpell = HeroBaseSpell - DivineBattleSpells[SpellChanted[0]][2]
                    HeroSpell = HeroSpell - DivineBattleSpells[SpellChanted[0]][3]
                    SpellChanted = []
                    HeroBaseSpell = HeroBaseSpell + DivineBattleSpells[HeroCmd[6:]][2]
                    HeroSpell = HeroSpell + DivineBattleSpells[HeroCmd[6:]][3]
                    SpellChanted.append(HeroCmd[6:])
                elif SpellChanted[0] in DivineHealingSpells:
                    SpellChanted = []
                    HeroBaseSpell = HeroBaseSpell + DivineBattleSpells[HeroCmd[6:]][2]
                    HeroSpell = HeroSpell + DivineBattleSpells[HeroCmd[6:]][3]
                    SpellChanted.append(HeroCmd[6:])
            elif HeroClass == "Cleric" and HeroCmd[6:] in DivineHealingSpells:
                if SpellChanted[0] in DivineHealingSpells:
                    SpellChanted = []
                    SpellChanted.append(HeroCmd[6:])
                elif SpellChanted[0] in DivineBattleSpells:
                    HeroBaseSpell = HeroBaseSpell - DivineBattleSpells[SpellChanted[0]][2]
                    HeroSpell = HeroSpell - DivineBattleSpells[SpellChanted[0]][3]
                    SpellChanted = []
                    SpellChanted.append(HeroCmd[6:])
            else:
                if not SpellChanted:
                    SpellChanted.append(HeroCmd[6:])
                else:
                    SpellChanted = []
                    SpellChanted.append(HeroCmd[6:])
            print "You chant the spell", HeroCmd[6:] + ", and are now ready to cast it."
        if HeroCmd[6:] not in HeroSpells:
            print "There is no such spell in your Spellbook."
    else:
        print "You are a", HeroClass + ". You cannot chant spells."

    return (SpellChanted,HeroBaseSpell,HeroSpell)

def SpellBook (HeroSpells):
    print
    if not HeroSpells:
        print "Your spellbook is empty."
    else:
        print "SpellBook:", ", ".join(HeroSpells)

# Function to buy/learn spells
def LearnSpell(HeroCmd,RoomNumber,HeroGold,HeroClass,HeroSpells):
    print
    if RoomNumber in ArcaneSpellshopRooms and HeroClass == "Sorcerer":
        if HeroCmd[6:] in ArcaneBattleSpells and ArcaneBattleSpells[HeroCmd[6:]][5] <= HeroLevel:
            if ArcaneBattleSpells[HeroCmd[6:]][0] <= HeroGold and HeroCmd[6:] not in HeroSpells:
                HeroSpells.append(HeroCmd[6:])
                HeroGold -= ArcaneBattleSpells[HeroCmd[6:]][0]
                print "The Chanter teaches you", HeroCmd[6:] + ", then takes", ArcaneBattleSpells[HeroCmd[6:]][0], "gold pieces from you."
            elif ArcaneBattleSpells[HeroCmd[6:]][0] > HeroGold:
                print "'I'm sorry, it looks like you don't have enough gold.'"
            elif HeroCmd[6:] in HeroSpells:
                print "'I've already taught all I can about the spell:", HeroCmd[6:] + ".'"

        elif HeroCmd[6:] in ArcaneHealingSpells and ArcaneHealingSpells[HeroCmd[6:]][5] <= HeroLevel:
            if ArcaneHealingSpells[HeroCmd[6:]][0] <= HeroGold and HeroCmd[6:] not in HeroSpells:
                HeroSpells.append(HeroCmd[6:])
                HeroGold -= ArcaneHealingSpells[HeroCmd[6:]][0]
                print "The Chanter teaches you", HeroCmd[6:] + ", then takes", ArcaneHealingSpells[HeroCmd[6:]][0], "gold pieces from you."
            elif ArcaneHealingSpells[HeroCmd[6:]][0] > HeroGold:
                print "'I'm sorry, it looks like you don't have enough gold.'"
            elif HeroCmd[6:] in HeroSpells:
                print "'I've already taught all I can about the spell:", HeroCmd[6:] + ".'"
        
        elif HeroCmd[6:] in ArcaneBattleSpells and ArcaneBattleSpells[HeroCmd[6:]][5] > HeroLevel:
            print "You are not experienced enough to learn this spell."
        elif HeroCmd[6:] in ArcaneHealingSpells and ArcaneHealingSpells[HeroCmd[6:]][5] > HeroLevel:
            print "You are not experienced enough to learn this spell."
        else:
            print "'There is no such spell,", HeroCmd[6:], "to learn here.'"
    elif RoomNumber in ArcaneSpellshopRooms and HeroClass != "Sorcerer":
        print "'Only those with knowledge of the arcane can learn spells here.'"
        
    elif RoomNumber in DivineSpellshopRooms and HeroClass == "Cleric":
        if HeroCmd[6:] in DivineBattleSpells and DivineBattleSpells[HeroCmd[6:]][5] <= HeroLevel:
            if DivineBattleSpells[HeroCmd[6:]][0] <= HeroGold and HeroCmd[6:] not in HeroSpells:
                HeroSpells.append(HeroCmd[6:])
                HeroGold -= DivineBattleSpells[HeroCmd[6:]][0]
                print "The Priest teaches you", HeroCmd[6:] + ", then takes your donation of", DivineBattleSpells[HeroCmd[6:]][0], "gold."
            elif DivineBattleSpells[HeroCmd[6:]][0] > HeroGold:
                print "'I'm sorry, the Gods only grant such a spell with the right donation of gold'"
            elif HeroCmd[6:] in HeroSpells:
                print "'I've already taught all I can about the spell:", HeroCmd[6:] + ".'"
        elif HeroCmd[6:] in DivineBattleSpells and DivineBattleSpells[HeroCmd[6:]][5] > HeroLevel:
            print "You are not experienced enough to learn this spell."

        elif HeroCmd[6:] in DivineHealingSpells and DivineHealingSpells[HeroCmd[6:]][5] <= HeroLevel:
            if DivineHealingSpells[HeroCmd[6:]][0] <= HeroGold and HeroCmd[6:] not in HeroSpells:
                HeroSpells.append(HeroCmd[6:])
                HeroGold -= DivineHealingSpells[HeroCmd[6:]][0]
                print "The Priest teaches you", HeroCmd[6:] + ", then takes your donation of", DivineHealingSpells[HeroCmd[6:]][0], "gold."
            elif DivineHealingSpells[HeroCmd[6:]][0] > HeroGold:
                print "'I'm sorry, the Gods only grant such a spell with the right donation of gold'"
            elif HeroCmd[6:] in HeroSpells:
                print "'I've already taught all I can about the spell:", HeroCmd[6:] + ".'"
        elif HeroCmd[6:] in DivineHealingSpells and DivineHealingSpells[HeroCmd[6:]][5] > HeroLevel:
            print "You are not experienced enough to learn this spell."
            
        elif HeroCmd[6:] not in DivineBattleSpells and HeroCmd[6:] not in DivineHealingSpells:
            print "'There is no such spell,", HeroCmd[6:], "to learn here.'"
    elif RoomNumber in DivineSpellshopRooms and HeroClass != "Cleric":
        print "'Only those with knowledge of the divine can learn spells here.'"
    else:
        print "You can't do that here...\n"
    
    return (HeroGold,HeroSpells)

# Display what currently exists in the inventory list
def HeroInv(HeroGold,Inventory):
    print "You have",HeroGold,"gold."
    if not Inventory:
        print "You are carrying nothing in your inventory."
    else:
        print "Items in inventory:", ", ".join(Inventory)

# Display what the player currently has equipped
def HeroEquipped(ItemsWorn):
    print
    if not ItemsWorn:
        print "You have nothing equipped."
    else:
        print "Equipped items: ", ", ".join(ItemsWorn)

# Each room has it's own inventory list for dropping and picking up items. This shows what is there.
def RoomItems(RoomInv, RoomNumber):
    if RoomInv[RoomNumber]:
        print "In the room you see:", ", ".join(RoomInv[RoomNumber])

# Take item from a room list matrix and put it in the inventory list
def GetItem(RoomInv,RoomNumber,HeroCmd,SolidItem):
    print
    if HeroCmd[4:] in RoomInv[RoomNumber] and HeroCmd[4:] not in SolidItem:
        if len(Inventory) < 20:
            print "You pick up the " + HeroCmd[4:] + " and put it in your inventory..."
            Inventory.append(HeroCmd[4:])
            RoomInv[RoomNumber].remove(HeroCmd[4:])
        elif len(Inventory) >= 20:
            print "You are overloaded."
    elif HeroCmd[4:] not in RoomInv[RoomNumber]:
        print "Sorry! There is no " + HeroCmd[4:] + " in this room..."
    elif HeroCmd[4:] in SolidItem and HeroCmd[4:] in RoomInv[RoomNumber]:
        print "You can't pick up the", HeroCmd[4:] + "..."
    return (RoomInv, RoomNumber)

# Take item from inventory list and put it in the room list matrix        
def DropItem(RoomInv, RoomNumber, HeroCmd):
    if HeroCmd[5:] in Inventory:
        print "\nYou neatly place the " + HeroCmd[5:] + " on the ground..."
        RoomInv[RoomNumber].append(HeroCmd[5:])
        Inventory.remove(HeroCmd[5:])
    elif HeroCmd[5:] not in Inventory:
        print "\nSorry! There is no " + HeroCmd[5:] + " in your inventory..."
    return (RoomInv, RoomNumber)

# Function to search items and get random treasure currently in the room list matrix
def SearchItems(HeroGold,RoomInv,RoomNumber,HeroCmd,HeroLevel):
    print

    # 1 in 5 chance of finding nothing, 2 in 5 chance of finding gold, 2 in 5 chance of finding treasure    
    LootChance = random.randint(1,5)

    #create a temp dictionary of treasure items that matches the difficulty level of the room
    CurrentTreasure = {}
    for k,v in LootItems.iteritems():
        if LootItems[k][2] == RoomIndex[RoomNumber][7]:
            CurrentTreasure[k]=v

    #create a temp dictionary for boss treasure
    CurrentRareTreasure = {}
    for k,v in RareLootItems.iteritems():
        if RareLootItems[k][2] <= RoomIndex[RoomNumber][7]:
            CurrentRareTreasure[k]=v

    if HeroCmd[7:] in SolidItem:
        # if no treasure level matches the current room level, then generate gold instead of treasure
        if not CurrentTreasure:
            LootChance = 4
        if HeroCmd[7:] in RoomInv[RoomNumber]:
            if LootChance < 3:
                TreasureItem = random.choice(CurrentTreasure.keys())
                print "After searching the", HeroCmd[7:], "for treasure, a", TreasureItem, "falls to the ground."
                print "The", HeroCmd[7:], "crumbles to dust..."
                RoomInv[RoomNumber].append(TreasureItem)
                RoomInv[RoomNumber].remove(HeroCmd[7:])  
            elif LootChance > 3:
                GoldChance = random.randint(1,5)
                GoldChance = GoldChance * HeroLevel
                print "After searching the", HeroCmd[7:], "you find", GoldChance, "gold and add it to your stash."
                print "The", HeroCmd[7:], "crumbles to dust..."
                HeroGold = HeroGold + GoldChance
                RoomInv[RoomNumber].remove(HeroCmd[7:])
            else:
                print "You find nothing..."
                print "The", HeroCmd[7:],"crumbles to dust..."
                RoomInv[RoomNumber].remove(HeroCmd[7:])
        elif HeroCmd[7:] not in RoomInv[RoomNumber]:
            print "You don't see a", HeroCmd[7:], "to search here..."
            
    elif HeroCmd[7:] in SolidItem2:
        # if there is a monster in the same room as the SolidItem2, then block the player from being able to search until the monster is dead
        MonsterInRoom = 0
        for key in RoomInv[RoomNumber]:
            if key in MonsterIndex:
                MonsterInRoom = 1
        if MonsterInRoom == 1:
            print "There is currently someone, or something, blocking your attempt to search..."
            
        elif MonsterInRoom == 0:
            # if no treasure level matches the current room level, then generate gold instead of treasure
            if not CurrentRareTreasure:
                LootChance = 6
            if HeroCmd[7:] in RoomInv[RoomNumber]:
                if LootChance < 6:
                    TreasureItem = random.choice(CurrentRareTreasure.keys())
                    print "After searching the", HeroCmd[7:], "for treasure, a", TreasureItem, "falls to the ground."
                    print "The", HeroCmd[7:], "crumbles to dust..."
                    RoomInv[RoomNumber].append(TreasureItem)
                    RoomInv[RoomNumber].remove(HeroCmd[7:])  
                elif LootChance == 6:
                    GoldChance = random.randint(1,5)
                    GoldChance = GoldChance * HeroLevel * 5
                    print "After searching the", HeroCmd[7:], "you find", GoldChance, "gold and add it to your stash."
                    print "The", HeroCmd[7:], "crumbles to dust..."
                    HeroGold = HeroGold + GoldChance
                    RoomInv[RoomNumber].remove(HeroCmd[7:])
                elif HeroCmd[7:] not in RoomInv[RoomNumber]:
                    print "You don't see a", HeroCmd[7:], "to search here..."
        
    else:
        print "That's not a searchable item..."
        
    return (HeroGold, RoomInv)

# Take item from inventory and put it in the list of items currently being used
def EquipItem(HeroSTRBonus,HeroClass,HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot,HeroCmd):
    print

    # 1 handed weapons
    if HeroCmd[6:] in Inventory and HeroCmd[6:] not in WeaponStats and HeroCmd[6:] not in ArmorStats and HeroCmd[6:] not in ShieldStats:
        print "That is not an equippable item..."
    elif HeroCmd[6:] in Inventory and HeroCmd[6:] in WeaponStats and WeaponSlot == 0 and WeaponStats[HeroCmd[6:]][8] < 2:
        if HeroClass == "Sorcerer" and WeaponStats[HeroCmd[6:]][6] > 1:
            print "As a Sorcerer, you cannot use:", HeroCmd[6:]
        elif HeroClass == "Rogue" and WeaponStats[HeroCmd[6:]][6] > 1:
            print "As a Rogue, you cannot use:", HeroCmd[6:]
        elif HeroClass == "Cleric" and WeaponStats[HeroCmd[6:]][7] == 0:
            print "Your divine beliefs do not allow a weapon that draws blood. Only blunt weapons."
        else:
            WeaponSlot = 1
            HeroMinDmg += WeaponStats[HeroCmd[6:]][2]
            HeroMaxDmg += WeaponStats[HeroCmd[6:]][3]
            # based on 1d3 fist
            HeroMinDmg -= 1
            HeroMaxDmg -= 3
            ItemEquipped(HeroCmd)
            
    # 2 handed weapons
    elif HeroCmd[6:] in Inventory and HeroCmd[6:] in WeaponStats and WeaponSlot == 0 and WeaponStats[HeroCmd[6:]][8] == 2 and ShieldSlot == 1:
        print "You cannot use a two-handed weapon with a shield."
    elif HeroCmd[6:] in Inventory and HeroCmd[6:] in WeaponStats and WeaponSlot == 0 and WeaponStats[HeroCmd[6:]][8] == 2 and ShieldSlot == 0:
        if HeroClass == "Sorcerer" and WeaponStats[HeroCmd[6:]][6] > 1:
            print "As a Sorcerer, you cannot use:", HeroCmd[6:]
        elif HeroClass == "Rogue" and WeaponStats[HeroCmd[6:]][6] > 1:
            print "As a Rogue, you cannot use:", HeroCmd[6:]
        elif HeroClass == "Cleric" and WeaponStats[HeroCmd[6:]][7] == 0:
            print "Your divine beliefs do not allow a weapon that draws blood. Only blunt weapons."
        elif HeroClass == "Cleric" and WeaponStats[HeroCmd[6:]][7] == 1:
            WeaponSlot = 2
            HeroMinDmg += (WeaponStats[HeroCmd[6:]][2] + HeroSTRBonus)
            HeroMaxDmg += (WeaponStats[HeroCmd[6:]][3] + HeroSTRBonus)
            # based on 1d3 fist
            HeroMinDmg -= 1
            HeroMaxDmg -= 3
            ItemEquipped(HeroCmd)
        else:
            WeaponSlot = 2
            HeroMinDmg += (WeaponStats[HeroCmd[6:]][2] + HeroSTRBonus)
            HeroMaxDmg += (WeaponStats[HeroCmd[6:]][3] + HeroSTRBonus)
            # based on 1d3 fist
            HeroMinDmg -= 1
            HeroMaxDmg -= 3
            ItemEquipped(HeroCmd)
    
    elif HeroCmd[6:] in Inventory and HeroCmd[6:] in ArmorStats and ArmorSlot == 0:
        if HeroClass == "Sorcerer" and ArmorStats[HeroCmd[6:]][5] > 1:
            print "As a sorcerer, you cannot wear:", HeroCmd[6:]
        elif HeroClass == "Rogue" and ArmorStats[HeroCmd[6:]][5] > 2:
            print "As a rogue, you cannot wear:", HeroCmd[6:]
        else:
            ArmorSlot = 1
            HeroArmor += ArmorStats[HeroCmd[6:]][2]
            ItemEquipped(HeroCmd)
            
    elif HeroCmd[6:] in Inventory and HeroCmd[6:] in ShieldStats and ShieldSlot == 0:
        if WeaponSlot == 2:
            print "You cannot use a shield with a two-handed weapon."
        elif HeroClass == "Sorcerer" and WeaponSlot == 1:
            print "As a Sorcerer, you cannot use shields."
        elif HeroClass == "Rogue" and ShieldStats[HeroCmd[6:]][5] > 2 and WeaponSlot == 1:
            print "As a Rogue, you cannot use:", HeroCmd[6:]
        else:
            ShieldSlot = 1
            HeroArmor += ShieldStats[HeroCmd[6:]][2]
            ItemEquipped(HeroCmd)
            
    elif HeroCmd[6:] not in Inventory:
        print "There is no " + HeroCmd[6:] + " in your inventory..."
    else:
        print "You already have something similar equipped! You should remove it first..."
    return (HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot)

# Take from list of items currently being used and put them in inventory
def RemoveItem(HeroSTRBonus,HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot,HeroCmd):
    print
    if HeroCmd[7:] in ItemsWorn and HeroCmd[7:] in WeaponStats:
        if WeaponSlot == 1:
            HeroMinDmg -= WeaponStats[HeroCmd[7:]][2]
            HeroMaxDmg -= WeaponStats[HeroCmd[7:]][3]
            # based on 1d3 fists
            HeroMinDmg += 1
            HeroMaxDmg += 3
            WeaponSlot = 0
            ItemRemoved(HeroCmd)
        elif WeaponSlot == 2:
            HeroMinDmg -= (WeaponStats[HeroCmd[7:]][2] + HeroSTRBonus)
            HeroMaxDmg -= (WeaponStats[HeroCmd[7:]][3] + HeroSTRBonus)
            # based on 1d3 fists
            HeroMinDmg += 1
            HeroMaxDmg += 3
            WeaponSlot = 0
            ItemRemoved(HeroCmd)                                                                    
    elif HeroCmd[7:] in ItemsWorn and HeroCmd[7:] in ArmorStats:
        ArmorSlot = 0
        HeroArmor = HeroArmor - ArmorStats[HeroCmd[7:]][2]
        ItemRemoved(HeroCmd)
    elif HeroCmd[7:] in ItemsWorn and HeroCmd[7:] in ShieldStats:
        ShieldSlot = 0
        HeroArmor = HeroArmor - ShieldStats[HeroCmd[7:]][2]
        ItemRemoved(HeroCmd)
    elif HeroCmd[7:] not in ItemsWorn:
        print "You do not have a " + HeroCmd[7:] + " currently equipped..."
    return (HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot)

# Function to equip items from inventory to item slots
def ItemEquipped(HeroCmd):
    ItemsWorn.append(HeroCmd[6:])
    Inventory.remove(HeroCmd[6:])
    print "You equip the " + HeroCmd[6:] + "."

# Function to remove items from item slots to inventory
def ItemRemoved(HeroCmd):
    Inventory.append(HeroCmd[7:])
    ItemsWorn.remove(HeroCmd[7:])
    print "You remove the " + HeroCmd[7:] + " and put it in your inventory."

# Function to quit the game
def QuitGame():
    QuitConfirm = raw_input ("\nAre you sure you wish to quit the program? (Y/N) ").lower()
    if QuitConfirm == "y":
        print "\nThanks for playing!\n"
    elif QuitConfirm == "yes":
        print "\nThanks for playing!\n"
    else:
        print "\nI knew you would rather stay..."

# Functions to display shop items and prices
def ShopItemWeapon(RoomNumber):
    if RoomNumber in BlacksmithRooms:
        print
        for k, v in WeaponStats.iteritems():
            if WeaponStats[k][5] == 1:
                print k + ":", v[0], "gold"
    else:
        print "\nYou can't do that here."

def ShopItemArmor(RoomNumber):
    if RoomNumber in BlacksmithRooms:
        print
        for k, v in ArmorStats.iteritems():
            if ArmorStats[k][4] == 1:
                print k + ":", v[0], "gold"
    else:
        print "\nYou don't see that here." 

def ShopItemShield(RoomNumber):
    if RoomNumber in BlacksmithRooms:
        print
        for k, v in ShieldStats.iteritems():
            if ShieldStats[k][4] == 1:
                print k + ":", v[0], "gold"
    else:
        print "\nYou don't see that here."

def ShopArcaneSpells(RoomNumber,HeroLevel):
    if RoomNumber in ArcaneSpellshopRooms:
        print
        for k, v in ArcaneBattleSpells.iteritems():
            if ArcaneBattleSpells[k][5] <= HeroLevel:
                print k + ":", v[0], "gold"
        for k, v in ArcaneHealingSpells.iteritems():
            if ArcaneHealingSpells[k][5] <= HeroLevel:
                print k + ":", v[0], "gold"
    else:
        print "\nYou don't see that here."

def ShopDivineSpells(RoomNumber,HeroLevel):
    if RoomNumber in DivineSpellshopRooms:
        print
        for k, v in DivineBattleSpells.iteritems():
            if DivineBattleSpells[k][5] <= HeroLevel:
                print k + ":", v[0], "gold"
        for k, v in DivineHealingSpells.iteritems():
            if DivineHealingSpells[k][5] <= HeroLevel:
                print k + ":", v[0], "gold"
    else:
        print "\nYou don't see that here."

def ShopPotions(RoomNumber):
    if RoomNumber in ApothecaryRooms:
        print
        for k, v in UseableItems.iteritems():
            if UseableItems[k][2] == 1:
                print k + ":", v[0], "gold"
    else:
        print "\nYou don't see that here." 

# Function to buy items
def BuyItems(HeroCmd,RoomNumber,HeroGold):
    if RoomNumber in BlacksmithRooms or RoomNumber in ApothercaryRooms:
        if RoomNumber in BlacksmithRooms:
            if HeroCmd[4:] in WeaponStats:
                if WeaponStats[HeroCmd[4:]][0] <= HeroGold:
                    Inventory.append(HeroCmd[4:])
                    HeroGold = HeroGold - WeaponStats[HeroCmd[4:]][0]
                    print "\n'Aha! " + HeroCmd[4:] + "! Good choice. I'll take your", WeaponStats[HeroCmd[4:]][0],"gold for that...'"
                elif WeaponStats[HeroCmd[4:]][0] > HeroGold:
                    print "\n'I'm sorry, it looks like you don't have enough gold...'"       
            elif HeroCmd[4:] in ArmorStats:
                if ArmorStats[HeroCmd[4:]][0] <= HeroGold:
                    Inventory.append(HeroCmd[4:])
                    HeroGold = HeroGold - ArmorStats[HeroCmd[4:]][0]
                    print "\n'Aha! " + HeroCmd[4:] + "! Good choice. I'll take your", ArmorStats[HeroCmd[4:]][0],"gold for that...'"
                elif ArmorStats[HeroCmd[4:]][0] > HeroGold:
                    print "\n'I'm sorry, it looks like you don't have enough gold...'"     
            elif HeroCmd[4:] in ShieldStats:
                if ShieldStats[HeroCmd[4:]][0] <= HeroGold:
                    Inventory.append(HeroCmd[4:])
                    HeroGold = HeroGold - ShieldStats[HeroCmd[4:]][0]
                    print "\n'Aha! " + HeroCmd[4:] + "! Good choice. I'll take your", ShieldStats[HeroCmd[4:]][0],"gold for that...'"
                elif ShieldStats[HeroCmd[4:]][0] > HeroGold:
                    print "\n'I'm sorry, it looks like you don't have enough gold...'"
            else:
                print "\n'There is no " + HeroCmd[4:] + " for sale here...'"  
        if RoomNumber in ApothecaryRooms:
            if HeroCmd[4:] in UseableItems:
                if UseableItems[HeroCmd[4:]][0] <= HeroGold:
                    Inventory.append(HeroCmd[4:])
                    HeroGold = HeroGold - UseableItems[HeroCmd[4:]][0]
                    print "\n'Aha! " + HeroCmd[4:] + "! Good choice. I'll take your", UseableItems[HeroCmd[4:]][0],"gold for that...'"
                elif UseableItems[HeroCmd[4:]][0] > HeroGold:
                    print "\n'I'm sorry, it looks like you don't have enough gold...'"
    else:
        print "You cannot do that here..."
    return HeroGold

# Function to sell items
def SellItems(HeroCmd,RoomNumber,HeroGold):
    if RoomNumber in PawnshopRooms:
        if HeroCmd[5:] in Inventory and HeroCmd[5:] in WeaponStats:
            Inventory.remove(HeroCmd[5:])
            HeroGold = HeroGold + WeaponStats[HeroCmd[5:]][1]
            print "\n'A " + HeroCmd[5:] + "? Here is", WeaponStats[HeroCmd[5:]][1], "gold for that...'"    
        elif HeroCmd[5:] in Inventory and HeroCmd[5:] in ArmorStats:
            Inventory.remove(HeroCmd[5:])
            HeroGold += ArmorStats[HeroCmd[5:]][1]
            print "\n'A " + HeroCmd[5:] + "? Here is", ArmorStats[HeroCmd[5:]][1], "gold for that...'"    
        elif HeroCmd[5:] in Inventory and HeroCmd[5:] in ShieldStats:
            Inventory.remove(HeroCmd[5:])
            HeroGold += ShieldStats[HeroCmd[5:]][1]
            print "\n'A " + HeroCmd[5:] + "? Here is", ShieldStats[HeroCmd[5:]][1], "gold for that...'"
        elif HeroCmd[5:] in Inventory and HeroCmd[5:] in LootItems:
            Inventory.remove(HeroCmd[5:])
            HeroGold += LootItems[HeroCmd[5:]][1]
            print "\n'A " + HeroCmd[5:] + "? Here is", LootItems[HeroCmd[5:]][1], "gold for that...'"
        elif HeroCmd[5:] in Inventory and HeroCmd[5:] in UseableItems:
            Inventory.remove(HeroCmd[5:])
            HeroGold += UseableItems[HeroCmd[5:]][1]
            print "\n'A " + HeroCmd[5:] + "? Here is", UseableItems[HeroCmd[5:]][1], "gold for that...'"
        elif HeroCmd[5:] not in Inventory:
            print "\n'You can't fool me! You don't have a", HeroCmd[5:] + "!'"
        else:
            print "\n'We don't have use for those things here!"
    else:
        print "\nYou can't do that here...\n"
    return HeroGold

# Function to rest
def HeroRest(HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMaxHealth,HeroHealth,HeroMaxMagic,HeroMagic,RoomNumber):
    if HeroMagic < HeroMaxMagic and HeroHealth < HeroMaxHealth:
        HeroHealth += 1
        HeroMagic += 1
        HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
        print "\nYou feel quite a bit better..."
    elif HeroHealth < HeroMaxHealth:
        HeroHealth += 1
        HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
        print "\nYou feel a little bit better..."
    elif HeroMagic < HeroMaxMagic:
        HeroMagic += 1
        HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
        print "\nYou feel a little bit better..."
    else:
        print "\nYou are already fully rested..."
    return (HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroHealth,HeroMagic,RoomNumber)

# Function to look at items
def ItemLook(HeroCmd,RoomNumber):
    print
    if HeroCmd[5:] in RoomInv[RoomNumber] or HeroCmd[5:] in Inventory or HeroCmd[5:] in ItemsWorn:
        if HeroCmd[5:] in LootItems:
            print LootItems[HeroCmd[5:]][3]
        if HeroCmd[5:] in WeaponStats:
            print WeaponStats[HeroCmd[5:]][9]
        if HeroCmd[5:] in ArmorStats:
            print ArmorStats[HeroCmd[5:]][6]
        if HeroCmd[5:] in ShieldStats:
            print ShieldStats[HeroCmd[5:]][6]
        if HeroCmd[5:] in UseableItems:
            print UseableItems[HeroCmd[5:]][3]
    else:
        print "You don't see that anywhere."

def UseItem(HeroCmd,HeroHealth,HeroMaxHealth,RoomNumber):
    print
    if HeroCmd[4:] in Inventory:
        if HeroCmd[4:] == "red vial":
            if HeroHealth == HeroMaxHealth:
                print "You are already at full health."
            elif HeroHealth < HeroMaxHealth:
                HeroHealth = HeroMaxHealth
                Inventory.remove(HeroCmd[4:])
                print "You drink the red vial and are healed for full health!"
        elif HeroCmd[4:] == "blue vial":
            if HeroClass == "Cleric" or HeroClass == "Sorcerer":
                if HeroMagic == HeroMaxMagic:
                    print "You are already at full mana."
                elif HeroMagic < HeroMaxMagic:
                    HeroMagic = HeroMaxMagic
                    Inventory.remove(HeroCmd[4:])
                    print "You drink the blue vial and feel your mana replenished!"
            elif HeroClass == "Fighter" or HeroClass == "Rogue":
                    Inventory.remove(HeroCmd[4:])
                    if HeroHealth == HeroMaxHealth:
                        print "You drink the sweet blue liquid. It does nothing for you."
                    elif HeroHealth < HeroMaxHealth:
                        HeroHealth = HeroHealth + 1
                        print "You drink the blue vial, but feel nothing more than a small sugar rush."
        elif HeroCmd[4:] == "scroll":
            RoomNumber = 2
            Inventory.remove(HeroCmd[4:])
            print "You read the runes on the scroll and feel enveloped by power.\nYour surroundings have changed. You have been transported elsewhere!"
        else:
            print "That is not a useable item."
    elif HeroCmd[4:] not in Inventory:
        print "You don't have a", HeroCmd[4:], "to use."

    return (HeroHealth,RoomNumber)

#######################
# ATTACK SUBFUNCTIONS #
#######################
#
# Monster attack Subfunction
def DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor):
    # monster attack
    AttackRoll = random.randint(1,20)
    if MonsterHealth < 1:
        print
    elif AttackRoll == 20:
        print MonsterSpawn, "critically hits you for", MonsterIndex[MonsterSpawn][4] + MonsterSTRBonus , "damage!"
        HeroHealth -= (MonsterIndex[MonsterSpawn][4] + MonsterSTRBonus)
    elif (MonsterAttack + AttackRoll) > HeroArmor:
        DamageRoll = random.randint(MonsterIndex[MonsterSpawn][3],MonsterIndex[MonsterSpawn][4])
        HeroHealth -= (DamageRoll + MonsterSTRBonus)
        print MonsterSpawn, "hits you for", DamageRoll + MonsterSTRBonus, "damage!"
    elif (MonsterAttack + AttackRoll) <= HeroArmor:
        MissStatus = random.randint(0,2)
        if MissStatus == 0:
            print MonsterSpawn, "misses you!"
        elif MissStatus == 1:
            print "You dodge the", MonsterSpawn + "'s attack!"
        elif MissStatus == 2:
            print "You block the", MonsterSpawn + "'s attack!"
    
    return HeroHealth

# Hero melee attack Subfunction
def DoHeroMeleeAttack(MonsterSpawn,MonsterHealth,HeroHealth,HeroAttack,HeroMaxDmg):
    AttackRoll = random.randint(1,20)
    if HeroHealth < 1:
        print
    elif AttackRoll == 20:
        print "You critically hit the", MonsterSpawn, "for", HeroMaxDmg, "damage!"
        MonsterHealth -= HeroMaxDmg
    elif (HeroAttack + AttackRoll) > MonsterIndex[MonsterSpawn][5]:
        DamageRoll = random.randint(HeroMinDmg,HeroMaxDmg)
        MonsterHealth -= DamageRoll
        print "You hit the", MonsterSpawn, "for", DamageRoll, "damage!"
    elif (HeroAttack + AttackRoll) <= MonsterIndex[MonsterSpawn][5]:
        MissStatus = random.randint(0,2)
        if MissStatus == 0:
            print "You missed the", MonsterSpawn + "!"
        elif MissStatus == 1:
            print "The", MonsterSpawn, "dodged your attack!"
        elif MissStatus == 2:
            print "The", MonsterSpawn, "blocked your attack!"
            
    return MonsterHealth

# Hero arcane damage subfunction
def DoHeroArcaneDamageAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell):
    AttackRoll = random.randint(1,20)
    if HeroHealth < 1:
        print
    elif AttackRoll == 20:
        MonsterHealth -= (HeroSpell * HeroLevel)
        HeroMagic -= (ArcaneBattleSpells[BattleSpell][1] * HeroLevel)
        print "Your spell", BattleSpell,"critically hits the", MonsterSpawn, "for", HeroSpell, "damage!"
    elif AttackRoll < 20:
        if (HeroINTBonus + HeroLevel + AttackRoll) > MonsterIndex[MonsterSpawn][5]:
            DamageRoll = random.randint(HeroBaseSpell,HeroSpell) * HeroLevel
            MonsterHealth -= DamageRoll
            HeroMagic -= (ArcaneBattleSpells[BattleSpell][1] * HeroLevel)
            print "You cast", BattleSpell, "and hit the", MonsterSpawn, "for", DamageRoll, "damage!"
        elif (HeroINTBonus + HeroLevel + AttackRoll) <= MonsterIndex[MonsterSpawn][5]:
            MissStatus = random.randint(0,2)
            if MissStatus == 0:
                print "You cast", BattleSpell + ", but missed the", MonsterSpawn + "!"
            elif MissStatus == 1:
                print "You cast", BattleSpell, "but the", MonsterSpawn, "dodged your spell!"
            elif MissStatus == 2:
                print "You cast", BattleSpell, "but the", MonsterSpawn, "blocked your spell!"    

    return (MonsterHealth,HeroMagic)

def DoHeroArcaneHealingAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell):
    AttackRoll = random.randint(1,20)
    HealthDifference = HeroMaxHealth - HeroHealth
    if HeroHealth < 1:
        print
    elif AttackRoll == 20:
        MonsterHealth -= (HeroSpell * HeroLevel)
        HeroMagic -= (ArcaneHealingSpells[BattleSpell][1] * HeroLevel)
        if HeroSpell >= HealthDifference:
            HeroHealth = HeroMaxHealth
            print "You have critically drained", (HeroSpell * HeroLevel), "health from the", MonsterSpawn, "and fully restored your health!"
        elif HeroHealth == HeroMaxHealth:
            print "You have critically drained the", MonsterSpawn, "of", (HeroSpell * HeroLevel), "health!"
        elif HeroSpell < HealthDifference:
            print "You critically siphon", (HeroSpell * HeroLevel), "health from the", MonsterSpawn + "!"
            HeroHealth += HeroSpell
    elif AttackRoll < 20:
        if (HeroINTBonus + HeroLevel + AttackRoll) > MonsterIndex[MonsterSpawn][5]:
            DamageRoll = random.randint(HeroBaseSpell,HeroSpell) * HeroLevel
            MonsterHealth -= DamageRoll
            HeroMagic -= (ArcaneHealingSpells[BattleSpell][1] * HeroLevel)
            if HeroSpell >= HealthDifference:
                HeroHealth = HeroMaxHealth
            elif HeroHealth == HeroMaxHealth:
                pass
            elif DamageRoll < HealthDifference:
                HeroHealth += DamageRoll
            print "You siphon", DamageRoll, "health from the", MonsterSpawn + "!"
        elif (HeroINTBonus + HeroLevel + AttackRoll) <= MonsterIndex[MonsterSpawn][5]:
            MissStatus = random.randint(0,2)
            if MissStatus == 0:
                print "You cast", BattleSpell + ", but missed the", MonsterSpawn + "!"
            elif MissStatus == 1:
                print "You cast", BattleSpell, "but the", MonsterSpawn, "dodged your spell!"
            elif MissStatus == 2:
                print "You cast", BattleSpell, "but the", MonsterSpawn, "blocked your spell!"
                                    
    return (MonsterHealth,HeroMagic)

def DoHeroDivineDamageAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell):
    AttackRoll = random.randint(1,20)
    if HeroHealth < 1:
        print
    elif AttackRoll == 20:
        MonsterHealth -= (HeroSpell * HeroLevel)
        HeroMagic -= (DivineBattleSpells[BattleSpell][1] * HeroLevel)
        print "Your spell", BattleSpell,"critically hits the", MonsterSpawn, "for", (HeroSpell * HeroLevel), "damage!"
    elif AttackRoll < 20:
        if (HeroINTBonus + HeroLevel + AttackRoll) > MonsterIndex[MonsterSpawn][5]:
            DamageRoll = random.randint(HeroBaseSpell,HeroSpell) * HeroLevel
            MonsterHealth -= DamageRoll
            HeroMagic -= (DivineBattleSpells[BattleSpell][1] * HeroLevel)
            print "You cast", BattleSpell, "and hit the", MonsterSpawn, "for", DamageRoll, "damage!"
        elif (HeroINTBonus + HeroLevel + AttackRoll) <= MonsterIndex[MonsterSpawn][5]:
            MissStatus = random.randint(0,2)
            if MissStatus == 0:
                print "You cast", BattleSpell + ", but missed the", MonsterSpawn + "!"
            elif MissStatus == 1:
                print "You cast", BattleSpell, "but the", MonsterSpawn, "dodged your spell!"
            elif MissStatus == 2:
                print "You cast", BattleSpell, "but the", MonsterSpawn, "blocked your spell!"
                       
    return (MonsterHealth,HeroMagic)

# Function for when player enters combat
def StartCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroMaxMagic,HeroClass,SpellChanted,HeroLevel,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,MonsterIndex,GameTurns,RoomNumber,HeroExperience,HeroHealth,MonsterSpawn,MonsterHealth,MonsterMinStat,MonsterMaxStat,MonsterMinDmg,MonsterMaxDmg,MonsterArmor,MonsterMagic,MonsterSpell,KillExperience,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell):
    AttackCmd = ""
    MonsterInitiative = False
    HeroInitiative = False

    MonsterSTR = random.randint(MonsterIndex[MonsterSpawn][1],MonsterIndex[MonsterSpawn][2])
    MonsterDEX = random.randint(MonsterIndex[MonsterSpawn][1],MonsterIndex[MonsterSpawn][2])
    
    MonsterAttack = ((MonsterSTR - 10)/2) + 1
    MonsterHealth = MonsterIndex[MonsterSpawn][0]
    MonsterSTRBonus = (MonsterSTR - 10)/2
    MonsterDEXBonus = (MonsterDEX - 10)/2
    if MonsterSTRBonus < 1:
        MonsterSTRBonus = 0

    MonsterInitiative = random.randint(1,20) + MonsterDEXBonus
    HeroInitiative = random.randint(1,20) + HeroDEXBonus
    while MonsterInitiative == HeroInitiative:
        MonsterInitiative = random.randint(1,20) + MonsterDEXBonus
        HeroInitiative = random.randint(1,20) + HeroDEXBonus

    if MonsterInitiative > HeroInitiative:
        FirstAttack = "monster"
        print "The", MonsterSpawn, "has the initiative!"
    else:
        FirstAttack = "hero"
        print "You have the initiative!"

    while AttackCmd != "f":
        HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
        if HeroHealth > 0:
            print "You are at", HeroHealth, "health!"
        elif HeroHealth < 1:
            print "\nYou have died!!!...\n"
            print "You wake up in a small corner of the church. A priest looks over you with"
            print "concern. 'We feared the worst' He says. 'But alas, it appears the Gods still"
            print "have use for you... With a suitable donation of gold, of course...'"
            RoomNumber = ResurrectionRooms[0]
            HeroHealth = HeroMaxHealth
            HeroMagic = HeroMaxMagic
            if HeroGold > 20:
                HeroGold -= (20 * HeroLevel)
            elif HeroGold <= 20:
                HeroGold = 0
            break
        
        if MonsterHealth > 0:
            print MonsterSpawn,"is at", MonsterHealth, "health!"
        elif MonsterHealth < 1:
            print "The", MonsterSpawn, "has been defeated!"
            HeroExperience += KillExperience
            print "You gain", KillExperience, "experience!"
            if MonsterSpawn in RoomInv[RoomNumber]:
                RoomInv[RoomNumber].remove(MonsterSpawn)
            RoomInv[RoomNumber].append("corpse")
            break

        if HeroClass == "Sorcerer" or HeroClass == "Cleric":
            BattleSpell = SpellChanted[0]
        print 
        print " Health:" + str(HeroHealth) + "/" + str(HeroMaxHealth)
        print "   Mana:" + str(HeroMagic) + "/" + str(HeroMaxMagic)
        print 
        AttackCmd = raw_input ("(A)ttack | (S)pellcast | (U)se item | (F)lee : ").lower()
        print

# se dexterity roll in chance to flee
        FleeChance = random.randint(1,30)
        if AttackCmd == "f" and FleeChance <= HeroDEX:
            print "You manage slip away in to the shadows and evade the", MonsterSpawn + "."
            break
        elif AttackCmd == "f" and FleeChance > HeroDEX:
            print "You attempt escape, but the", MonsterSpawn, "blocks your path!"
            AttackCmd = "a"

        if AttackCmd != "f":
            FleeChance == 1

# melee attack
        if AttackCmd == "a":     
            if FirstAttack == "monster": # Monster goes first
                HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)
                MonsterHealth = DoHeroMeleeAttack(MonsterSpawn,MonsterHealth,HeroHealth,HeroAttack,HeroMaxDmg)     
            else: # Hero goes first!
                MonsterHealth = DoHeroMeleeAttack(MonsterSpawn, MonsterHealth, HeroHealth, HeroAttack, HeroMaxDmg)
                HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)

# use item in combat
        elif AttackCmd == "u":
            print " Items available to use in inventory:\n"
            if "red vial" in Inventory:
                print " (R)ed vial"
            if "blue vial" in Inventory:
                print " (B)lue vial"
            if "green vial" in Inventory:
                print " (G)reen vial"
            if "scroll" in Inventory:
                print " (S)croll"
                
            CombatUseItem = raw_input("\n Pick an item to use: ").lower()
            if CombatUseItem == "r":
                if "red vial" in Inventory:
                    if HeroHealth == HeroMaxHealth:
                        print "\n You are already at full health."
                    elif HeroHealth < HeroMaxHealth:
                        HeroHealth = HeroMaxHealth
                        Inventory.remove("red vial")
                        print "\n You drink the red vial and are healed for full health!"
                else:
                    print "\n You can't use something you don't have..."
                print
                    
            elif CombatUseItem == "b":
                if "blue vial" in Inventory:
                    if HeroClass == "Cleric" or HeroClass == "Sorcerer":
                        if HeroMagic == HeroMaxMagic:
                            print "\n You are already at full mana."
                        elif HeroMagic < HeroMaxMagic:
                            HeroMagic = HeroMaxMagic
                            Inventory.remove("blue vial")
                            print "\n You drink the blue vial and feel your mana replenished!"
                    
                    elif HeroClass == "Fighter" or HeroClass == "Rogue":
                            Inventory.remove("blue vial")
                            if HeroHealth == HeroMaxHealth:
                                print "\n You drink the sweet blue liquid. It does nothing for you."
                            elif HeroHealth < HeroMaxHealth:
                                HeroHealth = HeroHealth + 1
                                print "\n You drink the blue vial, but feel nothing more than a small sugar rush."
                else:
                    print "\n You can't use something you don't have..."
                print
                    
            elif CombatUseItem == "s":
                if "scroll" in Inventory:
                    RoomNumber = 2
                    Inventory.remove("scroll")
                    print "\n You read the runes on the scroll and feel enveloped by power.\nYour surroundings have changed. You have been transported elsewhere!"
                else:
                    print "\n You can't use something you don't have..."
                print
                    
# sorcerer instant damage magic
        elif AttackCmd == "s" and HeroClass == "Sorcerer":
            # damage
            if BattleSpell in ArcaneBattleSpells:
                if HeroMagic >= ArcaneBattleSpells[BattleSpell][1]:
                    if FirstAttack == "monster": # Monster goes first
                        HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)
                        MonsterHealth,HeroMagic = DoHeroArcaneDamageAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell)
                    else: # Hero goes first
                        MonsterHealth,HeroMagic = DoHeroArcaneDamageAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell)
                        HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)    
                else:
                    print "Not enough mana"

# arcane healing (vampire)
            if BattleSpell in ArcaneHealingSpells:
                if HeroMagic >= ArcaneHealingSpells[BattleSpell][1]:
                    if FirstAttack == "monster": # Monster goes first
                        HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)
                        MonsterHealth,HeroMagic = DoHeroArcaneHealingAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell)    
                    else: # Hero goes first
                        MonsterHealth,HeroMagic = DoHeroArcaneHealingAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell)
                        HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)           
                else:
                    print "Not enough mana"
                    
# cleric instant damage magic
        elif AttackCmd == "s" and HeroClass == "Cleric":
            if BattleSpell in DivineBattleSpells:
                if HeroMagic >= DivineBattleSpells[BattleSpell][1]:
                    if FirstAttack == "monster": # Monster goes first
                        HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)
                        MonsterHealth,HeroMagic = DoHeroDivineDamageAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell) 
                    else: # Hero goes first
                        MonsterHealth,HeroMagic = DoHeroDivineDamageAttack(HeroHealth,MonsterHealth,HeroSpell,HeroLevel,HeroMagic,MonsterSpawn,HeroINTBonus,HeroBaseSpell)
                        HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)
                elif HeroMagic < DivineBattleSpells[BattleSpell][1]:
                    print "Not enough mana"
                    
# cleric healing
            elif BattleSpell in DivineHealingSpells:
                SpellRoll = random.randint(DivineHealingSpells[BattleSpell][2],DivineHealingSpells[BattleSpell][3])
                SpellRoll *= HeroLevel
                HealthDiff = HeroMaxHealth - HeroHealth
                if HeroMagic >= DivineHealingSpells[BattleSpell][1]:
                    if HeroHealth == HeroMaxHealth:
                        print "You are already at full heath..."
                    elif SpellRoll <= HealthDiff:
                        HeroHealth += SpellRoll
                        HeroMagic -= DivineHealingSpells[BattleSpell][1]
                        print "You have been healed for", SpellRoll, "health."
                        SpellRoll = False
                    elif SpellRoll > HealthDiff:
                        HeroHealth = HeroMaxHealth
                        HeroMagic -= DivineHealingSpells[BattleSpell][1]
                        print "You heal yourself to full health."
                        SpellRoll = False
                elif HeroMagic < DivineHealingSpells[BattleSpell][1]:
                    print "Not enough mana."
                    
                # monster attack
                HeroHealth = DoMonsterAttack(MonsterHealth,MonsterSpawn,MonsterSTRBonus,MonsterAttack,HeroHealth,HeroArmor)                

        elif AttackCmd == "s" and HeroClass == "Fighter" or AttackCmd == "s" and HeroClass == "Rogue": 
            print "You do not have the ability to spellcast."
        elif AttackCmd == "c" and HeroClass == "Fighter" or AttackCmd == "c" and HeroClass == "Rogue":
            print "You do not have the ability to chant spells."
        elif AttackCmd == "c" and HeroClass == "Cleric" or AttackCmd == "c" and HeroClass == "Sorcerer":
            print "Due to the delicate nature of chanting, it cannot be done in combat."
        else:
            print "That is not an attack choice"
        
    return (CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience)

# Function to declare or reset monster values and decide if monster is spawned as well as decide if a trap is triggered
def SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell):

    # generate a 1 in 40 chance of springing a trap
    RandomSpringTrap = random.randint(0,40)

    # decide if a random trap is sprung by roll and current room level
    if RandomSpringTrap == 40 and RoomIndex[RoomNumber][7] > 0:
        # 1 in 5 chance that the trap is instant damage
        TrapType = random.randint(1,5)
        if TrapType > 1:
            HeroPoisonTimer = (5 * HeroLevel)
            print "\n You have triggered a poison trap!"
            
        elif TrapType == 1:
            HeroHealth -= (3 * HeroLevel)
            print "\n You have triggered an explosive trap! You have been hit for", (3 * HeroLevel), "damage!"
            

    # generate a 4 in 20 chance of generating a monster
    MonsterSpawnChance = random.randint(0,19)
    if HeroHealth < 1:
        MonsterSpawnChance = 0

    # make a temp dictionary for monster of the current room level
    CurrentMonsterLevel = {}

    # populate the temp dictionary with all the monsters that match the room level
    for k,v in MonsterIndex.iteritems():
        if MonsterIndex[k][7] == RoomIndex[RoomNumber][7]:
            CurrentMonsterLevel[k]=v
    if RoomIndex[RoomNumber][7] == 0:
        MonsterSpawnChance = 0

    # if no monsters match the room level, don't try and generate anything
    if not CurrentMonsterLevel:
        MonsterSpawnChance = 0

    # generate a random monster of the current room level if it exists
    else:
        MonsterSpawn = random.choice(CurrentMonsterLevel.keys())
            
    MonsterHealth = 10
    MonsterMinDmg = 2
    MonsterMaxDmg = 4
    MonsterArmor = 0
    MonsterMagic = 0
    MonsterSpell = 0
    KillExperience = 0
    AttackChoice = ""

    if HeroCmd[:7] == "attack ":
        if HeroCmd[7:] in RoomInv[RoomNumber] and HeroCmd[7:] in MonsterIndex:
            MonsterSpawn = HeroCmd[7:]
            MonsterSpawnChance = 18
        elif HeroCmd[7:] not in RoomInv[RoomNumber]:
            print "\nThere's no", HeroCmd[7:], "to attack here."

    if MonsterSpawnChance == 1:
        # spawns a random monster that doesn't notice the hero
        MonsterHealth = MonsterIndex[MonsterSpawn][0]
        MonsterMinStat = MonsterIndex[MonsterSpawn][1]
        MonsterMaxStat = MonsterIndex[MonsterSpawn][2]
        MonsterMinDmg = MonsterIndex[MonsterSpawn][3]
        MonsterMaxDmg = MonsterIndex[MonsterSpawn][4]
        MonsterArmor = MonsterIndex[MonsterSpawn][5]
        KillExperience = MonsterIndex[MonsterSpawn][6]
        print "\nA",MonsterSpawn, "appears from the shadows, but doesn't notice you..."
        while AttackChoice != "hide":
            AttackChoice = raw_input ("\nYou choose to 'attack', or 'hide': ").lower()
            if AttackChoice == "attack":
                print "\nYou ready yourself and face your enemy..."
                CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = StartCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroMaxMagic,HeroClass,SpellChanted,HeroLevel,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,MonsterIndex,GameTurns,RoomNumber,HeroExperience,HeroHealth,MonsterSpawn,MonsterHealth,MonsterMinStat,MonsterMaxStat,MonsterMinDmg,MonsterMaxDmg,MonsterArmor,MonsterMagic,MonsterSpell,KillExperience,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
                break
            elif AttackChoice == "hide":
                print "\nYou stay still in the shadows while the", MonsterSpawn, "passes by you..."
    
    elif MonsterSpawnChance > 17:
        # spawns a random monster that attacks
        MonsterHealth = MonsterIndex[MonsterSpawn][0]
        MonsterMinStat = MonsterIndex[MonsterSpawn][1]
        MonsterMaxStat = MonsterIndex[MonsterSpawn][2]
        MonsterMinDmg = MonsterIndex[MonsterSpawn][3]
        MonsterMaxDmg = MonsterIndex[MonsterSpawn][4]
        MonsterArmor = MonsterIndex[MonsterSpawn][5]
        KillExperience = MonsterIndex[MonsterSpawn][6]
        print "\nA",MonsterSpawn, "appears from the shadows and attacks you!"
        CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = StartCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroMaxMagic,HeroClass,SpellChanted,HeroLevel,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,MonsterIndex,GameTurns,RoomNumber,HeroExperience,HeroHealth,MonsterSpawn,MonsterHealth,MonsterMinStat,MonsterMaxStat,MonsterMinDmg,MonsterMaxDmg,MonsterArmor,MonsterMagic,MonsterSpell,KillExperience,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)

    return (CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience)

# Each area has it's own unique room number. A description is printed depending on the room number with appropriate exits
def RoomText(RoomNumber):
    
    # pull from RoomDescription dictionary
    TextInRoom = RoomDescription[RoomNumber]
    WrappedText = textwrap.dedent(TextInRoom).strip()
    print textwrap.fill(WrappedText, width=75)

    # if a room has the display exits flagged, then print them out
    RoomExits = []
    if RoomIndex[RoomNumber][6] == 1:
        if RoomIndex[RoomNumber][0] > 0:
            RoomExits.append("North")
        if RoomIndex[RoomNumber][1] > 0:
            RoomExits.append("South")
        if RoomIndex[RoomNumber][2] > 0:
            RoomExits.append("East")
        if RoomIndex[RoomNumber][3] > 0:
            RoomExits.append("West")
        if RoomIndex[RoomNumber][4] > 0:
            RoomExits.append("Up")
        if RoomIndex[RoomNumber][5] > 0:
            RoomExits.append("Down")
        print "You see the following exits:", ", ".join(RoomExits)    

# When a direction command is entered, translate the input to the appropriate room number change
# More rooms can be added by adding another 'if RoomNumber == ?' and adding the approriate description in RoomText
def RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay):
    
# conditions match the RoomIndex to the Current RoomNumber and extract the available exits. if it's greater than 0, it changes RoomNumber to corresponding list item
    if HeroCmd == "n":
        if RoomIndex[RoomNumber][0] == 0:
            WallBump()
        else:
            RoomNumber = RoomIndex[RoomNumber][0]
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomEvent(RoomNumber,Inventory)
    elif HeroCmd == "s":
        if RoomIndex[RoomNumber][1] == 0:
            WallBump()
        else:
            RoomNumber = RoomIndex[RoomNumber][1]
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomEvent(RoomNumber,Inventory)
    elif HeroCmd == "e":
        if RoomIndex[RoomNumber][2] == 0:
            WallBump()
        else:
            RoomNumber = RoomIndex[RoomNumber][2]
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomEvent(RoomNumber,Inventory)
    elif HeroCmd == "w":
        if RoomIndex[RoomNumber][3] == 0:
            WallBump()
        else:
            RoomNumber = RoomIndex[RoomNumber][3]
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomEvent(RoomNumber,Inventory)
    elif HeroCmd == "u":
        if RoomIndex[RoomNumber][4] == 0:
            WallBump()
        else:
            RoomNumber = RoomIndex[RoomNumber][4]
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomEvent(RoomNumber,Inventory)
    elif HeroCmd == "d":
        if RoomIndex[RoomNumber][5] == 0:
            WallBump()
        else:
            RoomNumber = RoomIndex[RoomNumber][5]
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomEvent(RoomNumber,Inventory)         
    else:
        print "debugging - invalid room number"

    return (HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)

def RoomEvent(RoomNumber,Inventory):
    if RoomNumber in PawnshopRooms:
        if Inventory:
            NPCSeeItem = random.choice(Inventory)
            print "The shop owner looks you over. 'I may have a buyer for your", NPCSeeItem + "."
            if NPCSeeItem in WeaponStats:
                print "I can give you", WeaponStats[NPCSeeItem][1], "gold for that.'"
            elif NPCSeeItem in ArmorStats:
                print "I can give you", ArmorStats[NPCSeeItem][1], "gold for that.'"
            elif NPCSeeItem in ShieldStats:
                print "I can give you", ShieldStats[NPCSeeItem][1], "gold for that.'"
            elif NPCSeeItem in LootItems:
                print "I can give you", LootItems[NPCSeeItem][1], "gold for that.'"
            elif NPCSeeItem in RareLootItems:
                print "I can give you", RareLootItems[NPCSeeItem][1], "gold for that.'"

    if RoomNumber in BlacksmithRooms:
        RandomSalesPitch = random.randint(1,3)
        if RandomSalesPitch == 1:
            NPCSalesPitch = random.choice(WeaponStats.keys())
            print "The burly blacksmith grins at you as you enter."
            if WeaponStats[NPCSalesPitch][5] == 1:
                print "'We have a special on", NPCSalesPitch +"s. Only", WeaponStats[NPCSalesPitch][0], "gold!'"
        elif RandomSalesPitch == 2:
            NPCSalesPitch = random.choice(ArmorStats.keys())
            print "The burly blacksmith grins at you as you enter."
            if ArmorStats[NPCSalesPitch][4] == 1:
                print "'We have a special on", NPCSalesPitch +"s. Only", ArmorStats[NPCSalesPitch][0], "gold!'"
        elif RandomSalesPitch == 3:
            NPCSalesPitch = random.choice(ShieldStats.keys())
            print "The burly blacksmith grins at you as you enter."
            if ShieldStats[NPCSalesPitch][4] == 1:
                print "'We have a special on", NPCSalesPitch +"s. Only", ShieldStats[NPCSalesPitch][0], "gold!'"

# Main Program Loop
def MainProgram(RoomNumberStart,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,RoomInv,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroCmd,HeroName,RoomNumber,WeaponSlot,ArmorSlot,ShieldSlot,GameTurns):
    while HeroCmd != "quit":

# Check if the player is dead
        if HeroHealth < 1:
            print "\nYou have died!!!...\n"
            print "You wake up in a small corner of the church. A priest looks over you with"
            print "concern. 'We feared the worst' He says. 'But alas, it appears the Gods still"
            print "have use for you... With a suitable donation of gold, of course...'"
            RoomNumber = ResurrectionRooms[0]
            HeroHealth = HeroMaxHealth
            HeroMagic = HeroMaxMagic
            HeroPoisonTimer = 0
            
            HeroGold -= (20 * HeroLevel)
            if HeroGold < 0:
                HeroGold = 0
        
        # This is the main string input for commands from the hero
        print
        RepeatCmd = HeroCmd
        HeroCmd = raw_input ("HP:" + str(HeroHealth) + "/" + str(HeroMaxHealth) + " MP:" + str(HeroMagic) + "/" + str(HeroMaxMagic) + " > ").lower()
        if HeroCmd == "r":
            print "Repeating Last Command: '" + RepeatCmd + "'"
            HeroCmd = RepeatCmd
        
        # Convert inputs to common commands
        if HeroCmd in AltCmd:
            HeroCmd = AltCmd[HeroCmd]
           
        #command, args = HeroCmd.split(maxsplit = 1)
        
        # Route inputs to proper functions
        if HeroCmd == "n":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay = RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)
            RoomItems(RoomInv, RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "s":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay = RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)
            RoomItems(RoomInv, RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "e":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay = RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)
            RoomItems(RoomInv, RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "w":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay = RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)
            RoomItems(RoomInv, RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "u":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay = RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)
            RoomItems(RoomInv, RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "d":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay = RoomMove(Inventory,HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,RoomNumber,HeroCmd,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay)
            RoomItems(RoomInv, RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "i":
            HeroEquipped(ItemsWorn)
            HeroInv(HeroGold,Inventory)
        elif HeroCmd[:7] == "search ":
            HeroGold,RoomInv = SearchItems(HeroGold,RoomInv,RoomNumber,HeroCmd,HeroLevel)
        elif HeroCmd == "look":
            WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
            RoomText(RoomNumber)
            RoomItems(RoomInv, RoomNumber)
        elif HeroCmd[:5] == "look ":
            ItemLook(HeroCmd,RoomNumber)
        elif HeroCmd == "time":
            LookTime(TimeOfDay,TimeOfDayTimer)
        elif HeroCmd[:4] == "get ":
            GetItem(RoomInv,RoomNumber,HeroCmd,SolidItem)
        elif HeroCmd[:5] == "drop ":
            DropItem(RoomInv,RoomNumber,HeroCmd)
        elif HeroCmd[:4] == "use ":
            HeroHealth,RoomNumber = UseItem(HeroCmd,HeroHealth,HeroMaxHealth,RoomNumber)
        elif HeroCmd[:6] == "equip ":
            HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot = EquipItem(HeroSTRBonus,HeroClass,HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot, HeroCmd)
        elif HeroCmd[:7] == "remove ":
            HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot = RemoveItem(HeroSTRBonus,HeroMinDmg,HeroMaxDmg,HeroArmor,WeaponSlot,ArmorSlot,ShieldSlot, HeroCmd)
        elif HeroCmd[:4] == "buy ":
            HeroGold = BuyItems(HeroCmd,RoomNumber,HeroGold)
        elif HeroCmd[:5] == "sell ":
            HeroGold = SellItems(HeroCmd,RoomNumber,HeroGold)
        elif HeroCmd == "stats":
            HeroStats(HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroExperience,HeroGold,HeroName)
        elif HeroCmd == "status":
            HeroStatus (HeroPoisonTimer,HeroLevel,HeroHealth,HeroMaxHealth,HeroMagic,HeroMaxMagic,HeroArmor,HeroAttack,HeroMinDmg,HeroMaxDmg,HeroBaseSpell,HeroSpell,SpellChanted,ItemsWorn)
        elif HeroCmd == "weapon prices":
            ShopItemWeapon(RoomNumber)
        elif HeroCmd == "armor prices":
            ShopItemArmor(RoomNumber)
        elif HeroCmd == "shield prices":
            ShopItemShield(RoomNumber)
        elif HeroCmd == "arcane spells":
            ShopArcaneSpells(RoomNumber,HeroLevel)
        elif HeroCmd == "divine spells":
            ShopDivineSpells(RoomNumber,HeroLevel)
        elif HeroCmd == "potion prices":
            ShopPotions(RoomNumber)
        elif HeroCmd == "training prices":
            TrainPrice(RoomNumber)
        elif HeroCmd == "train":
            HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroGold,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMaxMagic,HeroSpell = HeroTrain(RoomNumber,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroGold,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMaxMagic,HeroSpell)
        elif HeroCmd == "xyzzy":
            print "\nCareful what you type. You are likely to be eaten by a grue..."
        elif HeroCmd[:6] == "learn ":
            HeroGold,HeroSpells = LearnSpell(HeroCmd,RoomNumber,HeroGold,HeroClass,HeroSpells)
        elif HeroCmd[:7] == "attack ":
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd[:5] == "cast ":
            HeroMagic,HeroHealth = CastSpell(SpellChanted,HeroCmd,HeroMagic,HeroHealth,HeroMaxHealth,HeroSpells)
        elif HeroCmd[:6] == "chant ":
            SpellChanted,HeroBaseSpell,HeroSpell = ChantSpell(HeroClass,HeroCmd,SpellChanted,HeroSpells,HeroSpell,HeroBaseSpell,ArcaneBattleSpells,DivineBattleSpells)
        elif HeroCmd == "spellbook":
            SpellBook(HeroSpells)
        elif HeroCmd == "rest":
            HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroHealth,HeroMagic,RoomNumber = HeroRest(HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMaxHealth,HeroHealth,HeroMaxMagic,HeroMagic,RoomNumber)
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
        elif HeroCmd == "help":
            CmdHelp()
        elif HeroCmd == "savegame":
            SaveGame(HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns)
        elif HeroCmd == "q":
            QuitConfirm = raw_input ("\nAre you sure you wish to quit the program? (Y/N) ").lower()
            if QuitConfirm == "y":
                print "\nThanks for playing!\n"
                return
            else:
                print "\nI knew you would rather stay..."
                HeroCmd = ""
###        elif HeroCmd == "savecamp":
###            import pickle
###             SaveInfo = (RoomNumberStart,Inventory,HeroSpells,ItemsWorn,BlacksmithRooms,PawnshopRooms,ApothecaryRooms,ArcaneSpellshopRooms,DivineSpellshopRooms,FighterTrainerRooms,RogueTrainerRooms,SorcererTrainerRooms,ClericTrainerRooms,ResurrectionRooms,IntroText,RoomDescription,RoomIndex,RoomInv,MonsterIndex,SolidItem,SolidItem2,LootItems,WeaponStats,ArmorStats,ShieldStats,UseableItems,ArcaneBattleSpells,DivineBattleSpells,ArcaneHealingSpells,DivineHealingSpells,ArcaneBuffSpells,DivineBuffSpells,SpecialArcane,SpecialDivine)
###             with open('Custom1.cmp', 'wb') as output:
###                 pickle.dump(SaveInfo, output)
###             print "\nThe campaign is now saved..."

# Gold debugging
        elif HeroCmd == "gold dupe":
             HeroGold += 10
             print "\nYou now have",HeroGold,"gold, you cheater..."
            
# Debugging commands:
###        elif HeroCmd == "debug":
###             print "RoomNumber:",RoomNumber
###             print "WeaponSlot:",WeaponSlot
###             print "ArmorSlot:",ArmorSlot
###             print "ShieldSlot:",ShieldSlot
###             print "GameTurns:",GameTurns
###             print "HeroSTRBonus:",HeroSTRBonus
###             print "HeroDEXBonus:",HeroDEXBonus
###             print "HeroINTBonus:",HeroINTBonus
###             print "TimeOfDayTimer:",TimeOfDayTimer
###             print "TimeOfDay:",TimeOfDay
###             print "WeatherTimer:",WeatherTimer
###             print "CurrentWeather:",CurrentWeather
###             print "HeroBuff:",HeroBuff
###             print "HeroPoison:",HeroPoison
###             print "HeroBuffTimer:",HeroBuffTimer
###             print "HeroPoisonTimer:",HeroPoisonTimer
      
        elif HeroCmd == "":
            HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber = TurnTimer(HeroHealth,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,GameTurns,WeatherTimer,TimeOfDayTimer,TimeOfDay,RoomNumber)
            NoCmd = random.randint(0,3)
            if NoCmd == 0:
                print "\nYou shift your weight from one foot to the other..."
            elif NoCmd == 1:
                print "\nYou stand and contemplate your next move..."
            elif NoCmd == 2:
                print "\nYou look around, paranoid someone is watching you..."
            elif NoCmd == 3:
                print "\nYou do a little stretching..."
            CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,SpellChanted,GameTurns,RoomNumber,HeroHealth,HeroMagic,HeroExperience = SpawnCombat(CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,HeroGold,HeroLevel,HeroClass,HeroMaxMagic,SpellChanted,HeroCmd,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroAttack,GameTurns,RoomNumber,HeroExperience,HeroHealth,HeroMaxHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell)
   
        else:
            print "\nThat is not a recognized command..."

    return (HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroGold,HeroCmd,HeroName,RoomNumber,WeaponSlot,ArmorSlot,ShieldSlot)

# Function to create new game
def NewGame(RoomNumberStart,HeroName,IntroText):
    while HeroName == False:
        HeroName = raw_input("\n What is your name, hero? ").title()
        print "\n From henceforth your name shall be known as: "+ HeroName
        HeroNameTrue = raw_input ("\n Is this correct? (Y/N)").lower()
        if HeroNameTrue == "y":

            HeroMaxHealth = 15
            HeroBaseMinDmg = 1
            HeroBaseMaxDmg = 2
            HeroBaseArmor = 0
            HeroMaxMagic = 0
            HeroBaseSpell = 0
            HeroSpell = 0
            HeroLevel = 1
            HeroRace = False
            HeroClass = False
            HeroSTR = 3
            HeroSTA = 3
            HeroDEX = 3
            HeroINT = 3
            HeroAttack = 0
            HeroSTRBonus = 0
            HeroDEXBonus = 0
            HeroINTBonus = 0
            HeroSpells = []
            SpellChanted = []
            SpellChanted,HeroSpells,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroMaxHealth,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroSpell = RollStats(SpellChanted,HeroSpells,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroMaxHealth,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroSpell)
            HeroHealth = HeroMaxHealth
            HeroMinDmg = HeroBaseMinDmg
            HeroMaxDmg = HeroBaseMaxDmg
            HeroArmor = HeroBaseArmor
            HeroMagic = HeroMaxMagic
            TimeOfDayTimer = 180
            TimeOfDay = "Daytime"
            WeatherTimer = 60
            CurrentWeather = 1
            HeroBuffTimer = 0
            HeroPoisonTimer = 1
            HeroBuff = 0
            HeroPoison = 0
            
            WrappedText = textwrap.dedent(IntroText[0]).strip()
            print
            print textwrap.fill(WrappedText, width=75)
            
            HeroName = MainProgram(RoomNumberStart,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,RoomInv,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroCmd,HeroName,RoomNumber,WeaponSlot,ArmorSlot,ShieldSlot,GameTurns)
        else:
            HeroName = False

# Game start
while GameChoice != "q":
    print
    print " Welcome to:"
    print " _                           _"
    print "(_ |_  _  _| _     _     _ _|_   |/  _  |  _  _  _| _  |  _ "
    print "__)| |(_|(_|(_)\^/_>    (_) |    |\ (_| | (/_| |(_|(_| | (/_"
    print
    print " A text-based RPG"
    print " Revision 00000.87"
    print
    print " Programming by:"
    print "   Michael Kadlec"
    print "   Daniel Foerster"
    print
    print " Creative Design and Playtesting:"
    print "   Stephanie Kelly"
    print "   Jon Copeland"
    print
    print "  (C)reate a new game"
    print "  (L)oad an existing game"
    print "  (H)elp"
    print "  (Q)uit"
    GameChoice = raw_input ("\n Please make a choice: ").lower()
    if GameChoice == "c":
        RoomNumber = RoomNumberStart
        HeroName = NewGame(RoomNumberStart,HeroName,IntroText)
        break
    elif GameChoice == "l":
        HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns = LoadGame(HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroName,ArmorSlot,WeaponSlot,RoomNumber,ShieldSlot,Inventory,ItemsWorn,RoomInv,GameTurns)
        WeatherView(RoomNumber,WeatherTimer,CurrentWeather)
        RoomText(RoomNumber)
        MainProgram(RoomNumberStart,HeroBuff,HeroPoison,HeroBuffTimer,HeroPoisonTimer,CurrentWeather,WeatherTimer,TimeOfDayTimer,TimeOfDay,HeroMagicAttack,HeroSpells,SpellChanted,HeroSTRBonus,HeroDEXBonus,HeroINTBonus,HeroRace,HeroClass,HeroSTR,HeroSTA,HeroDEX,HeroINT,HeroAttack,RoomInv,HeroLevel,HeroBaseMinDmg,HeroBaseMaxDmg,HeroBaseArmor,HeroMaxMagic,HeroBaseSpell,HeroExperience,HeroMaxHealth,HeroHealth,HeroMinDmg,HeroMaxDmg,HeroArmor,HeroMagic,HeroSpell,HeroGold,HeroCmd,HeroName,RoomNumber,WeaponSlot,ArmorSlot,ShieldSlot,GameTurns)
        break
    elif GameChoice == "h":
        print "\n You can access the list of commands in-game by typing 'help'\n"
    elif GameChoice == "q":
        print "\n Sorry to see you go so soon...\n"

raw_input()
