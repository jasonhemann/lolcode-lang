# LOLCODE Samples

Example programs demonstrating LOLCODE features, organized by complexity. Every project-based sample can be run with `dotnet run`:

```bash
# From the repo root — build the compiler first:
dotnet build dotnet-lolcode.slnx

# Then run any sample:
dotnet run --project samples/basics/hello-world
dotnet run --project samples/programs/fizzbuzz
dotnet run --project samples/games/arena-game
```

## Basics

Language fundamentals — one concept per sample.

| Sample | Run | Demonstrates |
|--------|-----|-------------|
| [hello-world](basics/hello-world/) | `dotnet run --project samples/basics/hello-world` | Program structure, VISIBLE |
| [variables](basics/variables/) | `dotnet run --project samples/basics/variables` | I HAS A, ITZ, R, types |
| [math](basics/math/) | `dotnet run --project samples/basics/math` | SUM OF, DIFF OF, PRODUKT OF, etc. |
| [conditionals](basics/conditionals/) | `dotnet run --project samples/basics/conditionals` | O RLY?, YA RLY, NO WAI, MEBBE |
| [loops](basics/loops/) | `dotnet run --project samples/basics/loops` | IM IN YR, UPPIN, NERFIN, TIL, WILE |
| [functions](basics/functions/) | `dotnet run --project samples/basics/functions` | HOW IZ I, FOUND YR, IF U SAY SO |
| [string-ops](basics/string-ops/) | `dotnet run --project samples/basics/string-ops` | SMOOSH, string escapes |
| [casting](basics/casting/) | `dotnet run --project samples/basics/casting` | MAEK, IS NOW A |
| [switch](basics/switch/) | `dotnet run --project samples/basics/switch` | WTF?, OMG, OMGWTF |

## Programs

Algorithmic demos combining multiple language features.

| Sample | Run | Demonstrates |
|--------|-----|-------------|
| [fizzbuzz](programs/fizzbuzz/) | `dotnet run --project samples/programs/fizzbuzz` | Loops + conditionals + math |
| [fibonacci](programs/fibonacci/) | `dotnet run --project samples/programs/fibonacci` | Functions + recursion |
| [recursion](programs/recursion/) | `dotnet run --project samples/programs/recursion` | Recursive functions |
| [string-calculator](programs/string-calculator/) | `dotnet run --project samples/programs/string-calculator` | Parsing + switch + functions |

## Games

Interactive programs with user input (`GIMMEH`).

| Sample | Run | Description |
|--------|-----|-------------|
| [guessing-game](games/guessing-game/) | `dotnet run --project samples/games/guessing-game` | Number guessing with I/O, loops, casting |
| [adventure-game](games/adventure-game/) | `dotnet run --project samples/games/adventure-game` | Room-based text adventure (164 lines) |
| [arena-game](games/arena-game/) | `dotnet run --project samples/games/arena-game` | Turn-based RPG battle with 5 enemies (323 lines) |

## File-Based

Single-file programs using `#:sdk Lolcode.NET.Sdk` — no project file needed.

| Sample | Run | Notes |
|--------|-----|-------|
| [hello.lol](file-based/hello.lol) | `dotnet run --file samples/file-based/hello.lol` | Requires SDK NuGet package to be installed |

## For Developers

Sample projects use `Directory.Build.props` to import the LOLCODE SDK directly from the source tree. After building the solution (`dotnet build dotnet-lolcode.slnx`), all samples work immediately — no NuGet packaging needed.

End users would write their `.lolproj` as:
```xml
<Project Sdk="Lolcode.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```
