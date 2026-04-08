using System.Collections.Immutable;
using System.Diagnostics.SymbolStore;
using System.Reflection;
using System.Reflection.Emit;
using System.Reflection.Metadata;
using System.Reflection.Metadata.Ecma335;
using System.Reflection.PortableExecutable;
using System.Security.Cryptography;
using Lolcode.CodeAnalysis.Binding;
using Lolcode.CodeAnalysis.BoundTree;
using Lolcode.CodeAnalysis.Syntax;
using Lolcode.CodeAnalysis.Text;

namespace Lolcode.CodeAnalysis.CodeGen;

/// <summary>
/// Generates a .NET assembly from a bound tree using PersistedAssemblyBuilder.
/// All LOLCODE variables are emitted as <see cref="object"/> locals.
/// Runtime calls go through <c>Lolcode.Runtime.LolRuntime</c>.
/// </summary>
internal sealed class CodeGenerator
{
    private readonly BoundBlockStatement _boundTree;
    private readonly string _assemblyName;
    private readonly string _runtimeAssemblyPath;
    private readonly Text.SourceText? _sourceText;
    private readonly string? _sourceFilePath;
    private ISymbolDocumentWriter? _document;

    private TypeBuilder _typeBuilder = null!;
    private ILGenerator _il = null!;
    private readonly Dictionary<string, LocalBuilder> _locals = new(StringComparer.Ordinal);
    private readonly Dictionary<string, MethodBuilder> _methods = new(StringComparer.Ordinal);
    private readonly Dictionary<string, BoundFunctionDeclaration> _functionBodies = new(StringComparer.Ordinal);

    // Labels for break (GTFO) support
    private readonly Stack<Label> _loopBreakLabels = new();
    private readonly Stack<Label> _switchBreakLabels = new();
    private Label _functionReturnLabel;
    private LocalBuilder? _functionReturnValue;

    // Runtime method references
    private MethodInfo _printMethod = null!;
    private MethodInfo _readLineMethod = null!;
    private MethodInfo _addMethod = null!;
    private MethodInfo _subtractMethod = null!;
    private MethodInfo _multiplyMethod = null!;
    private MethodInfo _divideMethod = null!;
    private MethodInfo _moduloMethod = null!;
    private MethodInfo _greaterMethod = null!;
    private MethodInfo _smallerMethod = null!;
    private MethodInfo _andMethod = null!;
    private MethodInfo _orMethod = null!;
    private MethodInfo _xorMethod = null!;
    private MethodInfo _notMethod = null!;
    private MethodInfo _bothSaemMethod = null!;
    private MethodInfo _diffrintMethod = null!;
    private MethodInfo _smooshMethod = null!;
    private MethodInfo _isTruthyMethod = null!;
    private MethodInfo _castToYarnMethod = null!;
    private MethodInfo _castToNumbrMethod = null!;
    private MethodInfo _castToNumbarMethod = null!;
    private MethodInfo _castToTroofMethod = null!;
    private MethodInfo _explicitCastMethod = null!;

    /// <summary>
    /// Creates a new emitter.
    /// </summary>
    public CodeGenerator(BoundBlockStatement boundTree, string assemblyName, string runtimeAssemblyPath,
        Text.SourceText? sourceText = null, string? sourceFilePath = null)
    {
        _boundTree = boundTree;
        _assemblyName = assemblyName;
        _runtimeAssemblyPath = runtimeAssemblyPath;
        _sourceText = sourceText;
        _sourceFilePath = sourceFilePath;
    }

    /// <summary>
    /// Emits the assembly to the specified output path.
    /// </summary>
    /// <returns>The path to the emitted DLL.</returns>
    public string Emit(string outputPath)
    {
        var runtimeAssembly = Assembly.LoadFrom(_runtimeAssemblyPath);
        var runtimeType = runtimeAssembly.GetType("Lolcode.Runtime.LolRuntime")
            ?? throw new InvalidOperationException("Could not find LolRuntime type");

        ResolveRuntimeMethods(runtimeType);

        var assemblyBuilder = new PersistedAssemblyBuilder(
            new AssemblyName(_assemblyName),
            typeof(object).Assembly);

        var moduleBuilder = assemblyBuilder.DefineDynamicModule(_assemblyName);

        // PDB: define document for source file
        if (_sourceText != null && !string.IsNullOrEmpty(_sourceFilePath))
        {
            var lolcodeLanguageGuid = new Guid("4C4F4C43-4F44-4500-0000-000000000001");
            _document = moduleBuilder.DefineDocument(
                Path.GetFullPath(_sourceFilePath), lolcodeLanguageGuid,
                SymLanguageVendor.Microsoft, SymDocumentType.Text);
        }

        _typeBuilder = moduleBuilder.DefineType(
            "Program",
            TypeAttributes.Public | TypeAttributes.Class | TypeAttributes.Abstract | TypeAttributes.Sealed);

        // First pass: define all function methods
        foreach (var statement in _boundTree.Statements)
        {
            if (statement is BoundFunctionDeclaration funcDecl)
            {
                var paramTypes = new Type[funcDecl.Function.Parameters.Length];
                Array.Fill(paramTypes, typeof(object));

                var method = _typeBuilder.DefineMethod(
                    funcDecl.Function.Name,
                    MethodAttributes.Public | MethodAttributes.Static,
                    typeof(object),
                    paramTypes);

                for (int i = 0; i < funcDecl.Function.Parameters.Length; i++)
                    method.DefineParameter(i + 1, ParameterAttributes.None, funcDecl.Function.Parameters[i].Name);

                _methods[funcDecl.Function.Name] = method;
                _functionBodies[funcDecl.Function.Name] = funcDecl;
            }
        }

        // Define Main entry point
        var mainMethod = _typeBuilder.DefineMethod(
            "Main",
            MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
            typeof(void),
            Type.EmptyTypes);

        // Emit function bodies
        foreach (var kv in _functionBodies)
        {
            EmitFunction(kv.Key, kv.Value);
        }

        // Emit Main body
        _il = mainMethod.GetILGenerator();
        _locals.Clear();

        _il.BeginScope();

        // Declare IT
        var itLocal = _il.DeclareLocal(typeof(object));
        _locals["IT"] = itLocal;
        SetLocalSymInfo(itLocal, "IT");
        _il.Emit(OpCodes.Ldnull);
        _il.Emit(OpCodes.Stloc, itLocal);

        foreach (var statement in _boundTree.Statements)
        {
            if (statement is not BoundFunctionDeclaration)
                EmitStatement(statement);
        }

        _il.EndScope();
        _il.Emit(OpCodes.Ret);

        _typeBuilder.CreateType();

        // Save assembly with PDB
        var dllPath = outputPath.EndsWith(".dll", StringComparison.OrdinalIgnoreCase)
            ? outputPath
            : Path.ChangeExtension(outputPath, ".dll");
        Directory.CreateDirectory(Path.GetDirectoryName(dllPath) ?? ".");

        var metadataBuilder = assemblyBuilder.GenerateMetadata(out var ilStream, out var mappedFieldData, out MetadataBuilder pdbBuilder);
        var entryPointHandle = MetadataTokens.MethodDefinitionHandle(mainMethod.MetadataToken);

        string? pdbPath = null;

        if (_document != null)
        {
            try
            {
                pdbPath = Path.ChangeExtension(dllPath, ".pdb");

                // Serialize PDB first (need BlobContentId for PE debug directory)
                var portablePdbBlob = new BlobBuilder();
                var portablePdbBuilder = new PortablePdbBuilder(
                    pdbBuilder, metadataBuilder.GetRowCounts(), entryPointHandle,
                    idProvider: content =>
                    {
                        using var hasher = IncrementalHash.CreateHash(HashAlgorithmName.SHA256);
                        foreach (var blob in content)
                            hasher.AppendData(blob.GetBytes().Array!, blob.GetBytes().Offset, blob.GetBytes().Count);
                        return BlobContentId.FromHash(hasher.GetHashAndReset());
                    });
                BlobContentId pdbContentId = portablePdbBuilder.Serialize(portablePdbBlob);

                using (var pdbStream = File.Create(pdbPath))
                    portablePdbBlob.WriteContentTo(pdbStream);

                // Build PE with debug info
                var debugDirectoryBuilder = new DebugDirectoryBuilder();
                debugDirectoryBuilder.AddCodeViewEntry(
                    Path.GetFileName(pdbPath), pdbContentId, portablePdbBuilder.FormatVersion);

                var peBuilder = new ManagedPEBuilder(
                    header: new PEHeaderBuilder(
                        imageCharacteristics: Characteristics.ExecutableImage,
                        subsystem: Subsystem.WindowsCui),
                    metadataRootBuilder: new MetadataRootBuilder(metadataBuilder),
                    ilStream: ilStream,
                    mappedFieldData: mappedFieldData,
                    debugDirectoryBuilder: debugDirectoryBuilder,
                    entryPoint: entryPointHandle);

                var peBlob = new BlobBuilder();
                peBuilder.Serialize(peBlob);

                using (var fs = new FileStream(dllPath, FileMode.Create, FileAccess.Write))
                    peBlob.WriteContentTo(fs);
            }
            catch
            {
                // PDB failed — fall back to DLL without debug info
                pdbPath = null;
                var peBuilder = new ManagedPEBuilder(
                    header: new PEHeaderBuilder(
                        imageCharacteristics: Characteristics.ExecutableImage,
                        subsystem: Subsystem.WindowsCui),
                    metadataRootBuilder: new MetadataRootBuilder(metadataBuilder),
                    ilStream: ilStream,
                    mappedFieldData: mappedFieldData,
                    entryPoint: entryPointHandle);

                var peBlob = new BlobBuilder();
                peBuilder.Serialize(peBlob);

                using (var fs = new FileStream(dllPath, FileMode.Create, FileAccess.Write))
                    peBlob.WriteContentTo(fs);
            }
        }
        else
        {
            // No PDB requested — emit without debug info
            var peBuilder = new ManagedPEBuilder(
                header: new PEHeaderBuilder(
                    imageCharacteristics: Characteristics.ExecutableImage,
                    subsystem: Subsystem.WindowsCui),
                metadataRootBuilder: new MetadataRootBuilder(metadataBuilder),
                ilStream: ilStream,
                mappedFieldData: mappedFieldData,
                entryPoint: entryPointHandle);

            var peBlob = new BlobBuilder();
            peBuilder.Serialize(peBlob);

            using (var fs = new FileStream(dllPath, FileMode.Create, FileAccess.Write))
                peBlob.WriteContentTo(fs);
        }

        // Also write runtime config
        WriteRuntimeConfig(dllPath);

        return dllPath;
    }

    private void ResolveRuntimeMethods(Type runtimeType)
    {
        _printMethod = runtimeType.GetMethod("Print")!;
        _readLineMethod = runtimeType.GetMethod("ReadLine")!;
        _addMethod = runtimeType.GetMethod("Add")!;
        _subtractMethod = runtimeType.GetMethod("Subtract")!;
        _multiplyMethod = runtimeType.GetMethod("Multiply")!;
        _divideMethod = runtimeType.GetMethod("Divide")!;
        _moduloMethod = runtimeType.GetMethod("Modulo")!;
        _greaterMethod = runtimeType.GetMethod("Greater")!;
        _smallerMethod = runtimeType.GetMethod("Smaller")!;
        _andMethod = runtimeType.GetMethod("And")!;
        _orMethod = runtimeType.GetMethod("Or")!;
        _xorMethod = runtimeType.GetMethod("Xor")!;
        _notMethod = runtimeType.GetMethod("Not")!;
        _bothSaemMethod = runtimeType.GetMethod("BothSaem")!;
        _diffrintMethod = runtimeType.GetMethod("Diffrint")!;
        _smooshMethod = runtimeType.GetMethod("Smoosh")!;
        _isTruthyMethod = runtimeType.GetMethod("IsTruthy")!;
        _castToYarnMethod = runtimeType.GetMethod("CastToYarn")!;
        _castToNumbrMethod = runtimeType.GetMethod("CastToNumbr")!;
        _castToNumbarMethod = runtimeType.GetMethod("CastToNumbar")!;
        _castToTroofMethod = runtimeType.GetMethod("CastToTroof")!;
        _explicitCastMethod = runtimeType.GetMethod("ExplicitCast")!;
    }

    private void EmitFunction(string name, BoundFunctionDeclaration decl)
    {
        var method = _methods[name];
        _il = method.GetILGenerator();
        _locals.Clear();

        _il.BeginScope();
        EmitSequencePoint(decl);

        // IT variable for this function
        var itLocal = _il.DeclareLocal(typeof(object));
        _locals["IT"] = itLocal;
        SetLocalSymInfo(itLocal, "IT");
        _il.Emit(OpCodes.Ldnull);
        _il.Emit(OpCodes.Stloc, itLocal);

        // Parameters are accessible by name
        for (int i = 0; i < decl.Function.Parameters.Length; i++)
        {
            var local = _il.DeclareLocal(typeof(object));
            _locals[decl.Function.Parameters[i].Name] = local;
            SetLocalSymInfo(local, decl.Function.Parameters[i].Name);
            _il.Emit(OpCodes.Ldarg, i);
            _il.Emit(OpCodes.Stloc, local);
        }

        // Return handling
        _functionReturnLabel = _il.DefineLabel();
        _functionReturnValue = _il.DeclareLocal(typeof(object));
        _il.Emit(OpCodes.Ldnull);
        _il.Emit(OpCodes.Stloc, _functionReturnValue);

        foreach (var statement in decl.Body.Statements)
            EmitStatement(statement);

        // If no FOUND YR was executed, return IT by default
        _il.EndScope();
        EmitLoadLocal("IT");
        _il.Emit(OpCodes.Stloc, _functionReturnValue);

        _il.MarkLabel(_functionReturnLabel);
        _il.Emit(OpCodes.Ldloc, _functionReturnValue);
        _il.Emit(OpCodes.Ret);
    }

    private void EmitStatement(BoundStatement statement)
    {
        switch (statement)
        {
            case BoundVariableDeclaration s:
                EmitSequencePoint(s);
                EmitVariableDeclaration(s);
                break;
            case BoundAssignment s:
                EmitSequencePoint(s);
                EmitAssignment(s);
                break;
            case BoundVisibleStatement s:
                EmitSequencePoint(s);
                EmitVisible(s);
                break;
            case BoundGimmehStatement s:
                EmitSequencePoint(s);
                EmitGimmeh(s);
                break;
            case BoundExpressionStatement s:
                EmitSequencePoint(s);
                EmitExpressionStatement(s);
                break;
            case BoundIfStatement s:
                if (s.Syntax is IfStatementSyntax ifSyntax)
                    EmitSequencePointForToken(ifSyntax.ORlyKeyword);
                EmitIf(s);
                break;
            case BoundSwitchStatement s:
                if (s.Syntax is SwitchStatementSyntax switchSyntax)
                    EmitSequencePointForToken(switchSyntax.WtfKeyword);
                EmitSwitch(s);
                break;
            case BoundLoopStatement s:
                if (s.Syntax is LoopStatementSyntax loopSyntax)
                    EmitSequencePointForToken(loopSyntax.ImInKeyword);
                EmitLoop(s);
                break;
            case BoundGtfoStatement s:
                EmitSequencePoint(s);
                EmitGtfo(s);
                break;
            case BoundReturnStatement s:
                EmitSequencePoint(s);
                EmitReturn(s);
                break;
            case BoundCastStatement s:
                EmitSequencePoint(s);
                EmitCastStatement(s);
                break;
            case BoundFunctionDeclaration:
                // Already handled in first pass
                break;
        }
    }

    private void EmitVariableDeclaration(BoundVariableDeclaration decl)
    {
        var local = _il.DeclareLocal(typeof(object));
        _locals[decl.Variable.Name] = local;
        SetLocalSymInfo(local, decl.Variable.Name);

        if (decl.Initializer != null)
        {
            EmitExpression(decl.Initializer);
        }
        else
        {
            _il.Emit(OpCodes.Ldnull); // NOOB
        }

        _il.Emit(OpCodes.Stloc, local);
    }

    private void EmitAssignment(BoundAssignment assignment)
    {
        EmitExpression(assignment.Expression);

        if (_locals.TryGetValue(assignment.Variable.Name, out var local))
        {
            _il.Emit(OpCodes.Stloc, local);
        }
    }

    private void EmitVisible(BoundVisibleStatement visible)
    {
        _il.Emit(OpCodes.Ldc_I4, visible.Arguments.Length);
        _il.Emit(OpCodes.Newarr, typeof(object));

        for (int i = 0; i < visible.Arguments.Length; i++)
        {
            _il.Emit(OpCodes.Dup);
            _il.Emit(OpCodes.Ldc_I4, i);
            EmitExpression(visible.Arguments[i]);
            _il.Emit(OpCodes.Stelem_Ref);
        }

        _il.Emit(visible.SuppressNewline ? OpCodes.Ldc_I4_1 : OpCodes.Ldc_I4_0);
        _il.Emit(OpCodes.Call, _printMethod);
    }

    private void EmitGimmeh(BoundGimmehStatement gimmeh)
    {
        _il.Emit(OpCodes.Call, _readLineMethod);

        if (_locals.TryGetValue(gimmeh.Variable.Name, out var local))
        {
            _il.Emit(OpCodes.Stloc, local);
        }
    }

    private void EmitExpressionStatement(BoundExpressionStatement exprStmt)
    {
        EmitExpression(exprStmt.Expression);
        if (_locals.TryGetValue("IT", out var itLocal))
        {
            _il.Emit(OpCodes.Stloc, itLocal);
        }
        else
        {
            _il.Emit(OpCodes.Pop);
        }
    }

    private void EmitIf(BoundIfStatement ifStmt)
    {
        var endLabel = _il.DefineLabel();

        EmitLoadLocal("IT");
        _il.Emit(OpCodes.Call, _isTruthyMethod);
        var yaRlyFalse = _il.DefineLabel();
        _il.Emit(OpCodes.Brfalse, yaRlyFalse);

        EmitBlock(ifStmt.ThenBlock);
        _il.Emit(OpCodes.Br, endLabel);

        _il.MarkLabel(yaRlyFalse);

        for (int i = 0; i < ifStmt.MebbeClauses.Length; i++)
        {
            var clause = ifStmt.MebbeClauses[i];
            EmitExpression(clause.Condition);
            _il.Emit(OpCodes.Call, _isTruthyMethod);
            var nextClause = _il.DefineLabel();
            _il.Emit(OpCodes.Brfalse, nextClause);

            EmitBlock(clause.Body);
            _il.Emit(OpCodes.Br, endLabel);

            _il.MarkLabel(nextClause);
        }

        if (ifStmt.ElseBlock != null)
        {
            EmitBlock(ifStmt.ElseBlock);
        }

        _il.MarkLabel(endLabel);
    }

    private void EmitSwitch(BoundSwitchStatement switchStmt)
    {
        var endLabel = _il.DefineLabel();
        _switchBreakLabels.Push(endLabel);

        var matched = _il.DeclareLocal(typeof(bool));
        _il.Emit(OpCodes.Ldc_I4_0);
        _il.Emit(OpCodes.Stloc, matched);

        foreach (var clause in switchStmt.OmgClauses)
        {
            var skipBody = _il.DefineLabel();
            var enterBody = _il.DefineLabel();

            _il.Emit(OpCodes.Ldloc, matched);
            _il.Emit(OpCodes.Brtrue, enterBody);

            EmitLoadLocal("IT");
            EmitLiteralValue(clause.LiteralValue);
            _il.Emit(OpCodes.Call, _bothSaemMethod);
            _il.Emit(OpCodes.Brfalse, skipBody);

            _il.MarkLabel(enterBody);
            _il.Emit(OpCodes.Ldc_I4_1);
            _il.Emit(OpCodes.Stloc, matched);

            EmitBlock(clause.Body);

            _il.MarkLabel(skipBody);
        }

        if (switchStmt.DefaultBlock != null)
        {
            var skipDefault = _il.DefineLabel();
            _il.Emit(OpCodes.Ldloc, matched);
            _il.Emit(OpCodes.Brtrue, skipDefault);

            EmitBlock(switchStmt.DefaultBlock);

            _il.MarkLabel(skipDefault);
        }

        _il.MarkLabel(endLabel);
        _switchBreakLabels.Pop();
    }

    private void EmitLoop(BoundLoopStatement loop)
    {
        var loopStart = _il.DefineLabel();
        var loopEnd = _il.DefineLabel();
        _loopBreakLabels.Push(loopEnd);

        // Loop variable is ALWAYS local to the loop (per spec)
        LocalBuilder? savedLocal = null;
        string? varName = loop.Variable?.Name;
        if (varName != null)
        {
            _locals.TryGetValue(varName, out savedLocal);
            var loopVar = _il.DeclareLocal(typeof(object));
            _locals[varName] = loopVar;
            _il.Emit(OpCodes.Ldc_I4_0);
            _il.Emit(OpCodes.Box, typeof(int));
            _il.Emit(OpCodes.Stloc, loopVar);
        }

        _il.MarkLabel(loopStart);

        if (loop.Condition != null)
        {
            EmitExpression(loop.Condition);
            _il.Emit(OpCodes.Call, _isTruthyMethod);

            if (loop.IsTil == true)
                _il.Emit(OpCodes.Brtrue, loopEnd);
            else
                _il.Emit(OpCodes.Brfalse, loopEnd);
        }

        EmitBlock(loop.Body);

        // Increment/decrement loop variable
        if (varName != null && loop.Operation != null)
        {
            if (loop.Operation == "UPPIN")
            {
                EmitLoadLocal(varName);
                EmitLiteralValue(1);
                _il.Emit(OpCodes.Call, _addMethod);
                EmitStoreLocal(varName);
            }
            else if (loop.Operation == "NERFIN")
            {
                EmitLoadLocal(varName);
                EmitLiteralValue(1);
                _il.Emit(OpCodes.Call, _subtractMethod);
                EmitStoreLocal(varName);
            }
        }

        _il.Emit(OpCodes.Br, loopStart);
        _il.MarkLabel(loopEnd);

        _loopBreakLabels.Pop();

        // Restore the previous variable binding
        if (varName != null)
        {
            if (savedLocal != null)
                _locals[varName] = savedLocal;
            else
                _locals.Remove(varName);
        }
    }

    private void EmitGtfo(BoundGtfoStatement gtfo)
    {
        switch (gtfo.Context)
        {
            case ControlFlowContext.Loop when _loopBreakLabels.Count > 0:
                _il.Emit(OpCodes.Br, _loopBreakLabels.Peek());
                break;
            case ControlFlowContext.Switch when _switchBreakLabels.Count > 0:
                _il.Emit(OpCodes.Br, _switchBreakLabels.Peek());
                break;
            case ControlFlowContext.Function:
                if (_functionReturnValue != null)
                {
                    _il.Emit(OpCodes.Ldnull);
                    _il.Emit(OpCodes.Stloc, _functionReturnValue);
                }
                _il.Emit(OpCodes.Br, _functionReturnLabel);
                break;
        }
    }

    private void EmitReturn(BoundReturnStatement ret)
    {
        EmitExpression(ret.Expression);
        if (_functionReturnValue != null)
        {
            _il.Emit(OpCodes.Stloc, _functionReturnValue);
        }
        _il.Emit(OpCodes.Br, _functionReturnLabel);
    }

    private void EmitCastStatement(BoundCastStatement cast)
    {
        EmitLoadLocal(cast.Variable.Name);
        _il.Emit(OpCodes.Ldstr, cast.TargetType);
        _il.Emit(OpCodes.Call, _explicitCastMethod);
        EmitStoreLocal(cast.Variable.Name);
    }

    private void EmitBlock(BoundBlockStatement block)
    {
        foreach (var statement in block.Statements)
            EmitStatement(statement);
    }

    private void EmitExpression(BoundExpression expression)
    {
        switch (expression)
        {
            case BoundLiteralExpression e:
                EmitLiteralValue(e.Value);
                break;
            case BoundVariableExpression e:
                EmitLoadLocal(e.Variable.Name);
                break;
            case BoundItExpression:
                EmitLoadLocal("IT");
                break;
            case BoundUnaryExpression e:
                EmitExpression(e.Operand);
                _il.Emit(OpCodes.Call, _notMethod);
                _il.Emit(OpCodes.Box, typeof(bool));
                break;
            case BoundBinaryExpression e:
                EmitBinary(e);
                break;
            case BoundSmooshExpression e:
                EmitSmoosh(e);
                break;
            case BoundAllOfExpression e:
                EmitAllOf(e);
                break;
            case BoundAnyOfExpression e:
                EmitAnyOf(e);
                break;
            case BoundComparisonExpression e:
                EmitComparison(e);
                break;
            case BoundCastExpression e:
                EmitCast(e);
                break;
            case BoundFunctionCallExpression e:
                EmitFunctionCall(e);
                break;
        }
    }

    private void EmitLiteralValue(object? value)
    {
        switch (value)
        {
            case null:
                _il.Emit(OpCodes.Ldnull);
                break;
            case int i:
                _il.Emit(OpCodes.Ldc_I4, i);
                _il.Emit(OpCodes.Box, typeof(int));
                break;
            case double d:
                _il.Emit(OpCodes.Ldc_R8, d);
                _il.Emit(OpCodes.Box, typeof(double));
                break;
            case string s:
                _il.Emit(OpCodes.Ldstr, s);
                break;
            case bool b:
                _il.Emit(b ? OpCodes.Ldc_I4_1 : OpCodes.Ldc_I4_0);
                _il.Emit(OpCodes.Box, typeof(bool));
                break;
        }
    }

    private void EmitBinary(BoundBinaryExpression binary)
    {
        EmitExpression(binary.Left);
        EmitExpression(binary.Right);

        MethodInfo method = binary.OperatorKind switch
        {
            BoundBinaryOperatorKind.Addition => _addMethod,
            BoundBinaryOperatorKind.Subtraction => _subtractMethod,
            BoundBinaryOperatorKind.Multiplication => _multiplyMethod,
            BoundBinaryOperatorKind.Division => _divideMethod,
            BoundBinaryOperatorKind.Modulo => _moduloMethod,
            BoundBinaryOperatorKind.Maximum => _greaterMethod,
            BoundBinaryOperatorKind.Minimum => _smallerMethod,
            BoundBinaryOperatorKind.LogicalAnd => _andMethod,
            BoundBinaryOperatorKind.LogicalOr => _orMethod,
            BoundBinaryOperatorKind.LogicalXor => _xorMethod,
            _ => throw new InvalidOperationException($"Unknown operator kind: {binary.OperatorKind}")
        };

        _il.Emit(OpCodes.Call, method);

        // Boolean operators return bool, need to box
        if (binary.OperatorKind is BoundBinaryOperatorKind.LogicalAnd
            or BoundBinaryOperatorKind.LogicalOr
            or BoundBinaryOperatorKind.LogicalXor)
        {
            _il.Emit(OpCodes.Box, typeof(bool));
        }
    }

    private void EmitSmoosh(BoundSmooshExpression smoosh)
    {
        _il.Emit(OpCodes.Ldc_I4, smoosh.Operands.Length);
        _il.Emit(OpCodes.Newarr, typeof(object));

        for (int i = 0; i < smoosh.Operands.Length; i++)
        {
            _il.Emit(OpCodes.Dup);
            _il.Emit(OpCodes.Ldc_I4, i);
            EmitExpression(smoosh.Operands[i]);
            _il.Emit(OpCodes.Stelem_Ref);
        }

        _il.Emit(OpCodes.Call, _smooshMethod);
    }

    private void EmitAllOf(BoundAllOfExpression allOf)
    {
        var falseLabel = _il.DefineLabel();
        var endLabel = _il.DefineLabel();

        foreach (var operand in allOf.Operands)
        {
            EmitExpression(operand);
            _il.Emit(OpCodes.Call, _isTruthyMethod);
            _il.Emit(OpCodes.Brfalse, falseLabel);
        }

        _il.Emit(OpCodes.Ldc_I4_1);
        _il.Emit(OpCodes.Br, endLabel);

        _il.MarkLabel(falseLabel);
        _il.Emit(OpCodes.Ldc_I4_0);

        _il.MarkLabel(endLabel);
        _il.Emit(OpCodes.Box, typeof(bool));
    }

    private void EmitAnyOf(BoundAnyOfExpression anyOf)
    {
        var trueLabel = _il.DefineLabel();
        var endLabel = _il.DefineLabel();

        foreach (var operand in anyOf.Operands)
        {
            EmitExpression(operand);
            _il.Emit(OpCodes.Call, _isTruthyMethod);
            _il.Emit(OpCodes.Brtrue, trueLabel);
        }

        _il.Emit(OpCodes.Ldc_I4_0);
        _il.Emit(OpCodes.Br, endLabel);

        _il.MarkLabel(trueLabel);
        _il.Emit(OpCodes.Ldc_I4_1);

        _il.MarkLabel(endLabel);
        _il.Emit(OpCodes.Box, typeof(bool));
    }

    private void EmitComparison(BoundComparisonExpression cmp)
    {
        EmitExpression(cmp.Left);
        EmitExpression(cmp.Right);

        if (cmp.IsEquality)
            _il.Emit(OpCodes.Call, _bothSaemMethod);
        else
            _il.Emit(OpCodes.Call, _diffrintMethod);

        _il.Emit(OpCodes.Box, typeof(bool));
    }

    private void EmitCast(BoundCastExpression cast)
    {
        EmitExpression(cast.Operand);
        _il.Emit(OpCodes.Ldstr, cast.TargetType);
        _il.Emit(OpCodes.Call, _explicitCastMethod);
    }

    private void EmitFunctionCall(BoundFunctionCallExpression call)
    {
        foreach (var arg in call.Arguments)
        {
            EmitExpression(arg);
        }

        if (_methods.TryGetValue(call.Function.Name, out var method))
        {
            _il.Emit(OpCodes.Call, method);
        }
    }

    private void EmitLoadLocal(string name)
    {
        if (_locals.TryGetValue(name, out var local))
        {
            _il.Emit(OpCodes.Ldloc, local);
        }
        else
        {
            _il.Emit(OpCodes.Ldnull);
        }
    }

    private void EmitStoreLocal(string name)
    {
        if (_locals.TryGetValue(name, out var local))
        {
            _il.Emit(OpCodes.Stloc, local);
        }
        else
        {
            _il.Emit(OpCodes.Pop);
        }
    }

    private void EmitSequencePoint(BoundNode node)
    {
        if (_document == null || _sourceText == null) return;
        if (node.Syntax is null || node.Syntax.Span.Length == 0) return;
        EmitSequencePointForSpan(node.Syntax.Span);
    }

    private void EmitSequencePointForToken(SyntaxToken token)
    {
        if (_document == null || _sourceText == null) return;
        if (token.Span.Length == 0) return;
        EmitSequencePointForSpan(token.Span);
    }

    private void EmitSequencePointForSpan(TextSpan span)
    {
        var loc = TextLocation.FromSpan(_sourceText!, span);
        _il.MarkSequencePoint(_document!,
            loc.StartLine + 1,       // 0-based → 1-based
            loc.StartCharacter + 1,  // 0-based → 1-based
            loc.EndLine + 1,         // 0-based → 1-based
            loc.EndCharacter + 1);   // 0-based → 1-based
    }

    private void SetLocalSymInfo(LocalBuilder local, string name)
    {
        if (_document != null)
            local.SetLocalSymInfo(name);
    }

    private static void WriteRuntimeConfig(string dllPath)
    {
        var configPath = Path.ChangeExtension(dllPath, ".runtimeconfig.json");
        var config = """
            {
              "runtimeOptions": {
                "tfm": "net10.0",
                "framework": {
                  "name": "Microsoft.NETCore.App",
                  "version": "10.0.0"
                }
              }
            }
            """;
        File.WriteAllText(configPath, config);
    }
}
