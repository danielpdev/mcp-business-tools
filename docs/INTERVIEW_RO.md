# Pregătire pentru interviu — MCP Business Tools

Roluri țintă: MCP / Agent Integration / Python.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: The MCP server exposes inventory reads and order preparation. Capability scopes come from the server process, never from tool arguments. Stock is committed only through a separate operator approval surface.

## Cinci întrebări

1. De unde vin permisiunile MCP?
2. De ce aprobarea nu este un tool al agentului?
3. Cum validezi tipurile?
4. Ce se întâmplă dacă stocul se schimbă?
5. Cum ai expune sigur serverul prin HTTP?

## Exercițiu înainte de a aplica

Add per-user authentication and reservation expiry without letting the model grant itself scopes.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
