# File-Based Hello World

A minimal LOLCODE program that runs without a `.lolproj` file, using .NET 10's file-based app support.

## Usage

```bash
dotnet run --file hello.lol
# Or:
dotnet hello.lol
```

## How It Works

The `#:sdk Lolcode.NET.Sdk` directive at the top tells the .NET SDK to use the LOLCODE compiler. No project file needed (when the SDK is installed from NuGet).

For local development, build the compiler first:
```bash
cd /path/to/dotnet-lolcode
dotnet build dotnet-lolcode.slnx
```

> **Note:** File-based apps use NuGet to resolve the `#:sdk` directive, so local testing
> requires the SDK to be published as a NuGet package. For development, use the project-based
> samples (`samples/basics/hello-world/`) which work directly from the source tree.
