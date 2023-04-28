<!--
UPDATE CHECKLIST
To update for next year:
- Create a new leaderboard so the competition is opt-in.
- Update all mentions of last year to the new year. (Easy to miss. Do a complete
  search/replace.)
- Un-freeze the dynamic leaderboard in the iframe at the bottom.
-->

# Advent of Code

Varje december så händer något fantastiskt.
Programmerare vaknar frivilligt klockan 6:00 på morgonen och löser mysiga små
problem i Advent of Code.
Julen handlar ju om gåvor,
så därför kommer LiTHe kod att donera 5kr för varje löst deluppgift till
skaparen av Advent of Code.
Ses där!

Så här går du med i vår leaderboard och tävling:

1. Skapa en användare på
   [adventofcode.com](https://adventofcode.com/2022/auth/login). Om du loggar in
   med ett Github-konto kan du till och med visa upp dina fina lösningar.
2. Gå med i vår leaderboard genom att skriva in koden `1879790-858765b5` på
   [leaderboard-sidan](https://adventofcode.com/2022/leaderboard/private).

Advent of Code är en global adventskalender som skapats av Eric Wastl. Problemen
är ganska enkla i början och blir svårare och svårare närmare julen. LiTHe kod
har en privat leaderboard som till skillnad från den globala leaderborden bara
innehåller LiU-studenter och andra av LiTHe kods kompisar.
(Den globala leaderboarden är i princip enbart fylld med
professionella tävlingsprogrammerare.)

Utöver vår Advent of Code-leaderboard håller LiTHe kod i en egen tävling. Vi
använder en lite annorlunda sortering än den på Advent of Codes hemsida där vi i
första hand sorterar efter stjärnor och sedan poäng. Endast LiU-studerande får
vara med och tävla om priserna men det går att trycka på en superavancerad knapp
för att även visa icke-tävlande. Om du tycker att du visst studerar på LiU men
inte är med på listan får du gärna kontakta någon i styrelsen så löser vi det.
(Du kan också kontakta oss om du inte vill vara med i tävlingen.)

Priser till vinnarna delas ut efter tävlingens slut 2022-12-25 23:59.

<!--
<ol start="0">
<li>1000 SEK</li>
<li>750 SEK </li>
<li>500 SEK </li>
<li>500 SEK </li>
<li>500 SEK </li>
<li>500 SEK </li>
<li>500 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
<li>250 SEK </li>
</ol>
-->

<div id="sponsor-container">
    <img class="sponsor" src="/static/img/mindroad_logo.png" alt="Mindroad">
</div>

<hr>

<label class="toggle-aoc" for="aoc-trigger">
    <span class="only-aoc-some">Visa alla</span>
    <span class="only-aoc-all">Visa tävlande</span>
</label>

<div id="leaderboard-container">
    <span class="only-aoc-all">
    <iframe class="only-light-theme leaderboard"
            src="https://lithekod.lysator.liu.se/leaderboard/?lightmode=true"></iframe>
    <iframe class="only-dark-theme leaderboard"
            src="https://lithekod.lysator.liu.se/leaderboard/"></iframe>
    </span><span class="only-aoc-some">
    <iframe class="only-light-theme leaderboard"
            src="https://lithekod.lysator.liu.se/leaderboard/?lightmode=true&some=true"></iframe>
    <iframe class="only-dark-theme leaderboard"
            src="https://lithekod.lysator.liu.se/leaderboard/?some=true"></iframe>
    </span>
</div>
