# 🐱 Lolcode.NET.Templates

Project templates for creating **LOLCODE** .NET applications with `dotnet new`.

## Installation

```bash
dotnet new install Lolcode.NET.Templates
```

## Usage

### Create a new LOLCODE console app

```bash
dotnet new lolcode -n MyApp
cd MyApp
dotnet run
```

This creates a ready-to-run project:

**`MyApp.lolproj`**
```xml
<Project Sdk="Lolcode.NET.Sdk/0.2.0">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```

**`Program.lol`**
```
HAI 1.2
  VISIBLE "HAI WORLD!"
KTHXBYE
```

## LOLCODE Snippets

### Variables and Types

```
HAI 1.2
  I HAS A name ITZ "CEILING CAT"   BTW YARN (string)
  I HAS A age ITZ 9                 BTW NUMBR (integer)
  I HAS A weight ITZ 4.20           BTW NUMBAR (float)
  I HAS A happy ITZ WIN             BTW TROOF (boolean)
  I HAS A nothing                   BTW NOOB (null)

  VISIBLE SMOOSH name AN " IZ " AN age AN " YEARZ OLD" MKAY
KTHXBYE
```

### FizzBuzz

```
HAI 1.2
  IM IN YR fizzbuzz UPPIN YR i TIL BOTH SAEM i AN 101
    I HAS A out ITZ ""
    BOTH SAEM MOD OF i AN 3 AN 0, O RLY?
      YA RLY, out R "Fizz"
    OIC
    BOTH SAEM MOD OF i AN 5 AN 0, O RLY?
      YA RLY, out R SMOOSH out AN "Buzz" MKAY
    OIC
    BOTH SAEM out AN "", O RLY?
      YA RLY, VISIBLE i
      NO WAI, VISIBLE out
    OIC
  IM OUTTA YR fizzbuzz
KTHXBYE
```

### Recursive Functions

```
HAI 1.2
  HOW IZ I factorial YR n
    BOTH SAEM n AN 0
    O RLY?
      YA RLY, FOUND YR 1
    OIC
    FOUND YR PRODUKT OF n AN I IZ factorial YR DIFF OF n AN 1 MKAY
  IF U SAY SO

  VISIBLE I IZ factorial YR 10 MKAY  BTW 3628800
KTHXBYE
```

### User Input

```
HAI 1.2
  VISIBLE "WAT IZ YR NAME?"
  I HAS A name
  GIMMEH name
  VISIBLE SMOOSH "OH HAI " AN name AN "!" MKAY
KTHXBYE
```

### Switch Statement

```
HAI 1.2
  I HAS A color ITZ "RED"
  color, WTF?
    OMG "RED", VISIBLE "FIRE!", GTFO
    OMG "BLU", VISIBLE "WATER!", GTFO
    OMG "GRN", VISIBLE "EARTH!", GTFO
    OMGWTF, VISIBLE "I DUNNO LOL"
  OIC
KTHXBYE
```

## Available Templates

| Template | Short Name | Description |
|----------|-----------|-------------|
| LOLCODE Console App | `lolcode` | Console application with `HAI`/`KTHXBYE` scaffold |

## Requirements

- .NET 10 SDK

## Links

- [GitHub Repository](https://github.com/mattleibow/dotnet-lolcode)
- [Language Specification](https://github.com/mattleibow/dotnet-lolcode/blob/main/docs/LANGUAGE_SPEC.md)
- [Sample Programs](https://github.com/mattleibow/dotnet-lolcode/tree/main/samples)

## License

[MIT](https://github.com/mattleibow/dotnet-lolcode/blob/main/LICENSE)
