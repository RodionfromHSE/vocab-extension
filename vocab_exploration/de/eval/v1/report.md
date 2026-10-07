# German vocab generation: model bake-off

25 words (stratified: nouns, verbs, adjectives/adverbs, phrases), none of them few-shot examples. Grammar is checked against Cambridge GLOBAL German–English, only on the fields Cambridge lists. Semantic scores come from blind cross-model judges (each output is rated by the two *other* models; judging cost $0.77).

## Summary

| model | valid | retries | grammar vs Cambridge | sense = Cambridge #1 | most common sense | word_en ok | definitions ok | translations ok | judge: no grammar errors | naturalness (1–5) | latency | $/word | $ for full list |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **deepseek-v4p1-flash** | 25/25 | 1 | 100% (68 checks) | 76% | 92% | 96% | 96% | 94% | 100% | 4.76 | 9.3s | $0.0018 | $5.21 |
| **glm-5p3** | 25/25 | 0 | 100% (68 checks) | 68% | 94% | 96% | 60% | 92% | 100% | 4.78 | 4.3s | $0.0018 | $5.36 |
| **kimi-k3** | 25/25 | 0 | 100% (68 checks) | 62% | 94% | 94% | 78% | 98% | 92% | 4.82 | 9.5s | $0.0104 | $30.93 |

## Per word

### 1. Handel (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. — · gen. Handels | trade | das Kaufen und Verkaufen von Waren | Handel treiben — *to trade*<br>der illegale Handel mit Rauschgift | |
| deepseek-v4p1-flash | der · pl. — · gen. des Handels | trade, commerce | das Kaufen und Verkaufen von Waren | Der Handel mit Kaffee ist sehr wichtig. — *The coffee trade is very important.*<br>Sie arbeitet im Handel. — *She works in commerce.* |  |
| glm-5p3 | der · pl. — · gen. des Handels | trade, commerce | das Kaufen und Verkaufen von Waren, besonders zwischen Ländern oder Firmen | Deutschland betreibt Handel mit vielen Ländern. — *Germany trades with many countries.*<br>Der internationale Handel wächst jedes Jahr. — *International trade grows every year.* |  |
| kimi-k3 | der · pl. — · gen. des Handels | trade, commerce | der Kauf und Verkauf von Waren zwischen Personen, Firmen oder Ländern | Der Handel zwischen den beiden Ländern wächst. — *Trade between the two countries is growing.*<br>Er arbeitet im internationalen Handel. — *He works in international trade.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): "Sie arbeitet im Handel" is better rendered as "She works in retail/the retail trade" than "in commerce".
- **deepseek-v4p1-flash** (judge glm-5p3): Solid entry; 'Der Handel mit Kaffee ist sehr wichtig' is slightly textbook-like but acceptable.

### 2. Trauung (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Trauungen · gen. Trauung | wedding (ceremony) | Hochzeitszeremonie | eine standesamtliche / kirchliche Trauung — *a civil/church wedding*<br>die Trauung vollziehen | |
| deepseek-v4p1-flash | die · pl. die Trauungen · gen. der Trauung | wedding ceremony, marriage ceremony | die kirchliche oder standesamtliche Zeremonie, bei der zwei Menschen heiraten | Die Trauung findet am Samstag im Standesamt statt. — *The wedding ceremony is at the registry office on Saturday.*<br>Nach der Trauung feiern wir mit der Familie. — *After the ceremony we're celebrating with the family.* |  |
| glm-5p3 | die · pl. die Trauungen · gen. der Trauung | wedding ceremony | die feierliche Handlung, bei der zwei Menschen rechtlich ein Ehepaar werden | Die Trauung findet im Rathaus statt. — *The wedding ceremony is taking place at the registry office.*<br>Nach der Trauung gab es ein großes Essen. — *There was a big meal after the ceremony.* |  |
| kimi-k3 | die · pl. die Trauungen · gen. der Trauung | wedding ceremony | feierliche Zeremonie, bei der zwei Menschen heiraten | Die Trauung findet am Samstag in der Kirche statt. — *The wedding ceremony takes place on Saturday in church.*<br>Nach der Trauung gab es ein großes Fest. — *After the ceremony there was a big celebration.* |  |

- **glm-5p3** (judge kimi-k3): Definition is inaccurate: a church Trauung does not make a couple legally married in Germany, so 'rechtlich ein Ehepaar werden' is wrong.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition wrongly restricts Trauung to a legal marriage ceremony; it can also be a church ceremony.

### 3. stoßen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | stößt · stieß · gestoßen · haben | to push, to shove | jdm / etw. einen Stoß versetzen | jdn ins Wasser stoßen — *to push sb into the water*<br>Er stieß aus Versehen das Glas vom Tisch. | |
| deepseek-v4p1-flash | stößt · stieß · hat gestoßen | to push, to shove | jemanden oder etwas mit einem kräftigen Druck bewegen | Er hat mich aus Versehen gestoßen. — *He accidentally pushed me.*<br>Stoß den Tisch mal ein Stück nach links. — *Push the table a bit to the left.* |  |
| glm-5p3 | stößt · stieß · hat gestoßen | to push, to shove | jemanden oder etwas mit Kraft kurz von sich weg bewegen | Er hat sie versehentlich mit dem Ellbogen gestoßen. — *He accidentally nudged her with his elbow.*<br>Stoß die Tür doch mal zu, es zieht. — *Give the door a push, will you — there's a draft.* |  |
| kimi-k3 | stößt · stieß · hat gestoßen | to push, to bump | mit Kraft gegen jemanden oder etwas drücken oder schlagen | Hör auf, mich zu stoßen! — *Stop pushing me!*<br>Ich habe mir den Kopf an der Tür gestoßen. — *I bumped my head on the door.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Moving a table a short distance would normally be 'schieben' or 'rücken', not 'stoßen', which implies a short sharp shove.
- **deepseek-v4p1-flash** (judge glm-5p3): "Stoß den Tisch mal ein Stück nach links" is unidiomatic — a native speaker would say "Schieb den Tisch mal ein Stück nach links".
- **glm-5p3** (judge kimi-k3): Both examples are good; 'die Tür zustoßen' is fine but 'zudrücken' would be the more typical everyday choice.
- **glm-5p3** (judge deepseek-v4p1-flash): Second example uses separable 'zustoßen' and its translation omits 'zu' (shut).
- **kimi-k3** (judge glm-5p3): "to bump" and the definition "schlagen" drift into a different sense (sich stoßen/anstoßen), mixing two meanings in one entry.; reflexive is false, but the second example uses the reflexive construction "sich (Dativ) den Kopf stoßen"
- **kimi-k3** (judge deepseek-v4p1-flash): Definition uses 'schlagen'/'hit', which is too strong for 'stoßen'.

### 4. lesen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | liest · las · gelesen · haben | to read | Geschriebenes ansehen und den Sinn entnehmen | Liest du gerne / viel? — *Do you like/do a lot of reading?*<br>Die winzige Schrift war kaum zu lesen. | |
| deepseek-v4p1-flash | liest · las · hat gelesen | to read | geschriebene Wörter oder Texte mit den Augen aufnehmen und verstehen | Ich lese abends gern ein Buch. — *I like reading a book in the evening.*<br>Hast du den Artikel schon gelesen? — *Have you read the article yet?* |  |
| glm-5p3 | liest · las · hat gelesen | to read | geschriebene oder gedruckte Texte verstehen | Ich lese jeden Abend ein paar Seiten. — *I read a few pages every evening.*<br>Hast du dieses Buch schon gelesen? — *Have you read this book yet?* |  |
| kimi-k3 | liest · las · hat gelesen | to read | geschriebenen Text anschauen und verstehen | Ich lese gerade ein spannendes Buch. — *I'm reading an exciting book at the moment.*<br>Hast du die Zeitung schon gelesen? — *Have you read the newspaper yet?* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Definition is accurate but slightly wordy ('mit den Augen aufnehmen') for A1–B1 learners.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition_de describes understanding texts rather than the act of reading.
- **kimi-k3** (judge glm-5p3): 'anschauen' in the German definition is slightly colloquial/regional; 'ansehen' would be more neutral, and the articleless singular 'geschriebenen Text' is a bit stiff.

### 5. dumm (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adjective | stupid, dumb | mit wenig Intelligenz | Sie stellt sich gern dumm, damit man ihr keine Verantwortung überträgt. — *She likes to act dumb so nobody gives her any responsibility.*<br>sich wie ein dummer kleiner Junge benehmen | |
| deepseek-v4p1-flash | dümmer · am dümmsten | stupid, silly | nicht klug und ohne guten Verstand | Das war wirklich eine dumme Idee. — *That was a really stupid idea.*<br>Sei nicht dumm, nimm die Hilfe an. — *Don't be silly, take the help.* |  |
| glm-5p3 | dümmer · am dümmsten | stupid, silly | nicht klug; ohne Verstand oder ohne gutes Urteilsvermögen | Das war eine wirklich dumme Frage. — *That was a really silly question.*<br>Wie konnte ich nur so dumm sein? — *How could I be so stupid?* |  |
| kimi-k3 | dümmer · am dümmsten | stupid, dumb | nicht intelligent; ohne Verstand | Das war wirklich dumm von mir. — *That was really stupid of me.*<br>Stell dich nicht so dumm an! — *Don't be so stupid!* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): "take the help" is unidiomatic English; better "accept the help" or "take the offer of help".
- **deepseek-v4p1-flash** (judge glm-5p3): "Sei nicht dumm" sounds slightly stilted without "so" ("Sei nicht so dumm"), and "take the help" is unidiomatic English; "accept the help" would be better.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition uses advanced 'Urteilsvermögen' for A1–B1.
- **kimi-k3** (judge glm-5p3): "Stell dich nicht so dumm an!" is natural German but means "Stop acting so dumb/foolish", so the translation "Don't be so stupid!" misses the sich-dumm-anstellen nuance and drifts toward a different sense.

### 6. Nummer (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Nummern · gen. Nummer | number | Zahl, die den Platz in einer Reihenfolge angibt | der Teilnehmer mit der Nummer 25 — *competitor number 25* | |
| deepseek-v4p1-flash | die · pl. die Nummern · gen. der Nummer | number | eine Zahl oder Ziffernfolge, mit der man etwas bezeichnet oder erkennt | Kannst du mir deine Nummer geben? — *Can you give me your number?*<br>Die Nummer steht auf dem Ticket. — *The number is on the ticket.* |  |
| glm-5p3 | die · pl. die Nummern · gen. der Nummer | number | eine Zahl oder eine Folge von Zahlen, die etwas Bestimmtes kennzeichnet | Wie ist deine Handynummer? — *What's your mobile number?*<br>Ich habe die falsche Nummer gewählt. — *I dialled the wrong number.* |  |
| kimi-k3 | die · pl. die Nummern · gen. der Nummer | number | eine Ziffer oder Zahl, mit der etwas bezeichnet wird | Kannst du mir deine Nummer geben? — *Can you give me your number?*<br>Ich habe die falsche Nummer gewählt. — *I dialled the wrong number.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Guter Eintrag; der Sinn (identifizierende Nummer, v. a. Telefonnummer) ist alltagstauglicher als Cambridges erste Bedeutung (Reihenfolge-/Platznummer), deckt sich mit dieser aber nicht exakt.
- **glm-5p3** (judge kimi-k3): Both examples are phone-number contexts; one non-telephone example (e.g. Hausnummer, Ticket) would show the meaning's range better.
- **kimi-k3** (judge glm-5p3): Die deutsche Definition mit „Ziffer“ (einzelne Ziffer) ist ungenau, und „a figure or set of figures“ klingt im Englischen unnatürlich; die Beispiele sind dagegen vorbildlich.
- **kimi-k3** (judge deepseek-v4p1-flash): Definition wrongly includes 'Ziffer'; a Nummer is not a single digit.

### 7. Ausländer (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Ausländer · gen. Ausländers | foreigner |  | eine Schule mit hohem Ausländeranteil — *a school with a large number of foreign immigrants* | |
| deepseek-v4p1-flash | der · pl. die Ausländer · gen. des Ausländers | foreigner | eine Person, die nicht die Staatsangehörigkeit des Landes hat, in dem sie lebt | Mein Nachbar ist Ausländer und kommt aus Italien. — *My neighbour is a foreigner and comes from Italy.*<br>In dieser Stadt leben viele Ausländer. — *Many foreigners live in this city.* |  |
| glm-5p3 | der · pl. die Ausländer · gen. des Ausländers | foreigner | eine Person, die nicht die Staatsangehörigkeit des Landes hat, in dem sie lebt | Viele Ausländer leben und arbeiten in Deutschland. — *Many foreigners live and work in Germany.*<br>Als Ausländer braucht man hier ein Visum. — *As a foreigner, you need a visa here.* |  |
| kimi-k3 | der · pl. die Ausländer · gen. des Ausländers | foreigner | eine Person, die aus einem anderen Land kommt oder eine andere Staatsangehörigkeit hat | Als Ausländer braucht man hier ein Visum. — *As a foreigner, you need a visa here.*<br>In dieser Stadt leben viele Ausländer. — *A lot of foreigners live in this city.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Definition is slightly narrow, as an Ausländer need not live in the country in question.
- **glm-5p3** (judge kimi-k3): definition_en ("comes from or belongs to") does not match definition_de, which is based on nationality.
- **glm-5p3** (judge deepseek-v4p1-flash): English definition 'belongs to a different country' is awkward; better 'is a citizen of another country'.

### 8. bloß (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adjective | bare | nicht mit etw. bedeckt | sich auf die bloße Erde setzen — *to sit on the bare ground*<br>Frierst du nicht mit bloßen Armen? | |
| deepseek-v4p1-flash | adverb | only, just | nur, lediglich; nicht mehr als | Ich habe bloß zehn Euro dabei. — *I only have ten euros on me.*<br>Das war bloß ein Scherz. — *That was just a joke.* |  |
| glm-5p3 | adverb | just, simply | drückt aus, dass etwas nur das Genannte ist und nichts weiter | Ich habe das bloß so gesagt. — *I just said that off the top of my head.*<br>Das ist bloß ein Missverständnis. — *It's just a misunderstanding.* |  |
| kimi-k3 | adverb | only, just | nur, nicht mehr als | Ich habe bloß noch fünf Euro dabei. — *I've only got five euros on me.*<br>Komm bloß nicht zu spät! — *Whatever you do, don't be late!* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Correctly chooses the far more common adverb sense ('only/just') rather than Cambridge's adjective sense 'bare'.
- **deepseek-v4p1-flash** (judge glm-5p3): Clean, consistent entry for the most common adverbial sense; both examples are perfectly natural.
- **glm-5p3** (judge kimi-k3): 'Ich habe das bloß so gesagt' means 'I just said it (without meaning anything by it)', not 'off the top of my head'.
- **glm-5p3** (judge deepseek-v4p1-flash): First example translation 'off the top of my head' is not faithful to 'bloß so'.
- **kimi-k3** (judge glm-5p3): Second example ('Komm bloß nicht zu spät!') belongs to the separate emphatic/imperative sense of 'bloß', not the defined 'only' sense, so the entry mixes two senses.
- **kimi-k3** (judge deepseek-v4p1-flash): Second example uses 'bloß' as a modal particle, not the defined adverb sense 'only/just'.

### 9. traditionell (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adjective | traditional |  | ein traditioneller Tanz — *a traditional dance* | |
| deepseek-v4p1-flash | traditioneller · am traditionellsten | traditional | so, wie es seit langer Zeit üblich ist | Das ist ein traditionelles Gericht aus Bayern. — *This is a traditional dish from Bavaria.*<br>Sie feiern das Fest ganz traditionell. — *They celebrate the festival in a very traditional way.* |  |
| glm-5p3 | traditioneller · am traditionellsten | traditional | so, wie es seit langem üblich ist und von Generation zu Generation weitergegeben wird | Wir feiern Weihnachten ganz traditionell. — *We celebrate Christmas in a very traditional way.*<br>Das ist ein traditionelles Rezept von meiner Oma. — *That's a traditional recipe from my grandma.* |  |
| kimi-k3 | traditioneller · am traditionellsten | traditional | nach alter Art und Weise, wie es seit langer Zeit üblich ist | Wir feiern Weihnachten immer ganz traditionell. — *We always celebrate Christmas in the traditional way.*<br>Das ist ein traditionelles Gericht aus Bayern. — *That's a traditional dish from Bavaria.* |  |

- **kimi-k3** (judge glm-5p3): definition_de is slightly clunky ('nach alter Art und Weise, wie es seit langer Zeit üblich ist') and could be simplified.
- **kimi-k3** (judge deepseek-v4p1-flash): Die deutsche Definition enthält die unidiomatische Formulierung „nach alter Art und Weise“.

### 10. Rabatt (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Rabatte · gen. Rabattes | discount | Preisnachlass | Frühbucherrabatt<br>Mengenrabatt | |
| deepseek-v4p1-flash | der · pl. die Rabatte · gen. des Rabatts | discount | ein niedrigerer Preis, den man beim Kauf bekommt | Auf diese Schuhe gibt es zehn Prozent Rabatt. — *There's a ten percent discount on these shoes.*<br>Kannst du mir einen Rabatt geben? — *Can you give me a discount?* |  |
| glm-5p3 | der · pl. die Rabatte · gen. des Rabatts | discount, reduction | ein niedrigerer Preis, den man beim Kaufen von etwas bezahlt | Auf diese Jacke gibt es 20 Prozent Rabatt. — *There's a 20% discount on this jacket.*<br>Bekommen Studenten hier auch Rabatt? — *Do students get a discount here too?* |  |
| kimi-k3 | der · pl. die Rabatte · gen. des Rabatts | discount | ein Betrag, um den ein Preis reduziert wird | Auf diese Jacke gibt es 20 Prozent Rabatt. — *There's a 20 percent discount on this jacket.*<br>Studenten bekommen hier oft Rabatt. — *Students often get a discount here.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): The definition describes the reduced price you pay, not the discount (price reduction) itself; 'einen niedrigeren Preis bekommen' is also slightly off idiomatically.
- **deepseek-v4p1-flash** (judge glm-5p3): Definition describes the reduced price rather than the reduction itself, but this is a minor imprecision acceptable for A1–B1 learners.
- **glm-5p3** (judge kimi-k3): The German definition defines the reduced price paid rather than the reduction itself and contradicts the (correct) English definition; also '20%' should be '20 %' in German.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition_de is imprecise: Rabatt is the reduction, not the lower price.

### 11. voraus (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adverb | ahead | besser, schneller usw. als andere / anderes | Andere Länder sind uns in Sachen Bildungspolitik weit voraus. — *Other countries are way ahead of us in terms of educational policy.*<br>seiner Zeit voraus sein | |
| deepseek-v4p1-flash | adverb | ahead, in front | weiter vorn, vor jemandem oder etwas | Geh schon mal voraus, ich komme gleich nach. — *Go on ahead, I'll catch up.*<br>Das Auto vor uns ist schon weit voraus. — *The car in front of us is already far ahead.* |  |
| glm-5p3 | adverb | ahead, in advance | vor jemandem oder etwas; in eine Richtung, die vor einem liegt | Geh du doch schon mal voraus, ich komme später. — *Go on ahead, I'll come later.*<br>Vielen Dank im Voraus für deine Hilfe. — *Many thanks in advance for your help.* |  |
| kimi-k3 | adverb | ahead, in advance | vor anderen oder vor dem eigentlichen Zeitpunkt | Geh schon mal voraus, ich komme gleich nach. — *Go on ahead, I'll follow in a minute.*<br>Danke im Voraus für deine Hilfe! — *Thanks in advance for your help!* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Second example is slightly redundant ('vor uns ... voraus'); the very common phrase 'im Voraus' is missing.
- **deepseek-v4p1-flash** (judge glm-5p3): Misses the very common fixed phrase 'im Voraus' (= in advance), 'in front' is not a natural equivalent for 'voraus', and 'Das Auto vor uns ist schon weit voraus' is grammatical but stilted.
- **glm-5p3** (judge kimi-k3): definition_de covers only the spatial sense while definition_en adds a temporal sense ('before something happens') that the German definition lacks.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition_de only covers spatial 'ahead' and does not explain the temporal 'im Voraus' example.
- **kimi-k3** (judge glm-5p3): Examples are perfectly natural and cover the two most common learner uses ('Geh schon mal voraus', 'im Voraus'), but definition_en 'before the actual time' is a literal, unidiomatic rendering (should be 'in advance').
- **kimi-k3** (judge deepseek-v4p1-flash): Definition mixes spatial and temporal senses and 'vor anderen' is imprecise.

### 12. Kuh (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Kühe · gen. Kuh | cow | weibliches Rind | Kühe geben Milch. — *Cows produce milk.*<br>die Kühe melken | |
| deepseek-v4p1-flash | die · pl. die Kühe · gen. der Kuh | cow | großes weibliches Rind, das Milch gibt | Die Kühe stehen auf der Weide. — *The cows are in the pasture.*<br>Unsere Kuh gibt jeden Tag frische Milch. — *Our cow gives fresh milk every day.* |  |
| glm-5p3 | die · pl. die Kühe · gen. der Kuh | cow | ein großes Nutztier, das Milch gibt und auf Wiesen grasst | Die Kühe grasen auf der Wiese. — *The cows are grazing in the field.*<br>Auf dem Bauernhof gibt es zwanzig Kühe. — *There are twenty cows on the farm.* |  |
| kimi-k3 | die · pl. die Kühe · gen. der Kuh | cow | ein großes Nutztier, das Milch gibt und auf dem Bauernhof lebt | Auf der Wiese stehen viele Kühe. — *There are lots of cows in the meadow.*<br>Die Kuh gibt jeden Tag frische Milch. — *The cow gives fresh milk every day.* |  |

- **glm-5p3** (judge kimi-k3): English definition is slightly wordy/awkward ("kept for milk that eats grass in fields") but accurate.
- **glm-5p3** (judge deepseek-v4p1-flash): definition_de uses incorrect verb form 'grasst' (should be 'grast').
- **kimi-k3** (judge glm-5p3): Definition omits that a Kuh is female (weibliches Rind), unlike Cambridge's first sense, but is otherwise accurate and learner-friendly.

### 13. vertreten (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to stand in / deputize for | jds Aufgaben für eine bestimmte Zeit übernehmen | Er hat sich auf der Sitzung von seiner Assistentin vertreten lassen. — *He had his assistant stand in for him at the meeting.* | |
| deepseek-v4p1-flash | vertritt · vertrat · hat vertreten | to represent, to stand in for | für jemanden handeln oder sprechen, wenn er selbst nicht da ist | Kannst du mich morgen im Büro vertreten? — *Can you stand in for me at the office tomorrow?*<br>Der Anwalt hat die Firma vor Gericht vertreten. — *The lawyer represented the company in court.* |  |
| glm-5p3 | vertritt · vertrat · hat vertreten | to represent | die Interessen oder Meinungen einer anderen Person vertreten und für sie sprechen | Mein Anwalt vertritt mich vor Gericht. — *My lawyer is representing me in court.*<br>Sie hat ihren Kollegen in der Sitzung vertreten. — *She stood in for her colleague at the meeting.* |  |
| kimi-k3 | vertritt · vertrat · hat vertreten | to represent | im Namen einer Person oder Gruppe sprechen oder handeln | Wer vertritt dich bei dem Termin? — *Who's representing you at the meeting?*<br>Sie hat unsere Firma auf der Messe vertreten. — *She represented our company at the trade fair.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Definition describes the 'stand in' sense, but the second example ('vor Gericht vertreten') illustrates the 'represent' sense, so definition and examples don't fully align.
- **deepseek-v4p1-flash** (judge glm-5p3): Matches Cambridge's 'stand in for' sense, but word_en conflates two senses and the lawyer/court example actually illustrates 'represent', not 'stand in for'.
- **glm-5p3** (judge kimi-k3): German definition is circular (uses 'vertreten' to define 'vertreten'), and the second example shows the 'stand in' sense, not the defined 'represent' sense.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition is circular because it uses 'vertreten' to define itself.
- **kimi-k3** (judge glm-5p3): Solid entry for the most common sense ('represent'), but 'bei dem Termin' should be the more natural 'beim Termin'.
- **kimi-k3** (judge deepseek-v4p1-flash): Chosen sense is broader 'represent' rather than Cambridge's temporary stand-in.

### 14. zerstören (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to destroy | etw. so stark beschädigen, dass man es nicht mehr benutzen kann | Dresden wurde im Krieg fast völlig zerstört. — *Dresden was almost completely destroyed in the war.* | |
| deepseek-v4p1-flash | zerstört · zerstörte · hat zerstört | to destroy | etwas so kaputt machen, dass es nicht mehr zu benutzen ist | Der Sturm hat viele Häuser zerstört. — *The storm destroyed many houses.*<br>Das Feuer hat den ganzen Wald zerstört. — *The fire destroyed the whole forest.* |  |
| glm-5p3 | zerstört · zerstörte · hat zerstört | to destroy | etwas so beschädigen, dass es nicht mehr existiert oder nicht mehr benutzt werden kann | Der Sturm hat viele Häuser zerstört. — *The storm destroyed many houses.*<br>Der Krieg hat die ganze Stadt zerstört. — *The war destroyed the whole city.* |  |
| kimi-k3 | zerstört · zerstörte · hat zerstört | to destroy | etwas so beschädigen, dass es kaputt ist oder nicht mehr existiert | Das Feuer hat das ganze Haus zerstört. — *The fire destroyed the whole house.*<br>Der Sturm hat viele Bäume zerstört. — *The storm destroyed many trees.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Definition only covers "no longer usable" and misses the frequent sense of complete annihilation (e.g. a destroyed city or forest).
- **deepseek-v4p1-flash** (judge glm-5p3): Die Definition mit 'kaputt machen' ist etwas umgangssprachlich und eng (nicht mehr benutzbar), während 'zerstören' oft völlige Vernichtung bedeutet – für A1–B1 aber noch akzeptabel.
- **kimi-k3** (judge glm-5p3): Der Beispielsatz 'Der Sturm hat viele Bäume zerstört' ist grammatisch korrekt, aber leicht unidiomatisch – ein Muttersprachler würde eher 'viele Bäume umgeworfen' sagen.
- **kimi-k3** (judge deepseek-v4p1-flash): Die Kollokation 'Bäume zerstören' ist weniger idiomatisch als 'Bäume umwerfen/entwurzeln'.

### 15. Lebenslauf (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Lebensläufe · gen. Lebenslaufes | résumé | schriftliche Darstellung des eigenen, bisherigen Lebensweges für eine Bewerbung | ein tabellarischer Lebenslauf — *a résumé in tabular form* | |
| deepseek-v4p1-flash | der · pl. die Lebensläufe · gen. des Lebenslaufs | CV, résumé | schriftliche Übersicht über Ausbildung, Berufserfahrung und Kenntnisse | Ich habe meinen Lebenslauf für die Bewerbung geschrieben. — *I wrote my CV for the job application.*<br>Schick deinen Lebenslauf bitte per E-Mail. — *Please send your CV by email.* |  |
| glm-5p3 | der · pl. die Lebensläufe · gen. des Lebenslaufs | CV, résumé | eine schriftliche Übersicht über den beruflichen Werdegang einer Person | Für die Bewerbung brauchst du einen Lebenslauf. — *You need a CV for the application.*<br>Ich habe meinen Lebenslauf aktualisiert. — *I've updated my CV.* |  |
| kimi-k3 | der · pl. die Lebensläufe · gen. des Lebenslaufs | CV, résumé | ein Dokument mit den wichtigsten Informationen über Ausbildung und Berufserfahrung einer Person | Schick mir bitte deinen Lebenslauf als PDF. — *Please send me your CV as a PDF.*<br>Im Lebenslauf dürfen keine Lücken sein. — *There shouldn't be any gaps in your CV.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): "einen Lebenslauf schreiben" is understandable but less idiomatic than "erstellen" or "aktualisieren".
- **deepseek-v4p1-flash** (judge glm-5p3): First example is grammatical but slightly textbook-like; a native speaker would more likely say 'Ich habe meinen Lebenslauf für die Bewerbung neu geschrieben/aktualisiert'.

### 16. Hauptbahnhof (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Hauptbahnhöfe · gen. Hauptbahnhofes | main/central station | größter Bahnhof einer Stadt |  | |
| deepseek-v4p1-flash | der · pl. die Hauptbahnhöfe · gen. des Hauptbahnhofs | main station, central station | der größte Bahnhof einer Stadt, an dem viele Züge halten | Wir treffen uns am Hauptbahnhof. — *We'll meet at the main station.*<br>Der Zug kommt um acht am Hauptbahnhof an. — *The train arrives at the main station at eight.* |  |
| glm-5p3 | der · pl. die Hauptbahnhöfe · gen. des Hauptbahnhofs | main station, central station | der wichtigste Bahnhof einer Stadt | Ich warte auf dich am Hauptbahnhof. — *I'll wait for you at the main station.*<br>Wie komme ich zum Hauptbahnhof? — *How do I get to the main station?* |  |
| kimi-k3 | der · pl. die Hauptbahnhöfe · gen. des Hauptbahnhofs | main station, central station | der größte und wichtigste Bahnhof einer Stadt | Wir treffen uns um drei am Hauptbahnhof. — *We're meeting at the main station at three.*<br>Wie komme ich am besten zum Hauptbahnhof? — *What's the best way to get to the main station?* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Definition is slightly longer than needed but still accurate, simple and learner-friendly.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition uses 'wichtigste' rather than Cambridge's 'größte', but it is the common everyday sense.

### 17. wiegen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | wog · gewogen · haben | to weigh | das Gewicht von jdm / etw. bestimmen | Das Obst wird an der Kasse gewogen. — *The fruit is weighed at the checkout.*<br>Sie wiegt sich jeden Morgen. | |
| deepseek-v4p1-flash | wiegt · wog · hat gewogen | to weigh | das Gewicht von jemandem oder etwas messen oder ein bestimmtes Gewicht haben | Wie viel wiegt dein Koffer? — *How much does your suitcase weigh?*<br>Ich habe das Paket schon gewogen. — *I've already weighed the package.* |  |
| glm-5p3 | wiegt · wog · hat gewogen | to weigh | mit einer Waage feststellen, wie schwer etwas oder jemand ist | Der Verkäufer hat das Fleisch gewogen. — *The assistant weighed the meat.*<br>Wie viel wiegst du denn jetzt? — *How much do you weigh now?* |  |
| kimi-k3 | wiegt · wog · hat gewogen | to weigh | ein bestimmtes Gewicht haben oder das Gewicht von etwas messen | Wie viel wiegst du denn? — *How much do you weigh?*<br>Der Koffer hat fast 20 Kilo gewogen. — *The suitcase weighed almost 20 kilos.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Natürliche Beispiele, aber die Definition vermischt den transitiven und den intransitiven Sinn in einem einzigen Eintrag, was für ein Lernerwörterbuch unsauber ist.
- **glm-5p3** (judge kimi-k3): The second example ("Wie viel wiegst du?") illustrates the intransitive sense 'to have a weight', which the transitive-only definition does not cover.
- **glm-5p3** (judge deepseek-v4p1-flash): Matches Cambridge's transitive sense, but the most common everyday sense is intransitive 'have weight'; second example uses that sense.
- **kimi-k3** (judge glm-5p3): Definition vermengt zwei verschiedene Senses ('ein Gewicht haben' vs. 'Gewicht messen'), und die Beispiele illustrieren nur den intransitiven Sinn, nicht Cambridges transitiven Erstsinns.
- **kimi-k3** (judge deepseek-v4p1-flash): Covers the most common intransitive sense, but definition also adds transitive 'measure weight'.

### 18. Ausbildung (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Ausbildungen · gen. Ausbildung | apprenticeship | eine Zeit, in der man einen Beruf in der Praxis erlernt | eine Ausbildung zum Elektriker machen — *to do an apprenticeship as an electrician*<br>noch in der Ausbildung sein | |
| deepseek-v4p1-flash | die · pl. die Ausbildungen · gen. der Ausbildung | training, apprenticeship | das Lernen eines Berufs, meist in einem Betrieb und in der Berufsschule | Meine Schwester macht eine Ausbildung als Köchin. — *My sister is doing an apprenticeship as a cook.*<br>Nach der Ausbildung möchte ich studieren. — *After my training, I want to go to university.* |  |
| glm-5p3 | die · pl. die Ausbildungen · gen. der Ausbildung | training, apprenticeship | das Lernen eines Berufs in einem Betrieb oder einer Schule | Sie macht eine Ausbildung zur Krankenschwester. — *She's training to be a nurse.*<br>Nach der Schule beginnt er seine Ausbildung. — *After school he's starting his apprenticeship.* |  |
| kimi-k3 | die · pl. die Ausbildungen · gen. der Ausbildung | training, vocational training | das Lernen eines Berufs in einer Firma oder Schule | Meine Tochter macht eine Ausbildung zur Krankenschwester. — *My daughter is training to be a nurse.*<br>Nach der Ausbildung will er im Ausland arbeiten. — *After his training, he wants to work abroad.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Sehr solide; 'eine Ausbildung als Köchin' ist korrekt, wobei 'zur Köchin' häufiger wäre.
- **glm-5p3** (judge kimi-k3): Slight mismatch: German definition says 'das Lernen' (process) while English says 'the period'.
- **glm-5p3** (judge deepseek-v4p1-flash): definition_en 'learning a job' is not idiomatic.
- **kimi-k3** (judge glm-5p3): word_en lässt 'apprenticeship' als wichtigste Entsprechung für das duale System vermissen.

### 19. Augenblick (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Augenblicke · gen. Augenblickes | moment | sehr kurzer Zeitraum | Einen Augenblick, bitte! — *Just a moment, please.*<br>das Flugzeug im letzten Augenblick erreichen | |
| deepseek-v4p1-flash | der · pl. die Augenblicke · gen. des Augenblicks | moment, instant | eine sehr kurze Zeitspanne | Einen Augenblick, bitte! — *One moment, please!*<br>Im nächsten Augenblick war er weg. — *The next moment he was gone.* |  |
| glm-5p3 | der · pl. die Augenblicke · gen. des Augenblicks | moment | eine sehr kurze Zeitspanne | Einen Augenblick, ich bin gleich fertig. — *Just a moment, I'll be done in a second.*<br>Im nächsten Augenblick regnete es. — *The next moment it started raining.* |  |
| kimi-k3 | der · pl. die Augenblicke · gen. des Augenblicks | moment | eine sehr kurze Zeit | Einen Augenblick, ich komme gleich! — *Just a moment, I'll be right there!*<br>Im Augenblick habe ich leider keine Zeit. — *I'm afraid I don't have time at the moment.* |  |

- **glm-5p3** (judge deepseek-v4p1-flash): Second example is unidiomatic and the English translation adds 'started' not present in the German.
- **kimi-k3** (judge glm-5p3): "Im Augenblick" in the sense of 'at the moment' is dated; a native speaker would say "Im Moment" or "Gerade".

### 20. setzen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to sit (down) | eine sitzende Stellung einnehmen | sich aufs Pferd setzen — *to get into the saddle*<br>Sie setzte sich zu mir / neben mich. | |
| deepseek-v4p1-flash | setzt sich · setzte sich · hat sich gesetzt refl. | to sit down | sich auf einen Platz niederlassen, sodass man sitzt | Setz dich doch zu mir! — *Come sit with me!*<br>Wir haben uns auf die Bank gesetzt. — *We sat down on the bench.* |  |
| glm-5p3 | setzt · setzte · hat gesetzt | to put, to place | etwas an eine bestimmte Stelle legen oder stellen | Setz die Blumen bitte auf den Tisch. — *Please put the flowers on the table.*<br>Er hat den Koffer neben die Tür gesetzt. — *He put the suitcase next to the door.* |  |
| kimi-k3 | setzt · setzte · hat gesetzt | to put, to set | etwas an eine bestimmte Stelle legen oder stellen | Setz das Buch einfach auf den Tisch. — *Just put the book on the table.*<br>Sie hat das Kind auf den Stuhl gesetzt. — *She sat the child on the chair.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Matches Cambridge's reflexive 'sit down' sense exactly and is very common, but the transitive 'put/place' sense is the single most common meaning of setzen overall.
- **deepseek-v4p1-flash** (judge glm-5p3): Correct and natural reflexive entry matching Cambridge's first sense, but the transitive 'put' sense is more frequent in everyday use and should come first for A1–B1 learners.
- **glm-5p3** (judge kimi-k3): Same transitive 'put/place' sense as A, not Cambridge's reflexive first sense; essentially a duplicate of A with equally natural examples.
- **glm-5p3** (judge deepseek-v4p1-flash): Examples use 'setzen' with objects where 'stellen/legen' is more idiomatic; sense is not the most common.
- **kimi-k3** (judge glm-5p3): Solid entry for the transitive 'put' sense, which is the most useful everyday meaning for learners, though it differs from Cambridge's first (reflexive) sense.
- **kimi-k3** (judge deepseek-v4p1-flash): Transitive 'setzen' is not the most common sense, and 'Setz das Buch...' is unidiomatic; use 'legen/stellen'.

### 21. vermissen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to miss | Sehnsucht empfinden, weil jd / etw. fehlt | Es ist schön, dass du wieder da bist; ich habe dich so vermisst! — *I’m glad you’re back. I really missed you!* | |
| deepseek-v4p1-flash | vermisst · vermisste · hat vermisst | to miss | jemanden oder etwas nicht bei sich haben und sich wünschen, dass er oder es da ist | Ich vermisse meine Familie sehr. — *I really miss my family.*<br>Hast du deine Freunde in Berlin vermisst? — *Did you miss your friends in Berlin?* |  |
| glm-5p3 | vermisst · vermisste · hat vermisst | to miss | traurig sein, weil jemand oder etwas nicht mehr da ist | Ich vermisse meine Familie sehr. — *I really miss my family.*<br>Nach dem Umzug habe ich meine Freunde vermisst. — *After moving, I missed my friends.* |  |
| kimi-k3 | vermisst · vermisste · hat vermisst | to miss | traurig sein, weil jemand oder etwas nicht da ist | Ich vermisse meine Familie sehr. — *I really miss my family.*<br>Hast du mich vermisst? — *Did you miss me?* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): German definition (sich wünschen, dass jemand da ist) and English definition (to feel sad) describe different things; they should match.
- **deepseek-v4p1-flash** (judge glm-5p3): Definition and second example are slightly stilted/textbook-like ('dass er oder es da ist'; 'Hast du deine Freunde in Berlin vermisst?' would more naturally be 'Hast du deine Freunde in Berlin vermisst?' with different word order or context, e.g. 'Hast du deine Freunde in Berlin vermisst?' is acceptable but less idiomatic than 'Ich habe meine Freunde in Berlin sehr vermisst').
- **glm-5p3** (judge kimi-k3): „nicht mehr da ist“ / „not there anymore“ is too narrow — vermissen does not imply permanent absence (you can miss someone who is just away).

### 22. mitnehmen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to take (with you) | jdn / etw. auf einen Weg mit sich nehmen | Kannst du mich ein Stück mit dem Auto mitnehmen? — *Can you give me a ride part of the way?*<br>Ich habe ihn zu einer Party mitgenommen. | |
| deepseek-v4p1-flash | nimmt mit · nahm mit · hat mitgenommen trennbar | to take along, to take with you | etwas oder jemanden mit sich an einen anderen Ort nehmen | Kannst du mich zum Bahnhof mitnehmen? — *Can you give me a ride to the station?*<br>Ich nehme den Regenschirm mit. — *I'll take the umbrella with me.* |  |
| glm-5p3 | nimmt mit · nahm mit · hat mitgenommen trennbar | to take along, to bring | eine Person oder Sache mitnehmen, wenn man irgendwo hingeht | Nimmst du deinen Regenschirm mit? — *Are you taking your umbrella with you?*<br>Ich habe dem Kind ein Buch mitgenommen. — *I brought a book for the child.* |  |
| kimi-k3 | nimmt mit · nahm mit · hat mitgenommen trennbar | to take along, to take with | etwas oder jemanden zu einem anderen Ort mitbringen | Soll ich dir was zu essen mitnehmen? — *Shall I bring you something to eat?*<br>Nimm doch einen Regenschirm mit, es regnet gleich. — *Take an umbrella with you, it's going to rain.* |  |

- **glm-5p3** (judge kimi-k3): 'to bring' is not an accurate equivalent for mitnehmen (that's mitbringen), and 'Ich habe dem Kind ein Buch mitgenommen' is less idiomatic than 'mitgebracht' for the given translation.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition is circular and 'to bring' is not a general equivalent for 'mitnehmen'.
- **kimi-k3** (judge glm-5p3): definition_de is circular and semantically wrong (uses 'mitbringen', which means bringing TO the speaker's location, not taking FROM it), and 'to take with' is incomplete without 'you'.
- **kimi-k3** (judge deepseek-v4p1-flash): Definition uses 'mitbringen' (bring) instead of 'mitnehmen', and 'to take with' is incomplete.

### 23. weg sein (phrase)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | phrase | to be out cold | ohne Bewusstsein sein | Für einen kurzen Moment war sie weg. — *She was out cold for a brief moment.* | |
| deepseek-v4p1-flash | ist weg · war weg · ist weg gewesen | to be gone, to be away | nicht mehr da oder nicht anwesend sein | Mein Handy ist schon wieder weg. — *My phone is gone again.*<br>Als ich kam, war sie schon weg. — *When I arrived, she was already gone.* |  |
| glm-5p3 | ist weg · war weg · ist weg gewesen | to be gone, to be out | nicht an einem bestimmten Ort anwesend sein | Gestern war Papa den ganzen Tag weg. — *Dad was out all day yesterday.*<br>Wo ist mein Handy? Eben war es noch weg... nein, hier! — *Where's my phone? It was just gone... no, here it is!* |  |
| kimi-k3 | ist weg · war weg · ist weg gewesen | to be gone, to be away | nicht mehr an einem Ort oder nicht mehr da sein | Mein Geldbeutel ist weg! — *My wallet is gone!*<br>Sie war das ganze Wochenende weg. — *She was away all weekend.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Good entry with two natural everyday examples; definition is simple and accurate.
- **glm-5p3** (judge kimi-k3): Definition covers only 'absent' while word_en also claims 'gone', and 'Eben war es noch weg' is unidiomatic (a native would say 'Eben war es noch da').
- **glm-5p3** (judge deepseek-v4p1-flash): Definition is too narrow ('anwesend' does not cover objects) and the second example is slightly awkward.
- **kimi-k3** (judge glm-5p3): Solid entry: covers both 'gone' (disappeared) and 'away' (absent) with two natural, distinct examples.

### 24. stehen bleiben (phrase)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | phrase | to stay | nicht anfangen, sich zu bewegen | Egal, was ich machte, der Esel blieb wie angewurzelt stehen. — *Whatever I did, the donkey stayed rooted to the spot.* | |
| deepseek-v4p1-flash | bleibt stehen · blieb stehen · ist stehen geblieben trennbar | to stop, to stand still | aufhören, sich zu bewegen, und an einer Stelle stehen | Der Bus ist an der Haltestelle stehen geblieben. — *The bus stopped at the bus stop.*<br>Wir sind kurz stehen geblieben, um die Karte zu lesen. — *We stopped briefly to read the map.* |  |
| glm-5p3 | bleibt stehen · blieb stehen · ist stehen geblieben trennbar | to stop, to stand still | nicht weitergehen und an einer Stelle anhalten | Wir sind vor dem Schaufenster stehen geblieben. — *We stopped in front of the shop window.*<br>Bleib doch mal kurz stehen, ich muss etwas sagen. — *Stop for a moment, I need to tell you something.* |  |
| kimi-k3 | bleibt stehen · blieb stehen · ist stehen geblieben | to stop, to remain standing | aufhören zu gehen oder sich zu bewegen und an einem Ort stehen | Bleib doch mal stehen, ich kann nicht so schnell laufen! — *Stop for a second, I can't walk that fast!*<br>Der Bus ist plötzlich stehen geblieben. — *The bus suddenly stopped.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Describes the 'stop moving' sense rather than Cambridge's 'stay/remain motionless' first sense, but that is the more common everyday meaning.
- **deepseek-v4p1-flash** (judge glm-5p3): Solid entry, but the chosen sense is 'to stop moving', not Cambridge's first sense 'to stay' (nicht anfangen, sich zu bewegen).
- **glm-5p3** (judge kimi-k3): Definition 'nicht weitergehen und an einer Stelle anhalten' is slightly narrow (walking only) and a touch awkward, though examples are excellent.
- **kimi-k3** (judge glm-5p3): Good examples and definitions, but the separable flag is incorrect and the sense differs from Cambridge's first sense ('to stay').; separable: false is wrong – 'stehen bleiben' behaves as a separable verb (er bleibt stehen, er ist stehen geblieben)
- **kimi-k3** (judge deepseek-v4p1-flash): The verb is separable, so 'separable' should be true.; separable is incorrectly marked false

### 25. verpflichtet sein (phrase)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | phrase | to owe sth |  | Ich bin Ihnen sehr zu Dank verpflichtet! — *I am deeply indebted to you!* | |
| deepseek-v4p1-flash | ist verpflichtet · war verpflichtet · ist verpflichtet gewesen | to be obliged, to be required | etwas tun müssen, weil es eine Pflicht oder Regel ist | Ich bin verpflichtet, Ihnen das zu sagen. — *I'm obliged to tell you that.*<br>Wir sind verpflichtet, die Regeln einzuhalten. — *We are required to follow the rules.* |  |
| glm-5p3 | ist verpflichtet · war verpflichtet · ist verpflichtet gewesen | to be obliged, to be required | etwas tun müssen, weil es eine Regel oder ein Gesetz ist | Wir sind verpflichtet, die Daten zu schützen. — *We are required to protect the data.*<br>Man ist verpflichtet, einen Ausweis mitzunehmen. — *You have to bring an ID card.* |  |
| kimi-k3 | ist verpflichtet · war verpflichtet · ist verpflichtet gewesen | to be obliged, to be required | etwas tun müssen, weil es eine Regel oder Pflicht vorschreibt | Alle Mitarbeiter sind zur Verschwiegenheit verpflichtet. — *All employees are obliged to maintain confidentiality.*<br>Du bist nicht verpflichtet, diese Frage zu beantworten. — *You're not required to answer that question.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Covers the common 'obliged/required' sense, not Cambridge's first sense 'jmdm. zu Dank verpflichtet sein' (to be indebted), but that is the right choice for A1–B1.
- **deepseek-v4p1-flash** (judge glm-5p3): Solid entry, but definition_de 'weil es eine Pflicht oder Regel ist' is slightly stilted; 'weil eine Pflicht oder Regel es verlangt' would be more idiomatic.
- **glm-5p3** (judge kimi-k3): Same correct sense choice as A; definition limited to 'Regel oder Gesetz' is slightly narrower than the word's full range (also moral duty), but acceptable.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition_de is inaccurate: 'weil es eine Regel oder ein Gesetz ist' does not mean because a rule/law requires it.
- **kimi-k3** (judge glm-5p3): Most natural examples, but definition_de is grammatically flawed, and 'zur Verschwiegenheit verpflichtet' uses vocabulary above B1 level.; definition_de: 'weil es eine Regel oder Pflicht vorschreibt' is unidiomatic/wrong argument structure; should be 'weil eine Regel oder Pflicht es vorschreibt'
