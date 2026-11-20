/* Ecrit par tools/textes_quest.py -- NE PAS EDITER A LA MAIN.
 *
 * Les textes du Quest, ajoutes a la suite des 23052 de Final
 * Showdown dans `rom/string_array.farc`. A gauche le numero de
 * la version Xbox 360 (2007), a droite le notre.
 */
#define QUEST_TEXTE_BASE   23052
#define QUEST_TEXTE_NOMBRE 492

static const struct { int x360, fs; } g_quest_textes[] = {
    {     0, 23052 },   /* .:Enter */
    {     1, 23053 },   /* .:Select */
    {     2, 23054 },   /* .:Cancel  .:Enter */
    {     3, 23055 },   /* .:Back  .:Enter */
    {     4, 23056 },   /* .:Cancel */
    {     5, 23057 },   /* .:Back */
    {     6, 23058 },   /* ..:Switch costumes  .:Enter */
    {     7, 23059 },   /* .:Save new replay  .:Back  .:Enter */
    {     8, 23060 },   /* ....:Toggle display  .:Enter */
    {     9, 23061 },   /* .:gamer card  .:Enter */
    {    10, 23062 },   /* .:gamer card  .:Back  .:Enter */
    {    11, 23063 },   /* ..:Home Menu  .:Enter */
    {    12, 23064 },   /* ..:Switch costumes  .:Back  .:Enter */
    {    13, 23065 },   /* ..:View tournament chart  .:Enter */
    {    14, 23066 },   /* ..:Open window */
    {    15, 23067 },   /* .:Enter tournament */
    {    16, 23068 },   /* ..:Delete data  .:Back  .:Enter */
    {    17, 23069 },   /* ....:Rotate  .:Back  .:Enter */
    {    18, 23070 },   /* ....:Zoom  ....:Rotate  .:Back  .:Enter */
    {    19, 23071 },   /* .:Delete  .:Enter */
    {    20, 23072 },   /* .:Delete  .:Back  .:Enter */
    {    21, 23073 },   /* .:Undo changes  .:Delete  .:Enter */
    {    22, 23074 },   /* .:Undo changes  .:Delete  .:Back  .:Enter */
    {    23, 23075 },   /* .:Backspace  .:Enter */
    {    24, 23076 },   /* ..:Initialize rankings  .:Back  .:Toggle ran */
    {    25, 23077 },   /* ..:Initialize  .:Back  .:Toggle rankings */
    {    26, 23078 },   /* ..:Delete file  ..:Options  .:Cancel  .:Ente */
    {    27, 23079 },   /* .:Play from beginning  .:Pause  .:Frame-by-f */
    {    28, 23080 },   /* .:Play from beginning  .:Play  .:Frame-by-fr */
    {    29, 23081 },   /* .:Open */
    {    30, 23082 },   /* .:Continuous play  .:Random play  .:Back  .: */
    {    31, 23083 },   /* ..:Play demo  .:Back  .:Enter */
    {    32, 23084 },   /* ..:Play demo  .:Back */
    {    33, 23085 },   /* .:Lock move  .:Back  .:Enter */
    {    34, 23086 },   /* .:Unlock  .:Back */
    {    35, 23087 },   /* ..:Play demo  .:Lock move  .:Back  .:Enter */
    {    36, 23088 },   /* ..:Play demo  .:Unlock  .:Back */
    {    37, 23089 },   /* Press the . button to cancel */
    {    38, 23090 },   /* ..:Help  ..:Toggle  .:Back */
    {    39, 23091 },   /* ..:Toggle  .:Back */
    {    40, 23092 },   /* .:gamer card */
    {    41, 23093 },   /* ..:Next */
    {    42, 23094 },   /* .:Enter */
    {    43, 23095 },   /* .:Select */
    {    44, 23096 },   /* .:Cancel  .:Enter */
    {    45, 23097 },   /* .:Back  .:Enter */
    {    46, 23098 },   /* .:Cancel */
    {    48, 23099 },   /* ..:Switch costumes  .:Enter */
    {    50, 23100 },   /* ....:Toggle display  .:Enter */
    {    59, 23101 },   /* ....:Rotate  .:Back  .:Enter */
    {    60, 23102 },   /* ....:Zoom  ....:Rotate  .:Back  .:Enter */
    {    61, 23103 },   /* .:Delete  .:Enter */
    {    62, 23104 },   /* .:Delete  .:Back  .:Enter */
    {    63, 23105 },   /* .:Undo changes  .:Delete  .:Enter */
    {    64, 23106 },   /* .:Undo changes  .:Delete  .:Back  .:Enter */
    {    67, 23107 },   /* ..:Initialize  .:Back  .:Toggle rankings */
    {    72, 23108 },   /* .:Continuous play  .:Random play  .:Back  .: */
    {    74, 23109 },   /* ..:Play demo  .:Back */
    {    75, 23110 },   /* .:Lock move  .:Back  .:Enter */
    {    76, 23111 },   /* .:Unlock  .:Back */
    {    77, 23112 },   /* ..:Play demo  .:Lock move  .:Back  .:Enter */
    {    80, 23113 },   /* ..:Help  ..:Toggle  .:Back */
    {    81, 23114 },   /* ..:Toggle  .:Back */
    {    82, 23115 },   /* .:gamer card */
    {    83, 23116 },   /* ..:Next */
    {    84, 23117 },   /* Fight against CPU-controlled opponents. */
    {    85, 23118 },   /* Duel against a human opponent. */
    {    86, 23119 },   /* Fight rivals as you work your way through di */
    {    87, 23120 },   /* Fight rivals as you work your way through di */
    {    88, 23121 },   /* Improve your fighting skills and techniques. */
    {    89, 23122 },   /* View replays. */
    {    90, 23123 },   /* View replays, movies and rankings. */
    {    92, 23124 },   /* Manage your game settings and saved Game Dat */
    {    94, 23125 },   /* Play with custom settings available. Hold RB */
    {    95, 23126 },   /* Play with custom settings available. (Other  */
    {    96, 23127 },   /* Play using standard competition settings and */
    {    97, 23128 },   /* Play using standard competition settings and */
    {    99, 23129 },   /* Duel against a human opponent with custom se */
    {   100, 23130 },   /* Duel on Xbox LIVE against human opponents. */
    {   101, 23131 },   /* Duel on Xbox LIVE, with the results affectin */
    {   102, 23132 },   /* Play on Xbox LIVE without affecting rankings */
    {   103, 23133 },   /* Cannot play multiplayer online games on Xbox */
    {   104, 23134 },   /* Cannot select this mode--incorrect connectio */
    {   109, 23135 },   /* Set conditions to create a session. Play on  */
    {   110, 23136 },   /* Quickly search for an opponent without setti */
    {   111, 23137 },   /* Set conditions to search for an opponent. Pl */
    {   113, 23138 },   /* Change your personal comment for online play */
    {   114, 23139 },   /* Return to the Character Select Screen. */
    {   115, 23140 },   /* End Xbox LIVE play and return to the VS. Men */
    {   122, 23141 },   /* End adjustment and create a session. */
    {   127, 23142 },   /* Choose your destination. You can adjust vari */
    {   128, 23143 },   /* Home: Adjust various settings. (You can also */
    {   129, 23144 },   /* A well-known arcade where many advanced play */
    {   130, 23145 },   /* An elite arcade frequented by many high-rank */
    {   131, 23146 },   /* A popular arcade with many players, ranging  */
    {   132, 23147 },   /* A crowded arcade packed with many beginning  */
    {   133, 23148 },   /* An arcade with a wide range of skill levels, */
    {   134, 23149 },   /* A lively arcade with a welcoming environment */
    {   135, 23150 },   /* An arcade that attracts all skill levels for */
    {   136, 23151 },   /* The arena where official Virtua Fighter tour */
    {   137, 23152 },   /* Purchase items or adjust settings. */
    {   138, 23153 },   /* View various records. */
    {   139, 23154 },   /* Adjust the difficulty level. */
    {   140, 23155 },   /* Adjust difficulty level and commentary setti */
    {   141, 23156 },   /* Save current settings. */
    {   142, 23157 },   /* Return to the Character Select Screen. */
    {   143, 23158 },   /* End Quest Mode and return to the Main Menu. */
    {   144, 23159 },   /* Return to default settings. */
    {   145, 23160 },   /* Finish adjustments and return to the Home Me */
    {   146, 23161 },   /* Play against the opponent on Unit 1. */
    {   147, 23162 },   /* Play against the opponent on Unit 2. */
    {   148, 23163 },   /* Play against the opponent on Unit 3. */
    {   149, 23164 },   /* %s is on a %d-win streak! */
    {   150, 23165 },   /* Participate in a tournament. */
    {   152, 23166 },   /* View official tournaments you have cleared. */
    {   153, 23167 },   /* Purchase items or adjust settings. */
    {   154, 23168 },   /* Practice commands. */
    {   200, 23169 },   /* Set the CPU's reaction to neutral. (No CPU i */
    {   201, 23170 },   /* All hits will land as normal hits. */
    {   226, 23171 },   /* Select how the CPU recovers from falls. */
    {   246, 23172 },   /* Finish adjustments and return to the game. */
    {   247, 23173 },   /* View replays. */
    {   251, 23174 },   /* A collection of useful combos for each chara */
    {   252, 23175 },   /* View rankings. */
    {   254, 23176 },   /* Select a character to view. */
    {   255, 23177 },   /* Select a movie to view. */
    {   256, 23178 },   /* Adjust command display for the 1P (left) pla */
    {   262, 23179 },   /* Select an exhibition match to view. */
    {   263, 23180 },   /* Adjust command display for the 1P (left) pla */
    {   264, 23181 },   /* Adjust input display for the 1P (left) playe */
    {   265, 23182 },   /* Adjust command display for the 2P (right) pl */
    {   266, 23183 },   /* Adjust input display for the 2P (right) play */
    {   267, 23184 },   /* Adjust commentary settings. */
    {   268, 23185 },   /* Implement settings and exit Replay Options. */
    {   269, 23186 },   /* Change ranking type. */
    {   270, 23187 },   /* Change ranking character. */
    {   291, 23188 },   /* Select an item to buy. */
    {   296, 23189 },   /* Select emblem type. */
    {   297, 23190 },   /* Select emblem. */
    {   298, 23191 },   /* Adjust game settings. */
    {   299, 23192 },   /* Adjust controller settings. */
    {   301, 23193 },   /* Adjust sound settings. */
    {   302, 23194 },   /* Manage saved Game Data. */
    {   304, 23195 },   /* Adjust CPU skill level. */
    {   305, 23196 },   /* Adjust the number of rounds required to win. */
    {   306, 23197 },   /* Adjust the time limit for each round. */
    {   307, 23198 },   /* Adjust the health bar for the player. */
    {   308, 23199 },   /* Adjust the health bar for the CPU. */
    {   309, 23200 },   /* Adjust commentary settings. */
    {   310, 23201 },   /* Adjust the number of rounds required to win. */
    {   311, 23202 },   /* Adjust the time limit for each round. (Offli */
    {   312, 23203 },   /* Adjust the health bar for the 1P (left) play */
    {   313, 23204 },   /* Adjust the health bar for the 2P (right) pla */
    {   314, 23205 },   /* Adjust the stage selection method. (Offline  */
    {   315, 23206 },   /* Adjust commentary settings. */
    {   316, 23207 },   /* Return to default settings. */
    {   317, 23208 },   /* Finish adjustments and return to the Options */
    {   318, 23209 },   /* Adjust controller settings. */
    {   320, 23210 },   /* Select a controller to adjust using left/rig */
    {   321, 23211 },   /* Adjust the display. */
    {   323, 23212 },   /* Adjust display position (horizontal). */
    {   324, 23213 },   /* Adjust display position (vertical). */
    {   325, 23214 },   /* Return to default settings. */
    {   326, 23215 },   /* Finish adjustments and return to the Options */
    {   328, 23216 },   /* Play sound effects. */
    {   330, 23217 },   /* Select ambient sound setting. Features addit */
    {   331, 23218 },   /* Select ambient sound setting. Faithfully rep */
    {   332, 23219 },   /* Adjust volume for sound effects. */
    {   333, 23220 },   /* Adjust volume for background music. */
    {   334, 23221 },   /* Adjust volume for commentary. */
    {   335, 23222 },   /* Return to default settings. */
    {   336, 23223 },   /* Finish adjustments and return to the Options */
    {   337, 23224 },   /* Save current status. */
    {   338, 23225 },   /* Load Game Data. */
    {   340, 23226 },   /* Adjust autosave settings. */
    {   341, 23227 },   /* Select a different storage device to save Ga */
    {   342, 23228 },   /* Adjust autosave settings. */
    {   343, 23229 },   /* Finish adjustments and return to the Save Da */
    {   348, 23230 },   /* Yes */
    {   349, 23231 },   /* No */
    {   352, 23232 },   /* OK */
    {   367, 23233 },   /* Goh */
    {   369, 23234 },   /* El Blaze */
    {   370, 23235 },   /* Test 1 */
    {   371, 23236 },   /* Test 2 */
    {   376, 23237 },   /* SARAH */
    {   377, 23238 },   /* LAU */
    {   396, 23239 },   /* W:%6d */
    {   397, 23240 },   /* L:%6d */
    {   398, 23241 },   /* W:%-6d */
    {   399, 23242 },   /* L:%-6d */
    {   400, 23243 },   /* Win ratio: */
    {   401, 23244 },   /* % */
    {   402, 23245 },   /* %d Wins */
    {   403, 23246 },   /* %d */
    {   404, 23247 },   /* %d:%d:%d */
    {   422, 23248 },   /* Return to the game */
    {   423, 23249 },   /* Command list */
    {   424, 23250 },   /* Controller settings */
    {   425, 23251 },   /* Return to the Main Menu */
    {   426, 23252 },   /* Return to the Arcade Screen */
    {   428, 23253 },   /* Return to the Event Square */
    {   429, 23254 },   /* Replay settings */
    {   431, 23255 },   /* Return to Replay */
    {   432, 23256 },   /* Play from the beginning */
    {   434, 23257 },   /* Return to the Arcade Menu */
    {   435, 23258 },   /* Return to the VS. Menu */
    {   436, 23259 },   /* Return to Rankings */
    {   440, 23260 },   /* Route B */
    {   500, 23261 },   /* You have requested a player match. To play a */
    {   512, 23262 },   /* Search for other opponents? */
    {   518, 23263 },   /* View opponent's gamer card */
    {   523, 23264 },   /* Starting Quest Mode. On the Map Screen, sele */
    {   528, 23265 },   /* SEGA WORLD NORTH */
    {   529, 23266 },   /* SEGA WORLD SOUTH */
    {   530, 23267 },   /* SEGA WORLD ROUTE 101 */
    {   531, 23268 },   /* CLUB SEGA DOWNTOWN */
    {   532, 23269 },   /* CLUB SEGA BAY AREA */
    {   533, 23270 },   /* SEGA ARENA COAST */
    {   534, 23271 },   /* SEGA ARENA EAST */
    {   535, 23272 },   /* EVENT SQUARE */
    {   537, 23273 },   /* Customize */
    {   538, 23274 },   /* Status */
    {   540, 23275 },   /* Quest settings */
    {   541, 23276 },   /* Save */
    {   542, 23277 },   /* Return to Character Select */
    {   543, 23278 },   /* End Quest Mode */
    {   544, 23279 },   /* STATUS */
    {   545, 23280 },   /* Rivals defeated */
    {   546, 23281 },   /* Items collected */
    {   547, 23282 },   /* Emblems collected */
    {   548, 23283 },   /* Overall completion rating */
    {   549, 23284 },   /* Longest streak */
    {   550, 23285 },   /* Total number of matches */
    {   551, 23286 },   /* Total playing time */
    {   552, 23287 },   /* Number of matches */
    {   553, 23288 },   /* Completion time */
    {   554, 23289 },   /* View rival list */
    {   555, 23290 },   /* View emblem list */
    {   556, 23291 },   /* Special */
    {   557, 23292 },   /* Your overall completion rating is 100%%. Whe */
    {   558, 23293 },   /* RIVAL LIST */
    {   560, 23294 },   /* Arcade completion rating:  */
    {   562, 23295 },   /* Difficulty */
    {   563, 23296 },   /* Normal */
    {   564, 23297 },   /* Hard */
    {   565, 23298 },   /* Expert */
    {   566, 23299 },   /* Commentary */
    {   567, 23300 },   /* On */
    {   568, 23301 },   /* Off */
    {   569, 23302 },   /* EMBLEM LIST */
    {   570, 23303 },   /* Emblems collected:  */
    {   571, 23304 },   /* Alphabet */
    {   572, 23305 },   /* Japanese */
    {   573, 23306 },   /* Animals */
    {   574, 23307 },   /* Food */
    {   575, 23308 },   /* Crests */
    {   576, 23309 },   /* Jobs */
    {   577, 23310 },   /* Characters */
    {   578, 23311 },   /* Space */
    {   579, 23312 },   /* Logos */
    {   580, 23313 },   /* Hobbies */
    {   581, 23314 },   /* Plants */
    {   582, 23315 },   /* Colors */
    {   583, 23316 },   /* Other */
    {   584, 23317 },   /* Bonus */
    {   587, 23318 },   /* Obtained the following item(s): */
    {   588, 23319 },   /* The following emblem(s) can now be used: */
    {   589, 23320 },   /* 1 */
    {   590, 23321 },   /* 2 */
    {   591, 23322 },   /* 3 */
    {   592, 23323 },   /* Tournament */
    {   593, 23324 },   /* Currently not in progress. */
    {   594, 23325 },   /* Customize */
    {   599, 23326 },   /* Official Tournaments */
    {   600, 23327 },   /* Currently not in progress. */
    {   601, 23328 },   /* List of official tournaments */
    {   602, 23329 },   /* Customize */
    {   607, 23330 },   /* You have not cleared any tournaments. */
    {   609, 23331 },   /* Prize: %s */
    {   612, 23332 },   /* Prize: %s */
    {   614, 23333 },   /* The following tournament has begun: */
    {   615, 23334 },   /* Official Tournament */
    {   616, 23335 },   /* Return to the Arcade Screen. */
    {   617, 23336 },   /* The following tournament has begun: */
    {   618, 23337 },   /* Official Tournament */
    {   619, 23338 },   /* Do you want to return to the Arcade Screen?  */
    {   620, 23339 },   /* Participants: %d */
    {   621, 23340 },   /* Rounds: %d */
    {   622, 23341 },   /* Time: %d */
    {   624, 23342 },   /* 1st place: %dG 2nd place: %dG 3rd place: %dG */
    {   625, 23343 },   /* 1st place: Item 2nd place: %dG 3rd place: %d */
    {   626, 23344 },   /* 1st place: Emblem 2nd place: %dG 3rd place:  */
    {   627, 23345 },   /* Official tournament. Place in the tournament */
    {   629, 23346 },   /* Do you want to enter this tournament? */
    {   634, 23347 },   /* Tournament */
    {   649, 23348 },   /* Gold */
    {   650, 23349 },   /* Emblem */
    {   651, 23350 },   /* Item */
    {   653, 23351 },   /* Beginning match...  */
    {   654, 23352 },   /* RESULT */
    {   658, 23353 },   /* Final tournament results */
    {   660, 23354 },   /* Your result: %s */
    {   661, 23355 },   /* %s received as a prize. */
    {   662, 23356 },   /*    */
    {   663, 23357 },   /*   received as a prize. */
    {   664, 23358 },   /* %s cleared. */
    {   665, 23359 },   /* Did not win a prize. (Arcade-sponsored tourn */
    {   666, 23360 },   /*  Place in Official Tournaments to clear them */
    {   667, 23361 },   /* Round 1 */
    {   668, 23362 },   /* Round 2 */
    {   669, 23363 },   /* Round 3 */
    {   678, 23364 },   /* Semifinals */
    {   679, 23365 },   /* Final */
    {   680, 23366 },   /* 3rd Place Match */
    {   681, 23367 },   /* Match 1 */
    {   682, 23368 },   /* Match 2 */
    {   683, 23369 },   /* Match 3 */
    {   684, 23370 },   /* Match 4 */
    {   685, 23371 },   /* Match 5 */
    {   686, 23372 },   /* Match 6 */
    {   687, 23373 },   /* Match 7 */
    {   688, 23374 },   /* Match 8 */
    {   689, 23375 },   /* Match 9 */
    {   690, 23376 },   /* Match 10 */
    {   691, 23377 },   /* Match 11 */
    {   692, 23378 },   /* Match 12 */
    {   693, 23379 },   /* Match 13 */
    {   694, 23380 },   /* Match 14 */
    {   695, 23381 },   /* Match 15 */
    {   696, 23382 },   /* Match 16 */
    {   702, 23383 },   /* Lost in Round 1 */
    {   703, 23384 },   /* Lost in Round 2 */
    {   704, 23385 },   /* Lost in Round 3 */
    {   708, 23386 },   /* Best 4 */
    {   710, 23387 },   /* 3rd Place */
    {   711, 23388 },   /* 2nd Place */
    {   712, 23389 },   /* Champion */
    {   937, 23390 },   /* Item shop */
    {   952, 23391 },   /* Head */
    {   953, 23392 },   /* Above head */
    {   954, 23393 },   /* Hair/Hat */
    {   955, 23394 },   /* Forehead */
    {   956, 23395 },   /* Face */
    {   957, 23396 },   /* Eyes */
    {   958, 23397 },   /* Glasses */
    {   959, 23398 },   /* Ears */
    {   960, 23399 },   /* Nose/Mouth */
    {   961, 23400 },   /* Face */
    {   962, 23401 },   /* Upper Body */
    {   963, 23402 },   /* Neck */
    {   964, 23403 },   /* Inner wear */
    {   965, 23404 },   /* Outer wear */
    {   966, 23405 },   /* Chest */
    {   967, 23406 },   /* Back */
    {   968, 23407 },   /* Skin */
    {   969, 23408 },   /* Arms */
    {   970, 23409 },   /* Shoulders */
    {   971, 23410 },   /* Upper arms */
    {   972, 23411 },   /* Wrists */
    {   973, 23412 },   /* Hands */
    {   974, 23413 },   /* Lower body */
    {   975, 23414 },   /* Belt */
    {   976, 23415 },   /* Hips */
    {   977, 23416 },   /* Pants */
    {   978, 23417 },   /* Feet */
    {   979, 23418 },   /* Shins */
    {   980, 23419 },   /* Toes */
    {   981, 23420 },   /* Orb disc */
    {   994, 23421 },   /* Part to equip */
    {   995, 23422 },   /* Usable types */
    {   996, 23423 },   /* Item points */
    {   997, 23424 },   /* Fight money */
    {   998, 23425 },   /* Already purchased */
    {   999, 23426 },   /* %dG */
    {  1000, 23427 },   /* You cannot buy a new orb disc if you already */
    {  1001, 23428 },   /* Orb item completed. You cannot acquire any m */
    {  1004, 23429 },   /* Emblem settings */
    {  1005, 23430 },   /* Remove emblem */
    {  1006, 23431 },   /* Emblems collected: */
    {  1007, 23432 },   /* Game Settings */
    {  1008, 23433 },   /* Controller Settings */
    {  1010, 23434 },   /* Sound Settings */
    {  1011, 23435 },   /* Game Data */
    {  1013, 23436 },   /* Game settings */
    {  1014, 23437 },   /* ARCADE */
    {  1015, 23438 },   /* Difficulty */
    {  1021, 23439 },   /* Round count */
    {  1024, 23440 },   /* 3 */
    {  1027, 23441 },   /* Time limit */
    {  1032, 23442 },   /* Max. health bar: Player */
    {  1041, 23443 },   /* Max. health bar: CPU */
    {  1047, 23444 },   /* 260 */
    {  1050, 23445 },   /* Commentary */
    {  1051, 23446 },   /* Off */
    {  1052, 23447 },   /* On */
    {  1056, 23448 },   /* VS. */
    {  1057, 23449 },   /* Round count */
    {  1058, 23450 },   /* 1 */
    {  1059, 23451 },   /* 2 */
    {  1063, 23452 },   /* Time limit */
    {  1068, 23453 },   /* Max. health bar: 1P */
    {  1077, 23454 },   /* Max. health bar: 2P */
    {  1086, 23455 },   /* Stage select */
    {  1088, 23456 },   /* On */
    {  1089, 23457 },   /* Commentary */
    {  1092, 23458 },   /* Return to defaults */
    {  1093, 23459 },   /* End adjustment */
    {  1094, 23460 },   /* Controller settings */
    {  1096, 23461 },   /* . */
    {  1097, 23462 },   /* . */
    {  1098, 23463 },   /* . */
    {  1099, 23464 },   /* . */
    {  1100, 23465 },   /* .. */
    {  1101, 23466 },   /* .. */
    {  1103, 23467 },   /* .. */
    {  1104, 23468 },   /* .. */
    {  1117, 23469 },   /* Vibration */
    {  1121, 23470 },   /* End adjustment */
    {  1149, 23471 },   /* Screen settings */
    {  1150, 23472 },   /* Display settings */
    {  1195, 23473 },   /* X-axis */
    {  1227, 23474 },   /* Y-axis */
    {  1259, 23475 },   /* Return to defaults */
    {  1260, 23476 },   /* End adjustment */
    {  1261, 23477 },   /* Sound settings */
    {  1268, 23478 },   /* Ambient sound */
    {  1271, 23479 },   /* Volume: sound effects */
    {  1293, 23480 },   /* Volume: music */
    {  1315, 23481 },   /* Volume: commentary */
    {  1337, 23482 },   /* Return to defaults */
    {  1338, 23483 },   /* End adjustments */
    {  1339, 23484 },   /* Game Data */
    {  1340, 23485 },   /* Save */
    {  1341, 23486 },   /* Load */
    {  1342, 23487 },   /* Autosave settings */
    {  1344, 23488 },   /* Change storage device */
    {  1345, 23489 },   /* Autosave settings */
    {  1346, 23490 },   /* Autosave */
    {  1350, 23491 },   /* End adjustments */
    {  1352, 23492 },   /* Create new data */
    {  1354, 23493 },   /* Play without using data */
    {  1355, 23494 },   /* Return to the Main Menu */
    {  1356, 23495 },   /* Return to the Arcade Menu */
    {  1357, 23496 },   /* Return to the VS. Menu */
    {  1358, 23497 },   /* Return to the Dojo Menu */
    {  1363, 23498 },   /* Select the character data you want to edit.  */
    {  1368, 23499 },   /* Select the character data to use. Offline ri */
    {  1437, 23500 },   /* Do you want to load Game Data? (Any unsaved  */
    {  1480, 23501 },   /* Do you want to end the game and return to th */
    {  1484, 23502 },   /* Do you want to end the game and return to th */
    {  1500, 23503 },   /* Accessing... */
    {  1504, 23504 },   /* Are you sure you want to return to Character */
    {  1505, 23505 },   /* Are you sure you want to return to the Main  */
    {  1507, 23506 },   /* This tournament will end. Is this okay? */
    {  1508, 23507 },   /* Are you sure you want to cancel the tourname */
    {  1524, 23508 },   /* Bonus emblem unlocked. */
    {  1525, 23509 },   /* Is this emblem okay? */
    {  1526, 23510 },   /* Are you sure you want to remove emblem? */
    {  1527, 23511 },   /* Are you sure you want to delete the selected */
    {  1528, 23512 },   /* Deleted. */
    {  1529, 23513 },   /* Are you sure you want to buy  %s? */
    {  1530, 23514 },   /* Purchased. */
    {  1531, 23515 },   /* Cannot purchase--insufficient funds. */
    {  1532, 23516 },   /* Are you sure you want to leave the Item shop */
    {  1533, 23517 },   /* Are you sure you want to end customization? */
    {  1535, 23518 },   /* Are you sure you want to cancel changes and  */
    {  1536, 23519 },   /* Do you want to return to default settings? */
    {  1537, 23520 },   /* Do you want to return to default settings? */
    {  1538, 23521 },   /* Do you want to return to default settings? */
    {  1539, 23522 },   /* Do you want to erase the rankings? */
    {  1627, 23523 },   /* Teirou Kanpo.Honshin Shouten.Shouten Housui */
    {  1796, 23524 },   /* Moves from Teirou Kanpo */
    {  1798, 23525 },   /* Reversals */
    {  3073, 23526 },   /* Tobimaegeri */
    {  3329, 23527 },   /* From Hagakure-ryu You Jumonji Kamae: .+. (ho */
    {  3585, 23528 },   /* ......or... */
    {  3586, 23529 },   /* ...... */
    {  3601, 23530 },   /* ... */
    {  3603, 23531 },   /* ... */
    {  4096, 23532 },   /* Senten Kukyaku */
    {  4865, 23533 },   /* Kuretsu Tenhou */
    {  4866, 23534 },   /* Shun'en Ryouku */
    {  4867, 23535 },   /* Honshin Haisetsukou */
    {  7042, 23536 },   /* Renkan Chouten.Taisei Chouzan */
    {  7043, 23537 },   /* Renkan Chouten.Taisei Dakka */
    {  7044, 23538 },   /* Renkan Chouten.Zenkuhon */
    {  7045, 23539 },   /* Renkan Chouten.Enkou Nyudou */
    {  7046, 23540 },   /* Renkan Chouten.Rakuchi Bougetsu */
    {  7047, 23541 },   /* Renkan Chouten.Rakuten Hagetsu */
    {  7048, 23542 },   /* Shoukou Yakutou */
    {  7049, 23543 },   /* Rententai */
};
