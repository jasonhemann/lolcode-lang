# 🐱 Lolcode.NET.Sdk

MSBuild SDK for compiling **LOLCODE 1.2** programs to .NET assemblies. Write `.lol` files, build with `dotnet build`, run with `dotnet run`.

## Quick Start

### Create a project from template

```bash
dotnet new install Lolcode.NET.Templates
dotnet new lolcode -n MyApp
cd MyApp
dotnet run
```

### Manual project setup

Create a `MyApp.lolproj`:

```xml
<Project Sdk="Lolcode.NET.Sdk/0.2.0">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```

Create a `Program.lol`:

```
HAI 1.2
  VISIBLE "HAI WORLD!"
KTHXBYE
```

Build and run:

```bash
dotnet build    # Compiles .lol → .dll
dotnet run      # Compile and execute
dotnet watch    # Recompile on changes
dotnet publish  # Publish for deployment
```

### File-based apps (no project needed)

Create `hello.lol` — no project file required:

```
#:sdk Lolcode.NET.Sdk/0.2.0
HAI 1.2
  VISIBLE "HAI WORLD!"
KTHXBYE
```

```bash
dotnet run --file hello.lol
# Or even shorter:
dotnet hello.lol
```

## Language Features

Full LOLCODE 1.2 support:

```
HAI 1.2
  BTW Variables and types
  I HAS A name ITZ "LOLCODE"
  I HAS A count ITZ 42
  I HAS A pi ITZ 3.14
  I HAS A cool ITZ WIN

  BTW Math
  VISIBLE SUM OF count AN 8          BTW 50
  VISIBLE PRODUKT OF count AN 2      BTW 84

  BTW String concatenation
  VISIBLE SMOOSH "HAI " AN name AN "!" MKAY

  BTW Conditionals
  BOTH SAEM count AN 42, O RLY?
    YA RLY, VISIBLE "IT IZ 42!"
    NO WAI, VISIBLE "IT IZ NOT 42"
  OIC

  BTW Loops
  IM IN YR loop UPPIN YR i TIL BOTH SAEM i AN 5
    VISIBLE SMOOSH "COUNT: " AN i MKAY
  IM OUTTA YR loop

  BTW Functions
  HOW IZ I greet YR who
    FOUND YR SMOOSH "OH HAI " AN who AN "!" MKAY
  IF U SAY SO

  VISIBLE I IZ greet YR "WORLD" MKAY
KTHXBYE
```

## What's Included

The SDK package contains:
- **LOLCODE compiler** — full lexer → parser → binder → lowerer → code generator pipeline
- **MSBuild integration** — `Sdk.props` and `Sdk.targets` for seamless `dotnet` CLI experience
- **Runtime library** — automatically referenced for compiled programs

## Requirements

- .NET 10 SDK

## Links

- [GitHub Repository](https://github.com/mattleibow/dotnet-lolcode)
- [Language Specification](https://github.com/mattleibow/dotnet-lolcode/blob/main/docs/LANGUAGE_SPEC.md)
- [Sample Programs](https://github.com/mattleibow/dotnet-lolcode/tree/main/samples)

## License

[MIT](https://github.com/mattleibow/dotnet-lolcode/blob/main/LICENSE)
