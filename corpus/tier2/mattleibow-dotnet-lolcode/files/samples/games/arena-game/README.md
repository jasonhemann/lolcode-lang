# LOLCODE ARENA — Turn-Based Battle Game

A text-based RPG arena game written entirely in LOLCODE, built with the `Lolcode.NET.Sdk`.

## How to Play

```bash
# From the repository root:
dotnet build dotnet-lolcode.slnx

# Then run the game:
cd samples/games/arena-game
dotnet run
```

## Gameplay

Fight through 5 increasingly tough enemies to become the Arena Champion!

| # | Enemy | HP | ATK | DEF |
|---|-------|-----|-----|-----|
| 1 | ANGRY KITTEH | 30 | 8 | 2 |
| 2 | TROLLFACE | 50 | 12 | 4 |
| 3 | SPAM BOT | 70 | 15 | 6 |
| 4 | 404 DRAGON | 100 | 20 | 8 |
| 5 | CEILIN CAT | 150 | 25 | 10 |

### Actions

| Command | Effect |
|---------|--------|
| `attack` | Deal (ATK - enemy DEF) damage, enemy counter-attacks |
| `defend` | Enemy deals half damage this turn |
| `heal` | Use a potion (+30 HP), enemy still attacks |
| `flee` | Forfeit the match |

### Tips

- You start with **100 HP**, **3 potions**, **15 ATK**, **5 DEF**
- HP carries between fights — ration your potions!
- You recover **10 HP** after each victory
- Defending halves incoming damage — use it against hard hitters

## LOLCODE Features Demonstrated

| Feature | Usage |
|---------|-------|
| `HOW IZ I` / `IF U SAY SO` | Functions for damage calc, HP display, enemy stats |
| `IM IN YR` / `IM OUTTA YR` | Arena loop (5 rounds) and battle loop |
| `WTF?` / `OMG` / `OMGWTF` | Enemy stat lookup by round number |
| `O RLY?` / `YA RLY` / `NO WAI` | Win/lose checks, action handling |
| `BOTH SAEM` / `DIFFRINT` | Comparisons for HP, round, action matching |
| `SUM OF` / `DIFF OF` / `PRODUKT OF` / `QUOSHUNT OF` | Damage and healing math |
| `BIGGR OF` / `SMALLR OF` | HP clamping (0 ≤ HP ≤ max) |
| `SMOOSH` | String concatenation for HP bars |
| `VISIBLE` (infinite arity) | Status display, battle narration |
| `GIMMEH` | Player name and action input |
| `GTFO` | Breaking from battle/arena loops |
| `IT` | Implicit variable in conditionals |
| `FOUND YR` | Function return values |
