# German vocab generation: model bake-off

25 words (stratified: nouns, verbs, adjectives/adverbs, phrases), none of them few-shot examples. Grammar is checked against Cambridge GLOBAL German–English, only on the fields Cambridge lists. Semantic scores come from blind cross-model judges (each output is rated by the two *other* models; judging cost $0.76).

## Summary

| model | valid | retries | grammar vs Cambridge | sense = Cambridge #1 | most common sense | word_en ok | definitions ok | translations ok | judge: no grammar errors | naturalness (1–5) | latency | $/word | $ for full list |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **deepseek-v4p1-flash** | 25/25 | 0 | 100% (68 checks) | 78% | 96% | 98% | 86% | 100% | 100% | 4.76 | 7.0s | $0.0019 | $5.69 |
| **glm-5p3** | 25/25 | 0 | 100% (68 checks) | 72% | 92% | 96% | 66% | 98% | 94% | 4.76 | 4.2s | $0.0020 | $6.03 |
| **kimi-k3** | 25/25 | 0 | 99% (68 checks) | 62% | 92% | 100% | 84% | 94% | 100% | 4.80 | 8.4s | $0.0117 | $34.80 |

## Per word

### 1. Handel (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. — · gen. Handels | trade | das Kaufen und Verkaufen von Waren | Handel treiben — *to trade*<br>der illegale Handel mit Rauschgift | |
| deepseek-v4p1-flash | der · pl. — · gen. des Handels | trade, commerce | das Kaufen und Verkaufen von Waren | Der Handel mit Kaffee ist ein großes Geschäft. — *The coffee trade is a big business.*<br>Zwischen den Ländern gibt es viel Handel. — *There is a lot of trade between the countries.* |  |
| glm-5p3 | der · pl. — · gen. des Handels | trade, commerce | das Kaufen und Verkaufen von Waren, besonders zwischen Ländern oder Firmen | Deutschland treibt viel Handel mit China. — *Germany does a lot of trade with China.*<br>Der internationale Handel wächst jedes Jahr. — *International trade grows every year.* |  |
| kimi-k3 | der · pl. — · gen. des Handels | trade, commerce | der Kauf und Verkauf von Waren zwischen Personen, Firmen oder Ländern | Der Handel zwischen den beiden Ländern wächst. — *Trade between the two countries is growing.*<br>Er arbeitet im internationalen Handel. — *He works in international trade.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Second example is grammatical but slightly textbook-like; otherwise solid.
- **deepseek-v4p1-flash** (judge glm-5p3): "Zwischen den Ländern gibt es viel Handel" klingt lehrbuchhaft; natürlicher wäre "Die Länder treiben (regen) Handel miteinander".

### 2. Trauung (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Trauungen · gen. Trauung | wedding (ceremony) | Hochzeitszeremonie | eine standesamtliche / kirchliche Trauung — *a civil/church wedding*<br>die Trauung vollziehen | |
| deepseek-v4p1-flash | die · pl. die Trauungen · gen. der Trauung | wedding ceremony, marriage ceremony | die offizielle Zeremonie, bei der zwei Menschen heiraten | Die Trauung findet um elf Uhr in der Kirche statt. — *The wedding ceremony takes place at eleven o'clock in the church.*<br>Nach der Trauung feiern wir im Restaurant. — *After the ceremony we're celebrating in a restaurant.* |  |
| glm-5p3 | die · pl. die Trauungen · gen. der Trauung | wedding ceremony | die feierliche Handlung, bei der zwei Menschen rechtlich ein Paar werden | Die Trauung findet im Rathaus statt. — *The wedding ceremony is taking place at the town hall.*<br>Nach der Trauung gibt es ein gemeinsames Essen. — *After the ceremony there's a meal together.* |  |
| kimi-k3 | die · pl. die Trauungen · gen. der Trauung | wedding ceremony | die feierliche Zeremonie, bei der zwei Menschen heiraten | Die Trauung findet am Samstag in der Kirche statt. — *The wedding ceremony takes place on Saturday in church.*<br>Nach der Trauung gab es ein großes Fest. — *After the ceremony there was a big celebration.* |  |

- **glm-5p3** (judge kimi-k3): Definition is inaccurate: a Trauung (e.g. a church wedding) does not necessarily make two people legally a couple.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition wrongly restricts Trauung to a legal act, and the second English translation is awkward.
- **kimi-k3** (judge glm-5p3): Solid entry; the English example translation 'takes place on Saturday in church' would be slightly more natural as 'in church on Saturday'.

### 3. stoßen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | stößt · stieß · gestoßen · haben | to push, to shove | jdm / etw. einen Stoß versetzen | jdn ins Wasser stoßen — *to push sb into the water*<br>Er stieß aus Versehen das Glas vom Tisch. | |
| deepseek-v4p1-flash | stößt · stieß · hat gestoßen | to push, to shove | jemanden oder etwas mit einem kräftigen Druck bewegen | Stoß mich nicht so! — *Don't push me like that!*<br>Er hat mich aus Versehen gestoßen. — *He accidentally pushed me.* |  |
| glm-5p3 | stößt · stieß · hat gestoßen | to push, to shove | jemanden oder etwas mit Kraft kurz von sich weg bewegen | Er hat mich absichtlich gestoßen. — *He pushed me on purpose.*<br>Stoß die Tür mal mit dem Fuß zu. — *Push the door shut with your foot.* |  |
| kimi-k3 | stößt · stieß · ist gestoßen | to bump, to knock | mit einem Körperteil hart gegen etwas kommen | Ich bin mit dem Kopf gegen die Tür gestoßen. — *I bumped my head on the door.*<br>Pass auf, dass du nicht an den Tisch stößt! — *Careful you don't knock against the table!* | auxiliary |

- **deepseek-v4p1-flash** (judge kimi-k3): "mit einem kräftigen Druck" suggests sustained pressure (drücken); stoßen is a short, sharp push or jolt.
- **glm-5p3** (judge kimi-k3): The second example actually illustrates the separable verb "zustoßen", not bare "stoßen".
- **glm-5p3** (judge deepseek-v4p1-flash): Definition is too narrow ('von sich weg') and one example uses separable 'zustoßen'.; Example 'Stoß die Tür mal mit dem Fuß zu' uses separable verb 'zustoßen', not 'stoßen'.
- **kimi-k3** (judge glm-5p3): This is the intransitive 'bump/knock against something' sense, not the transitive 'push/shove' sense that should be the first sense; 'Pass auf, dass du nicht an den Tisch stößt' is also a bit stilted compared to 'dass du dich nicht stößt'.
- **kimi-k3** (judge deepseek-v4p1-flash): Chosen sense is intransitive bump/knock, not Cambridge's first transitive push/shove; second translation slightly unidiomatic.

### 4. lesen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | liest · las · gelesen · haben | to read | Geschriebenes ansehen und den Sinn entnehmen | Liest du gerne / viel? — *Do you like/do a lot of reading?*<br>Die winzige Schrift war kaum zu lesen. | |
| deepseek-v4p1-flash | liest · las · hat gelesen | to read | geschriebene Wörter oder Texte mit den Augen erfassen und verstehen | Ich lese jeden Abend ein Buch. — *I read a book every evening.*<br>Hast du den Artikel schon gelesen? — *Have you read the article yet?* |  |
| glm-5p3 | liest · las · hat gelesen | to read | geschriebene Texte verstehen, indem man die Wörter mit den Augen aufnimmt | Ich lese jeden Abend ein paar Seiten. — *I read a few pages every evening.*<br>Hast du dieses Buch schon gelesen? — *Have you read this book yet?* |  |
| kimi-k3 | liest · las · hat gelesen | to read | geschriebenen Text anschauen und verstehen | Ich lese abends gern im Bett. — *I like reading in bed in the evening.*<br>Hast du die Zeitung heute schon gelesen? — *Have you read the newspaper today?* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): "Ich lese jeden Abend ein Buch" is grammatical but slightly implausible/textbook-like (a whole book every evening).
- **deepseek-v4p1-flash** (judge glm-5p3): "Ich lese jeden Abend ein Buch" sounds slightly textbook-like (a whole book every evening?); "ein paar Seiten" or "in einem Buch" would be more natural.
- **kimi-k3** (judge glm-5p3): definition_de is slightly awkward: "anschauen" fits visual objects better than text; "ansehen" or "aufnehmen" would be more idiomatic.

### 5. dumm (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adjective | stupid, dumb | mit wenig Intelligenz | Sie stellt sich gern dumm, damit man ihr keine Verantwortung überträgt. — *She likes to act dumb so nobody gives her any responsibility.*<br>sich wie ein dummer kleiner Junge benehmen | |
| deepseek-v4p1-flash | dümmer · am dümmsten | stupid, silly | nicht klug; ohne guten Verstand | Das war wirklich eine dumme Idee. — *That was a really stupid idea.*<br>So eine dumme Frage hört man selten. — *You rarely hear such a stupid question.* |  |
| glm-5p3 | dümmer · am dümmsten | stupid, silly | nicht klug; ohne gutes Urteilsvermögen | Das war eine wirklich dumme Frage. — *That was a really silly question.*<br>Entschuldigung, das war dumm von mir. — *Sorry, that was stupid of me.* |  |
| kimi-k3 | dümmer · am dümmsten | stupid, dumb | nicht intelligent; ohne gutes Urteilsvermögen | Das war eine wirklich dumme Idee. — *That was a really stupid idea.*<br>Stell dich nicht so dumm an! — *Don't be so stupid!* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): 'So eine dumme Frage hört man selten' is grammatical but stilted and textbook-like; a native speaker would rarely say this.
- **glm-5p3** (judge kimi-k3): "dumb" would be a more standard second equivalent than "silly", but the entry is otherwise solid.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition uses too advanced 'Urteilsvermögen' for A1–B1.
- **kimi-k3** (judge glm-5p3): The second example uses 'sich dumm anstellen' (act dumb/fool around), a slightly different construction than the plain adjective sense, though the German itself is natural.
- **kimi-k3** (judge deepseek-v4p1-flash): Definition uses too advanced 'Urteilsvermögen' for A1–B1.

### 6. Nummer (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Nummern · gen. Nummer | number | Zahl, die den Platz in einer Reihenfolge angibt | der Teilnehmer mit der Nummer 25 — *competitor number 25* | |
| deepseek-v4p1-flash | die · pl. die Nummern · gen. der Nummer | number | eine Ziffernfolge, mit der man jemanden oder etwas kennzeichnet | Kannst du mir deine Nummer geben? — *Can you give me your number?*<br>Auf dem Trikot steht die Nummer 10. — *The number 10 is on the jersey.* |  |
| glm-5p3 | die · pl. die Nummern · gen. der Nummer | number | eine Zahl oder Zeichenfolge, die etwas Bestimmtes kennzeichnet, z. B. eine Person oder ein Haus | Wie ist deine Telefonnummer? — *What's your phone number?*<br>Wir wohnen in der Nummer zwölf. — *We live at number twelve.* |  |
| kimi-k3 | die · pl. die Nummern · gen. der Nummer | number | eine Ziffer oder Zahl, die etwas kennzeichnet, z. B. ein Telefon oder ein Haus | Kannst du mir deine Nummer geben? — *Can you give me your number?*<br>Ich habe die falsche Nummer gewählt. — *I dialled the wrong number.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Sense (identifying number, esp. phone/jersey) is the most useful everyday one but is broader than Cambridge's first sense (position in a sequence); 'The number 10 is on the jersey' is faithful but slightly literal.
- **glm-5p3** (judge kimi-k3): "Wir wohnen in der Nummer zwölf" is unidiomatic; a native speaker would say "Wir wohnen in Hausnummer zwölf" or "im Haus Nummer zwölf".
- **glm-5p3** (judge deepseek-v4p1-flash): Example 'Wir wohnen in der Nummer zwölf' is unidiomatic; 'Hausnummer' or 'in Nummer zwölf' would be natural.
- **kimi-k3** (judge glm-5p3): Definition is imprecise: a phone number is not 'eine Ziffer' (a single digit), and 'such as a phone or a house' should refer to the number, not the object; examples themselves are excellent.
- **kimi-k3** (judge deepseek-v4p1-flash): Definition says a number identifies a telephone, which is inaccurate; it should be a phone number/line.

### 7. Ausländer (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Ausländer · gen. Ausländers | foreigner |  | eine Schule mit hohem Ausländeranteil — *a school with a large number of foreign immigrants* | |
| deepseek-v4p1-flash | der · pl. die Ausländer · gen. des Ausländers | foreigner | eine Person, die die Staatsangehörigkeit eines anderen Landes hat | In unserer Klasse sind viele Ausländer. — *There are many foreigners in our class.*<br>Mein Nachbar ist Ausländer und spricht fünf Sprachen. — *My neighbour is a foreigner and speaks five languages.* |  |
| glm-5p3 | der · pl. die Ausländer · gen. des Ausländers | foreigner | eine Person, die aus einem anderen Land kommt und nicht die Staatsangehörigkeit des Landes hat, in dem sie lebt | Viele Ausländer leben und arbeiten in Deutschland. — *Many foreigners live and work in Germany.*<br>Als Ausländer braucht man hier ein Visum. — *As a foreigner, you need a visa here.* |  |
| kimi-k3 | der · pl. die Ausländer · gen. des Ausländers | foreigner | eine Person, die aus einem anderen Land kommt oder eine andere Staatsangehörigkeit hat | In dieser Stadt leben viele Ausländer. — *A lot of foreigners live in this city.*<br>Als Ausländer braucht er ein Visum. — *As a foreigner, he needs a visa.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Definition omits the reference point ('eines anderen Landes' than which one?), and 'In unserer Klasse sind viele Ausländer' is grammatical but slightly textbook-like and dated in tone.
- **glm-5p3** (judge kimi-k3): Definition is too restrictive: it requires both foreign origin and lack of citizenship, but someone born in the country without its citizenship is also an Ausländer.
- **kimi-k3** (judge glm-5p3): The 'or' in the definition is inaccurate: someone who comes from another country but has taken local citizenship is no longer an Ausländer; the defining criterion is citizenship, not origin.

### 8. bloß (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adjective | bare | nicht mit etw. bedeckt | sich auf die bloße Erde setzen — *to sit on the bare ground*<br>Frierst du nicht mit bloßen Armen? | |
| deepseek-v4p1-flash | adverb | only, just | nur, nicht mehr als das, was genannt wird | Ich habe bloß zehn Euro dabei. — *I only have ten euros on me.*<br>Das war bloß ein Scherz. — *That was just a joke.* |  |
| glm-5p3 | adverb | only, just | nichts weiter als; keine anderen als die genannten | Ich habe bloß zwanzig Euro dabei. — *I've only got twenty euros on me.*<br>Das war bloß ein Scherz! — *That was just a joke!* |  |
| kimi-k3 | adverb | only, just | nicht mehr als; nur | Ich habe bloß noch fünf Euro dabei. — *I've only got five euros left on me.*<br>Ich wollte bloß kurz Hallo sagen. — *I just wanted to say hi quickly.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Cambridge's first sense is the adjective 'bare', but the adverb 'only/just' is correctly chosen as the most common everyday meaning; entry is clean.
- **deepseek-v4p1-flash** (judge glm-5p3): Solid entry; the German definition 'nicht mehr als das, was genannt wird' is slightly clunky but acceptable.
- **glm-5p3** (judge kimi-k3): Second half of the German definition ('keine anderen als die genannten') is slightly awkward for 'bloß', but overall accurate.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition includes inaccurate/overly narrow paraphrase 'keine anderen als die genannten'.
- **kimi-k3** (judge deepseek-v4p1-flash): Translation 'say hi quickly' is less idiomatic for 'kurz Hallo sagen'.

### 9. traditionell (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adjective | traditional |  | ein traditioneller Tanz — *a traditional dance* | |
| deepseek-v4p1-flash | traditioneller · am traditionellsten | traditional | so, wie es seit langer Zeit üblich ist | Die Hochzeit war sehr traditionell. — *The wedding was very traditional.*<br>Er trägt zu Festen traditionelle Kleidung. — *He wears traditional clothes for festivals.* |  |
| glm-5p3 | traditioneller · am traditionellsten | traditional | so, wie es seit langer Zeit üblich ist und weitergegeben wird | Wir feiern Weihnachten auf traditionelle Art. — *We celebrate Christmas in a traditional way.*<br>Das Restaurant serviert traditionelle deutsche Gerichte. — *The restaurant serves traditional German dishes.* |  |
| kimi-k3 | traditioneller · am traditionellsten | traditional | so, wie es in einer Familie oder einem Land seit langer Zeit üblich ist | Wir essen traditionell an Weihnachten Gans. — *We traditionally eat goose at Christmas.*<br>Sie trägt ein traditionelles Kleid aus ihrer Heimat. — *She's wearing a traditional dress from her home country.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): "zu Festen" is grammatical but slightly stilted; "an Feiertagen" or "bei Festen" would sound more natural.
- **kimi-k3** (judge glm-5p3): First example uses 'traditionell' adverbially, which mismatches the adjective part of speech, and the word order 'Wir essen traditionell an Weihnachten Gans' is stilted; 'An Weihnachten essen wir traditionell Gans' would be more natural.
- **kimi-k3** (judge deepseek-v4p1-flash): Example 'Wir essen traditionell an Weihnachten Gans' uses traditionell adverbially and has slightly marked word order.

### 10. Rabatt (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Rabatte · gen. Rabattes | discount | Preisnachlass | Frühbucherrabatt<br>Mengenrabatt | |
| deepseek-v4p1-flash | der · pl. die Rabatte · gen. des Rabatts | discount | ein niedrigerer Preis, den man beim Kauf von etwas bekommt | Auf diese Jacke gibt es gerade 20 Prozent Rabatt. — *There's 20 percent off this jacket right now.*<br>Kannst du mir einen kleinen Rabatt geben? — *Can you give me a small discount?* |  |
| glm-5p3 | der · pl. die Rabatte · gen. des Rabatts | discount | ein Betrag, um den der Preis einer Ware oder Dienstleistung gesenkt wird | Auf diesen Mantel gibt es 20 Prozent Rabatt. — *There's a 20 percent discount on this coat.*<br>Studenten bekommen bei uns Rabatt. — *Students get a discount from us.* |  |
| kimi-k3 | der · pl. die Rabatte · gen. des Rabatts | discount | ein Betrag, um den der Preis für etwas reduziert wird | Auf diese Jacke gibt es 20 Prozent Rabatt. — *There's a 20 percent discount on this jacket.*<br>Studenten bekommen hier oft einen Rabatt. — *Students often get a discount here.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): The definition describes the reduced price itself, but 'Rabatt' is the reduction/amount deducted, not the lower price.
- **deepseek-v4p1-flash** (judge glm-5p3): Definition is imprecise: 'Rabatt' is the reduction/amount taken off the price, not the lower price itself.

### 11. voraus (adjective_adverb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | adverb | ahead | besser, schneller usw. als andere / anderes | Andere Länder sind uns in Sachen Bildungspolitik weit voraus. — *Other countries are way ahead of us in terms of educational policy.*<br>seiner Zeit voraus sein | |
| deepseek-v4p1-flash | adverb | ahead, in front | weiter vorn als jemand oder etwas anderes | Geh schon mal voraus, ich komme gleich nach. — *Go ahead, I'll follow in a moment.*<br>Sie ist uns schon weit voraus. — *She is already far ahead of us.* |  |
| glm-5p3 | adverb | ahead, in front | an einer Stelle vor den anderen; bevor etwas anderes passiert | Die Kinder laufen immer voraus. — *The children always run on ahead.*<br>Ich schicke die Unterlagen voraus. — *I'll send the documents ahead.* |  |
| kimi-k3 | adverb | ahead, in advance | vor anderen oder vor dem eigentlichen Zeitpunkt | Geh schon mal voraus, ich komme gleich nach. — *Go on ahead, I'll follow in a minute.*<br>Danke im Voraus für deine Hilfe! — *Thanks in advance for your help!* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Guter Eintrag zur räumlichen Bedeutung, aber 'Sie ist uns schon weit voraus' schwebt unklar zwischen räumlicher und Cambridges übertragener Bedeutung ('in der Entwicklung voraus').
- **glm-5p3** (judge kimi-k3): Covers the common spatial/temporal sense well, but not Cambridge's comparative 'ahead of others' sense.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition mixes spatial 'ahead' with temporal 'before', which is not the meaning of 'voraus'.
- **kimi-k3** (judge glm-5p3): Sehr nützliche Alltagsbeispiele, aber der Eintrag vermengt zwei Bedeutungen (räumlich 'voraus' und zeitlich 'im Voraus'), was für eine Einsinn-Definition unsauber ist.
- **kimi-k3** (judge deepseek-v4p1-flash): Combines two senses and uses the fixed phrase 'im Voraus', which is not the adverb 'voraus' alone.

### 12. Kuh (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Kühe · gen. Kuh | cow | weibliches Rind | Kühe geben Milch. — *Cows produce milk.*<br>die Kühe melken | |
| deepseek-v4p1-flash | die · pl. die Kühe · gen. der Kuh | cow | ein großes Nutztier, das Milch gibt und auf der Wiese grast | Die Kühe stehen auf der Wiese. — *The cows are standing in the field.*<br>Auf dem Bauernhof gibt es viele Kühe. — *There are many cows on the farm.* |  |
| glm-5p3 | die · pl. die Kühe · gen. der Kuh | cow | ein großes Tier, das auf Bauernhöfen lebt und Milch gibt | Die Kühe grasen auf der Wiese. — *The cows are grazing in the meadow.*<br>Auf dem Bauernhof gibt es zwanzig Kühe. — *There are twenty cows on the farm.* |  |
| kimi-k3 | die · pl. die Kühe · gen. der Kuh | cow | ein großes Nutztier, das Milch gibt und auf dem Bauernhof lebt | Die Kühe stehen draußen auf der Wiese. — *The cows are out in the field.*<br>Auf dem Bauernhof gibt es zwanzig Kühe. — *There are twenty cows on the farm.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Definition is slightly redundant ('grazes in fields' adds little beyond 'farm animal'), but otherwise flawless.

### 13. vertreten (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to stand in / deputize for | jds Aufgaben für eine bestimmte Zeit übernehmen | Er hat sich auf der Sitzung von seiner Assistentin vertreten lassen. — *He had his assistant stand in for him at the meeting.* | |
| deepseek-v4p1-flash | vertritt · vertrat · hat vertreten | to stand in for, to represent | für jemanden handeln, der gerade nicht da ist | Kannst du mich morgen im Meeting vertreten? — *Can you stand in for me at the meeting tomorrow?*<br>Meine Kollegin vertritt mich, während ich im Urlaub bin. — *My colleague is standing in for me while I'm on holiday.* |  |
| glm-5p3 | vertritt · vertrat · hat vertreten | to represent, to stand in for | die Aufgaben oder Interessen von jemandem übernehmen oder ausdrücken | Ich vertrete meinen Kollegen diese Woche im Urlaub. — *I'm standing in for my colleague this week while he's on holiday.*<br>Sie hat die Firma bei dem Treffen vertreten. — *She represented the company at the meeting.* |  |
| kimi-k3 | vertritt · vertrat · hat vertreten | to represent | offiziell für eine Person oder Gruppe sprechen oder handeln | Sie vertritt ihre Firma auf der Messe. — *She's representing her company at the trade fair.*<br>Welcher Anwalt hat dich vor Gericht vertreten? — *Which lawyer represented you in court?* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): word_en adds 'to represent', which is a different sense and misleading for a single-meaning entry; otherwise excellent.
- **deepseek-v4p1-flash** (judge glm-5p3): Faithful to Cambridge's first sense with fully natural examples, but 'stand in for' is a narrower, less frequent everyday meaning than 'to represent'.
- **glm-5p3** (judge kimi-k3): Definition blurs two distinct senses (standing in vs. representing interests), and 'Ich vertrete meinen Kollegen diese Woche im Urlaub' is ambiguous about who is on holiday.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition conflates 'stand in' and 'represent' and is not a single most common sense.
- **kimi-k3** (judge glm-5p3): Does not match Cambridge's first sense, but 'to represent' (a company, a client) is arguably the most common everyday meaning and the entry is clean and natural throughout.
- **kimi-k3** (judge deepseek-v4p1-flash): Chosen sense is 'represent', not Cambridge's 'stand in' sense.

### 14. zerstören (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to destroy | etw. so stark beschädigen, dass man es nicht mehr benutzen kann | Dresden wurde im Krieg fast völlig zerstört. — *Dresden was almost completely destroyed in the war.* | |
| deepseek-v4p1-flash | zerstört · zerstörte · hat zerstört | to destroy | etwas so stark beschädigen, dass es nicht mehr zu gebrauchen ist | Der Brand hat das ganze Haus zerstört. — *The fire destroyed the whole house.*<br>Der Krieg hat viele Städte zerstört. — *The war destroyed many cities.* |  |
| glm-5p3 | zerstört · zerstörte · hat zerstört | to destroy | etwas so beschädigen, dass es nicht mehr existiert oder nicht mehr benutzt werden kann | Der Sturm hat viele Häuser zerstört. — *The storm destroyed many houses.*<br>Der Brand hat die alte Kirche völlig zerstört. — *The fire completely destroyed the old church.* |  |
| kimi-k3 | zerstört · zerstörte · hat zerstört | to destroy | etwas so stark beschädigen, dass es kaputt ist oder nicht mehr existiert | Das Feuer hat das ganze Haus zerstört. — *The fire destroyed the whole house.*<br>Vorsicht, du zerstörst noch meine Brille! — *Careful, you'll break my glasses!* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Definition is slightly narrower than the core sense, omitting the "no longer exists" aspect (e.g. a city destroyed in war).
- **deepseek-v4p1-flash** (judge glm-5p3): Die Definition ('nicht mehr zu gebrauchen') ist zu eng, da zerstörte Städte nicht nur unbrauchbar, sondern nicht mehr existent sind.
- **kimi-k3** (judge glm-5p3): Sehr gelungen; das zweite Beispiel ist authentische gesprochene Sprache und die Übersetzung mit 'break' ist idiomatisch.
- **kimi-k3** (judge deepseek-v4p1-flash): Second example is unidiomatic: zerstören is too strong for glasses, and 'break' is not a faithful translation.

### 15. Lebenslauf (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Lebensläufe · gen. Lebenslaufes | résumé | schriftliche Darstellung des eigenen, bisherigen Lebensweges für eine Bewerbung | ein tabellarischer Lebenslauf — *a résumé in tabular form* | |
| deepseek-v4p1-flash | der · pl. die Lebensläufe · gen. des Lebenslaufs | CV, résumé | eine schriftliche Übersicht über Ausbildung und Berufserfahrung, die man bei einer Bewerbung abgibt | Für die Bewerbung brauche ich meinen Lebenslauf. — *I need my CV for the application.*<br>Schick deinen Lebenslauf bitte an die Firma. — *Please send your CV to the company.* |  |
| glm-5p3 | der · pl. die Lebensläufe · gen. des Lebenslaufs | CV, résumé | ein kurzer schriftlicher Text über die eigene Ausbildung und die bisherigen Jobs | Für die Bewerbung brauche ich einen Lebenslauf. — *I need a CV for the application.*<br>Schick mir bitte deinen Lebenslauf per E-Mail. — *Please send me your CV by email.* |  |
| kimi-k3 | der · pl. die Lebensläufe · gen. des Lebenslaufs | CV, résumé | ein Dokument mit den wichtigsten Informationen über Ausbildung und Beruf einer Person, das man bei einer Bewerbung mitschickt | Schick mir bitte deinen Lebenslauf als PDF. — *Please send me your CV as a PDF.*<br>In ihrem Lebenslauf stehen drei Jahre Auslandserfahrung. — *Her CV lists three years of experience abroad.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): In der Definition ist „abgibt“ etwas unüblich; natürlicher wäre „mitschickt“ oder „einreicht“.
- **deepseek-v4p1-flash** (judge glm-5p3): 'Schick deinen Lebenslauf bitte an die Firma' klingt durch die Wortstellung leicht steif; 'abgibt' in der Definition ist weniger üblich als 'einschickt'.

### 16. Hauptbahnhof (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Hauptbahnhöfe · gen. Hauptbahnhofes | main/central station | größter Bahnhof einer Stadt |  | |
| deepseek-v4p1-flash | der · pl. die Hauptbahnhöfe · gen. des Hauptbahnhofs | main station, central station | der wichtigste Ort in einer Stadt, an dem Züge ankommen und abfahren | Wir treffen uns am Hauptbahnhof. — *We're meeting at the main station.*<br>Der Zug fährt vom Hauptbahnhof ab. — *The train leaves from the main station.* |  |
| glm-5p3 | der · pl. die Hauptbahnhöfe · gen. des Hauptbahnhofs | main station, central station | der größte und wichtigste Bahnhof einer Stadt | Der Zug hält nicht am Hauptbahnhof. — *The train doesn't stop at the main station.*<br>Wir treffen uns am Hauptbahnhof. — *We're meeting at the main station.* |  |
| kimi-k3 | der · pl. die Hauptbahnhöfe · gen. des Hauptbahnhofs | main station, central station | der größte und wichtigste Bahnhof einer Stadt | Der Zug nach Berlin fährt vom Hauptbahnhof ab. — *The train to Berlin leaves from the main station.*<br>Wir treffen uns um drei Uhr am Hauptbahnhof. — *We're meeting at the main station at three o'clock.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Definition describes a generic 'Ort' rather than a Bahnhof, making it less precise than A/B.
- **deepseek-v4p1-flash** (judge glm-5p3): Definition is slightly vaguer than 'größter Bahnhof einer Stadt' but still accurate and learner-friendly.

### 17. wiegen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | wog · gewogen · haben | to weigh | das Gewicht von jdm / etw. bestimmen | Das Obst wird an der Kasse gewogen. — *The fruit is weighed at the checkout.*<br>Sie wiegt sich jeden Morgen. | |
| deepseek-v4p1-flash | wiegt · wog · hat gewogen | to weigh | eine bestimmte Schwere haben | Ich wiege 70 Kilo. — *I weigh 70 kilos.*<br>Das Paket wiegt fast fünf Kilo. — *The parcel weighs almost five kilos.* |  |
| glm-5p3 | wiegt · wog · hat gewogen | to weigh | mit einer Waage messen, wie schwer etwas oder jemand ist | Der Verkäufer hat das Fleisch gewogen. — *The shop assistant weighed the meat.*<br>Wie viel wiegst du denn? — *How much do you weigh?* |  |
| kimi-k3 | wiegt · wog · hat gewogen | to weigh | ein bestimmtes Gewicht haben | Wie viel wiegst du denn? — *How much do you weigh?*<br>Der Koffer hat fast 20 Kilo gewogen. — *The suitcase weighed almost 20 kilos.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Same intransitive sense as B rather than Cambridge's transitive first sense; "Schwere" is also less simple than the standard "Gewicht" for A1–B1 learners.
- **deepseek-v4p1-flash** (judge glm-5p3): Right sense and good examples, but 'eine bestimmte Schwere haben' is unidiomatic lexicographer German; it should be 'ein bestimmtes Gewicht haben'.
- **glm-5p3** (judge kimi-k3): The second example ("Wie viel wiegst du denn?") illustrates the intransitive sense, not the defined transitive sense of weighing something on scales.
- **glm-5p3** (judge deepseek-v4p1-flash): Example 2 illustrates the intransitive sense, not the transitive definition.
- **kimi-k3** (judge glm-5p3): Best entry overall: it covers the most common everyday sense with a correct, simple definition and natural examples.

### 18. Ausbildung (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | die · pl. Ausbildungen · gen. Ausbildung | apprenticeship | eine Zeit, in der man einen Beruf in der Praxis erlernt | eine Ausbildung zum Elektriker machen — *to do an apprenticeship as an electrician*<br>noch in der Ausbildung sein | |
| deepseek-v4p1-flash | die · pl. die Ausbildungen · gen. der Ausbildung | training, apprenticeship | eine Zeit, in der man einen Beruf lernt und dabei in einem Betrieb arbeitet | Sie macht eine Ausbildung als Krankenschwester. — *She is doing training as a nurse.*<br>Nach der Ausbildung hat er schnell eine Stelle gefunden. — *After his training, he quickly found a job.* |  |
| glm-5p3 | die · pl. die Ausbildungen · gen. der Ausbildung | training, apprenticeship | das Lernen eines Berufs in einem Betrieb oder einer Schule | Sie macht eine Ausbildung zur Friseurin. — *She's doing an apprenticeship as a hairdresser.*<br>Nach der Schule beginnt er seine Ausbildung. — *After school he starts his training.* |  |
| kimi-k3 | die · pl. die Ausbildungen · gen. der Ausbildung | training, vocational training | die Zeit, in der man einen Beruf in einer Firma und in der Schule lernt | Meine Tochter macht eine Ausbildung zur Krankenschwester. — *My daughter is training to be a nurse.*<br>Nach der Ausbildung hat er sofort einen Job gefunden. — *He found a job straight after his training.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Definition slightly over-restricts to Betrieb (excludes schulische Ausbildung), but acceptable for A1–B1.
- **kimi-k3** (judge glm-5p3): Definition's 'in einer Firma und in der Schule' is slightly awkward phrasing of the dual system, and 'apprenticeship' would be a more idiomatic equivalent than 'vocational training'.

### 19. Augenblick (noun)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | der · pl. Augenblicke · gen. Augenblickes | moment | sehr kurzer Zeitraum | Einen Augenblick, bitte! — *Just a moment, please.*<br>das Flugzeug im letzten Augenblick erreichen | |
| deepseek-v4p1-flash | der · pl. die Augenblicke · gen. des Augenblicks | moment | eine sehr kurze Zeitspanne | Einen Augenblick, bitte! — *One moment, please!*<br>Ich bin in einem Augenblick zurück. — *I'll be back in a moment.* |  |
| glm-5p3 | der · pl. die Augenblicke · gen. des Augenblicks | moment | eine sehr kurze Zeitspanne | Einen Augenblick, ich komme gleich! — *Just a moment, I'll be right there!*<br>In diesem Augenblick klingelte das Telefon. — *At that moment the phone rang.* |  |
| kimi-k3 | der · pl. die Augenblicke · gen. des Augenblicks | moment | eine sehr kurze Zeit | Warten Sie bitte einen Augenblick! — *Please wait a moment!*<br>Im letzten Augenblick ist er noch gekommen. — *He arrived at the last moment.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): "Ich bin in einem Augenblick zurück" is grammatical but slightly less idiomatic than "Ich bin gleich wieder da".
- **deepseek-v4p1-flash** (judge glm-5p3): 'One moment, please!' is acceptable but 'Just a moment, please!' would be more idiomatic English; 'Ich bin in einem Augenblick zurück' is fine but 'Ich bin gleich zurück' is more colloquial.
- **kimi-k3** (judge glm-5p3): Second example 'Im letzten Augenblick ist er noch gekommen' is grammatical but slightly stilted; 'Er ist im letzten Augenblick noch gekommen' would be more natural.

### 20. setzen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to sit (down) | eine sitzende Stellung einnehmen | sich aufs Pferd setzen — *to get into the saddle*<br>Sie setzte sich zu mir / neben mich. | |
| deepseek-v4p1-flash | setzt sich · setzte sich · hat sich gesetzt refl. | to sit down, to take a seat | sich auf einen Stuhl, eine Bank oder den Boden niederlassen | Setz dich doch zu mir! — *Come and sit down next to me!*<br>Wir haben uns auf die Bank gesetzt. — *We sat down on the bench.* |  |
| glm-5p3 | setzt · setzte · hat gesetzt | to put, to place | etwas an eine Stelle bringen und dort hinlegen oder hinstellen | Sie hat den Blumentopf aufs Fensterbrett gesetzt. — *She put the flowerpot on the windowsill.*<br>Er setzt sich eine Mütze auf. — *He puts on a cap.* |  |
| kimi-k3 | setzt · setzte · hat gesetzt | to put, to place | etwas an eine bestimmte Stelle legen oder stellen | Setz das Buch einfach auf den Tisch. — *Just put the book on the table.*<br>Sie hat das Kind auf den Stuhl gesetzt. — *She sat the child on the chair.* |  |

- **deepseek-v4p1-flash** (judge glm-5p3): Correct and natural entry for 'sich setzen' (to sit down), matching Cambridge's first sense, but it treats the reflexive as a separate lemma and omits the base verb's more common transitive 'put/place' meaning.
- **glm-5p3** (judge kimi-k3): Second example belongs to the lemma 'aufsetzen', so it does not illustrate 'setzen'.; Second example 'Er setzt sich eine Mütze auf.' illustrates the separable verb 'aufsetzen', not the headword 'setzen'.
- **glm-5p3** (judge deepseek-v4p1-flash): Second example illustrates separable 'aufsetzen', not 'setzen'; definition is imprecise.; Example 'Er setzt sich eine Mütze auf' uses separable verb 'aufsetzen', not 'setzen'.
- **kimi-k3** (judge glm-5p3): Solid entry for the transitive 'put/place' sense, which is the most common everyday meaning of the bare verb 'setzen', though it differs from Cambridge's first (reflexive) sense.
- **kimi-k3** (judge deepseek-v4p1-flash): Definition uses 'legen/stellen' rather than the specific meaning of 'setzen'; first example is unidiomatic.

### 21. vermissen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to miss | Sehnsucht empfinden, weil jd / etw. fehlt | Es ist schön, dass du wieder da bist; ich habe dich so vermisst! — *I’m glad you’re back. I really missed you!* | |
| deepseek-v4p1-flash | vermisst · vermisste · hat vermisst | to miss | traurig sein, weil jemand oder etwas nicht mehr da ist | Ich vermisse meine Familie sehr. — *I miss my family a lot.*<br>Nach dem Umzug hat sie ihre Freunde oft vermisst. — *After moving, she often missed her friends.* |  |
| glm-5p3 | vermisst · vermisste · hat vermisst | to miss | traurig sein, weil jemand oder etwas nicht mehr da ist | Ich vermisse meine Familie sehr. — *I really miss my family.*<br>Nach dem Umzug habe ich meine Freunde vermisst. — *After moving, I missed my friends.* |  |
| kimi-k3 | vermisst · vermisste · hat vermisst | to miss | traurig sein, weil eine Person oder Sache nicht da ist | Ich vermisse meine Familie sehr. — *I miss my family a lot.*<br>Hast du mich vermisst? — *Did you miss me?* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): „nicht mehr da ist“ impliziert fälschlich endgültiges Fehlen; „nicht da ist“ wäre genauer.
- **glm-5p3** (judge kimi-k3): „nicht mehr da ist“ suggeriert dauerhaftes Fehlen; man vermisst jemanden aber auch bei vorübergehender Abwesenheit.
- **kimi-k3** (judge glm-5p3): Definition mit "eine Person oder Sache" ist etwas steif; "jemand oder etwas" wäre natürlicher, und "nicht mehr da" trifft den Sinn genauer als "nicht da".

### 22. mitnehmen (verb)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | (regular) · haben | to take (with you) | jdn / etw. auf einen Weg mit sich nehmen | Kannst du mich ein Stück mit dem Auto mitnehmen? — *Can you give me a ride part of the way?*<br>Ich habe ihn zu einer Party mitgenommen. | |
| deepseek-v4p1-flash | nimmt mit · nahm mit · hat mitgenommen trennbar | to take, to take along | etwas oder jemanden an einen anderen Ort bringen, wenn man selbst dorthin geht | Nimmst du mich zum Bahnhof mit? — *Are you taking me to the station?*<br>Ich habe meinen Schlüssel nicht mitgenommen. — *I didn't take my key with me.* |  |
| glm-5p3 | nimmt mit · nahm mit · hat mitgenommen trennbar | to take along, to bring | eine Person oder eine Sache zu einem anderen Ort begleiten oder tragen | Soll ich noch etwas vom Supermarkt mitnehmen? — *Should I pick anything up from the supermarket?*<br>Nimm deine Jacke mit, es wird kalt. — *Take your jacket with you, it's getting cold.* |  |
| kimi-k3 | nimmt mit · nahm mit · hat mitgenommen trennbar | to take along, to take with | eine Person oder Sache zu einem anderen Ort mitbringen | Nimm doch einen Regenschirm mit, es soll regnen. — *Take an umbrella with you, it's supposed to rain.*<br>Kann ich meinen Hund mitnehmen? — *Can I bring my dog along?* |  |

- **glm-5p3** (judge kimi-k3): 'to bring' suggests the wrong direction (that is 'mitbringen'), and 'begleiten oder tragen' is an awkward, inaccurate definition.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition_de is imprecise ('begleiten/tragen'), and word_en includes 'to bring', which is not the core meaning.
- **kimi-k3** (judge glm-5p3): Die deutsche Definition definiert 'mitnehmen' zirkulär und leicht fehlerhaft über 'mitbringen' (mitbringen = zum Sprecher/Zuhörer bringen, mitnehmen = von dort weg).
- **kimi-k3** (judge deepseek-v4p1-flash): Definition_de uses 'mitbringen', which reverses the direction of 'mitnehmen'.

### 23. weg sein (phrase)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | phrase | to be out cold | ohne Bewusstsein sein | Für einen kurzen Moment war sie weg. — *She was out cold for a brief moment.* | |
| deepseek-v4p1-flash | ist weg · war weg · ist weg gewesen | to be gone, to be away | nicht mehr da; an einem anderen Ort oder nicht mehr vorhanden | Mein Handy ist schon wieder weg. — *My phone is gone again.*<br>Tim war gestern den ganzen Tag weg. — *Tim was away all day yesterday.* |  |
| glm-5p3 | ist weg · war weg · ist weg gewesen | to be away, to be gone | nicht an einem bestimmten Ort sein, weil man woanders ist | Papa ist noch weg, er kommt später. — *Dad's still away, he's coming later.*<br>Mein Handy ist weg – hast du es gesehen? — *My phone is gone – have you seen it?* |  |
| kimi-k3 | ist weg · war weg · ist weg gewesen | to be gone, to be away | nicht mehr an einem Ort oder nicht mehr da sein | Mein Geldbeutel ist weg! — *My wallet is gone!*<br>Sie war das ganze Wochenende weg. — *She was away all weekend.* |  |

- **glm-5p3** (judge kimi-k3): The definition only covers 'away' (a person being elsewhere), but the second example uses the 'gone/lost' sense, which the definition doesn't cover.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition is too narrow: it only describes a person being away, not an object being gone/missing.
- **kimi-k3** (judge glm-5p3): Solide Eintrag; die Definition könnte den 'nicht mehr vorhanden'-Aspekt (verloren/verschwunden) etwas deutlicher machen.

### 24. stehen bleiben (phrase)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | phrase | to stay | nicht anfangen, sich zu bewegen | Egal, was ich machte, der Esel blieb wie angewurzelt stehen. — *Whatever I did, the donkey stayed rooted to the spot.* | |
| deepseek-v4p1-flash | bleibt stehen · blieb stehen · ist stehen geblieben trennbar | to stop, to stand still | sich nicht weiter fortbewegen und an einem Ort Halt machen | Der Bus bleibt an der Haltestelle stehen. — *The bus stops at the bus stop.*<br>Als er mich sah, blieb er stehen. — *When he saw me, he stopped.* |  |
| glm-5p3 | bleibt stehen · blieb stehen · ist stehen geblieben trennbar | to stop, to stand still | nicht weitergehen und an einer Stelle halten | Vor dem Museum sind wir stehen geblieben. — *We stopped in front of the museum.*<br>Bleib doch mal kurz stehen, ich muss etwas sagen. — *Stop for a moment, I need to tell you something.* |  |
| kimi-k3 | bleibt stehen · blieb stehen · ist stehen geblieben trennbar | to stop, to stand still | aufhören zu gehen oder sich zu bewegen | Bleib doch mal stehen, ich muss kurz was sagen. — *Stop for a second, I need to say something.*<br>Das Auto ist mitten auf der Straße stehen geblieben. — *The car stopped in the middle of the road.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Sense ('stop moving') differs from Cambridge's first sense ('not start moving'), but is the more common everyday meaning; definition is slightly formal ('sich fortbewegen', 'Halt machen') for A1–B1.
- **deepseek-v4p1-flash** (judge glm-5p3): Solide, alltagstaugliche Beispiele; die Definition ist korrekt, aber mit 'Halt machen' etwas schwerfällig für A1–B1.
- **glm-5p3** (judge kimi-k3): Sense ('stop moving') differs from Cambridge's first sense ('remain standing'), but it is the most common everyday meaning.
- **glm-5p3** (judge deepseek-v4p1-flash): Chosen sense is 'to stop', while Cambridge's first sense is 'to stay/remain standing'.
- **kimi-k3** (judge glm-5p3): Sehr natürliches, gesprochenes Deutsch in beiden Beispielen; die einfache Definition ist ideal für Lernende.
- **kimi-k3** (judge deepseek-v4p1-flash): Chosen sense is 'to stop', while Cambridge's first sense is 'to stay/remain standing'; 'Das Auto ist ... stehen geblieben' often implies a breakdown.

### 25. verpflichtet sein (phrase)

| source | grammar | word_en | definition_de | examples | failed checks |
|---|---|---|---|---|---|
| Cambridge | phrase | to owe sth |  | Ich bin Ihnen sehr zu Dank verpflichtet! — *I am deeply indebted to you!* | |
| deepseek-v4p1-flash | ist verpflichtet · war verpflichtet · ist verpflichtet gewesen | to be obliged, to be required | etwas tun müssen, weil es eine Regel oder ein Gesetz verlangt | Als Mieter bin ich verpflichtet, die Miete pünktlich zu zahlen. — *As a tenant, I'm obliged to pay the rent on time.*<br>Bist du verpflichtet, das Formular zu unterschreiben? — *Are you required to sign the form?* |  |
| glm-5p3 | ist verpflichtet · war verpflichtet · ist verpflichtet gewesen | to be obliged, to be required | etwas tun müssen, weil es eine Regel oder ein Gesetz ist | Man ist verpflichtet, einen Ausweis mitzunehmen. — *You're required to bring an ID card.*<br>Wir sind verpflichtet, die Rechnung zu bezahlen. — *We're obliged to pay the bill.* |  |
| kimi-k3 | ist verpflichtet · war verpflichtet · ist verpflichtet gewesen | to be obliged, to be required | etwas tun müssen, weil ein Gesetz oder eine Regel es verlangt | Alle Fahrer sind verpflichtet, einen Gurt zu tragen. — *All drivers are required to wear a seatbelt.*<br>Du bist nicht verpflichtet, diese Frage zu beantworten. — *You're not obliged to answer that question.* |  |

- **deepseek-v4p1-flash** (judge kimi-k3): Covers the common 'obliged to do sth' sense, not Cambridge's formal 'jmdm. zu Dank verpflichtet sein' (to owe sth) — but that is the right choice for A1–B1.
- **deepseek-v4p1-flash** (judge glm-5p3): Solid entry; the chosen obligation sense is more useful for learners than Cambridge's 'to owe sth' sense, though it does not match it.
- **glm-5p3** (judge kimi-k3): Same sense mismatch with Cambridge as A (acceptable, as this is the everyday meaning); definition_de 'weil es eine Regel oder ein Gesetz ist' is slightly less precise than 'verlangt'.
- **glm-5p3** (judge deepseek-v4p1-flash): Definition_de is wrong: a rule or law is not the thing one must do.
- **kimi-k3** (judge glm-5p3): Good definitions, but 'einen Gurt zu tragen' is clipped; a native speaker would more likely say 'sich anzuschnallen' or 'einen Sicherheitsgurt zu tragen'.
- **kimi-k3** (judge deepseek-v4p1-flash): Chosen sense is the common 'obliged/required' meaning, not Cambridge's 'indebted/owe' sense.
