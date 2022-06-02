# Fantasy Hockey League (FHL)

pip install:
flask
flask_login
request
psycopg2
pytz

GIT: https://github.com/mackele/FantasyHockeyLeague

HTML / CSS / JSS-ursprung: 
Emilia: huvudansvarig för html/css
Simon: huvudansvarig för JS 
Alexander: hjälpt till efter hand 
Lukas: hjälpt till efter hand 
Marcus: hjälpt till efter hand 


Att tänka på:
Första gången programmet körs för dagen kommer indexsidan att laddas långsamt då ny data hämtas om dagens matcher, 
lagens statistik från NHL:s API.

Första gången programmet körs för dagen kommer en av sidorna buy_players, my_players, match, play_game att köras långsamt
då ny data hämtas från NHL:s API och bearbetas innan det läggs in i databasen. Detta tar ca 5 minuter.

Det är enbart möjligt att skapa ett lag per dag. Detta lag kan enbart spelas med under nästkommande dag när ny statistik har hämtas från NHL:s API. Det går att kringgå detta genom att köra funktionen "insert_score_to_database()" i team_score för att hämta ny statistik direkt.

